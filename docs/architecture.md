# Mosquito Risk Dashboard - Architecture Documentation

**Version:** 0.1.0  
**Last Updated:** February 8, 2026  
**Status:** Production-Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Style](#architecture-style)
3. [Technology Stack](#technology-stack)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [Data Flow](#data-flow)
7. [External Integrations](#external-integrations)
8. [Security & Performance](#security--performance)
9. [Testing Strategy](#testing-strategy)
10. [Deployment](#deployment)

---

## System Overview

### Purpose

The Mosquito Risk Dashboard is a geospatial web application that visualizes mosquito-borne disease risk by analyzing environmental factors across user-specified locations and date ranges. It leverages satellite imagery and Earth observation data to compute risk levels based on vegetation (NDVI), land surface temperature (LST), and precipitation patterns.

### Key Capabilities

- **Risk Visualization**: Pixel-wise mosquito risk classification (Low/Medium/High) displayed on interactive maps
- **Multi-Layer Analysis**: Simultaneous visualization of 4 environmental layers with color-coded legends
- **Location Flexibility**: Supports queries by ZIP code or city/state names via geocoding
- **Historical Analysis**: Processes satellite data for user-defined date ranges (2023-2024 default)
- **Environmental Drivers**: Detailed breakdown of temperature, vegetation, precipitation, and standing water indicators

### Users

- Public health officials planning vector control programs
- Residents assessing mosquito risk for outdoor activities
- Researchers analyzing environmental disease vectors

---

## Architecture Style

### Clean Architecture (Hexagonal)

The application follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (FastAPI Routes, React Pages)               │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│              (Services, Business Logic)                  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                      Domain Layer                        │
│         (Models, Validation, Domain Logic)               │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                    │
│     (Earth Engine, Geocoding, Caching, Config)          │
└─────────────────────────────────────────────────────────┘
```

**Benefits:**
- **Testability**: Domain logic is independent of frameworks and external services
- **Flexibility**: Infrastructure can be swapped without affecting business logic
- **Maintainability**: Clear boundaries prevent tight coupling

---

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.12+ | Core backend language |
| **Web Framework** | FastAPI | Latest | REST API, async support, OpenAPI |
| **Earth Engine** | earthengine-api | Latest | Satellite data processing |
| **Geospatial** | geopandas, folium, geemap | Latest | Geographic data manipulation |
| **Data Science** | pandas, scipy, matplotlib | Latest | Data analysis and visualization |
| **HTTP Client** | httpx | Latest | Async HTTP for geocoding |
| **Config** | pyyaml | Latest | YAML-based configuration |
| **Testing** | pytest | Latest | Unit and integration tests |
| **Server** | uvicorn | Latest | ASGI server |

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | TypeScript | 5.7+ | Type-safe frontend code |
| **Framework** | React | 18.3+ | UI component library |
| **Build Tool** | Vite | 6.1+ | Fast build and HMR |
| **Mapping** | Leaflet + React-Leaflet | 1.9+, 4.2+ | Interactive map rendering |
| **Styling** | CSS | - | Custom styles |

### External Services

- **Google Earth Engine**: Satellite imagery and geospatial computation platform
- **Nominatim (Geopy)**: Open-source geocoding service for location resolution

---

## Backend Architecture

### Directory Structure

```
backend/
├── __main__.py              # Entry point (uvicorn server)
├── src/
│   ├── api/                 # Presentation Layer
│   │   ├── app.py           # FastAPI app factory
│   │   ├── routes/          # REST endpoints
│   │   │   ├── risk.py      # /api/risk/* endpoints
│   │   │   └── drivers.py   # /api/drivers endpoint
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── errors.py        # Error handlers
│   │   └── middleware.py    # CORS, rate limiting, correlation ID
│   ├── services/            # Application Layer
│   │   ├── risk_service.py  # Risk calculation orchestration
│   │   └── drivers_service.py # Environmental drivers logic
│   ├── domain/              # Domain Layer
│   │   ├── models.py        # Domain entities (Location, DateRange, RiskBand)
│   │   ├── validation.py    # Business validation rules
│   │   ├── errors.py        # Domain exceptions
│   │   └── types.py         # Custom type definitions
│   ├── eda/                 # Analytics & Classification
│   │   ├── risk_mapping.py  # Pixel-wise risk classification
│   │   ├── drivers_*.py     # Driver-specific computations
│   │   └── visualization.py # Visualization utilities
│   └── infra/               # Infrastructure Layer
│       ├── ee_client.py     # Earth Engine initialization
│       ├── ee_tiles.py      # Tile URL generation
│       ├── ee_geometry.py   # Region/viewport utilities
│       ├── geocoding.py     # Location geocoding
│       ├── sources.py       # Config file management
│       ├── cache.py         # Caching abstraction
│       └── logging.py       # Structured logging
└── tests/
    ├── unit/                # Unit tests
    └── integration/         # API integration tests
```

### Layer Responsibilities

#### 1. API Layer (`api/`)

**Responsibility**: HTTP request handling, validation, serialization

**Key Components**:
- `app.py`: FastAPI application factory with middleware stack
- `routes/risk.py`: Risk-related endpoints (`GET /api/risk/default`, `POST /api/risk/query`)
- `routes/drivers.py`: Environmental drivers endpoint (`POST /api/drivers`)
- `schemas.py`: Pydantic models for request/response validation
- `middleware.py`: Cross-cutting concerns (CORS, rate limiting, correlation IDs)

**Design Patterns**:
- **Factory Pattern**: `create_app()` for testable app instantiation
- **Dependency Injection**: Services injected per-request
- **Middleware Chain**: CORS → Rate Limit → Correlation ID → Routes

#### 2. Services Layer (`services/`)

**Responsibility**: Business logic orchestration, workflow coordination

**Key Services**:

**`RiskService`**:
- Orchestrates risk calculation workflow
- Coordinates Earth Engine, geocoding, and risk mapping
- Generates multi-layer responses (Risk, LST, NDVI, Precipitation)
- Methods:
  - `get_default()`: Returns default risk for ZIP 33172 (2023-2024)
  - `query()`: Computes risk for user-specified location and date range

**`DriversService`**:
- Computes environmental driver tiles (vegetation, temperature, precipitation, standing water)
- Generates NDVI, LST, precipitation, and NDWI images
- Methods:
  - `query()`: Returns driver analysis for location and date range

**Design Patterns**:
- **Service Layer Pattern**: Business logic abstraction
- **Repository Pattern**: Delegates data access to infrastructure layer

#### 3. Domain Layer (`domain/`)

**Responsibility**: Core business entities, validation rules, domain logic

**Key Models**:
- `Location`: Geographic location with geometry and bounding box
- `DateRange`: Start/end date with validation
- `RiskBand`: Risk classification (Low/Medium/High) with colors
- `LocationSource`: Enum for location origin (default/geocoded)

**Validation Rules**:
- Date range: Max 5 years, start ≤ end, not future dates
- Location: Valid geocoding results required

**Design Patterns**:
- **Value Objects**: Immutable dataclasses (`@dataclass(frozen=True)`)
- **Domain Exceptions**: Custom errors (`InvalidDateRangeError`, `DataUnavailableError`)

#### 4. EDA Layer (`eda/`)

**Responsibility**: Earth Engine analytics, risk classification algorithms

**Key Module: `risk_mapping.py`**

**`build_default_risk_image()`**:
Implements pixel-wise risk classification matching Jupyter notebook algorithm:

1. **Data Acquisition**:
   - NDVI from Sentinel-2 SR Harmonized (cloud-masked)
   - LST from MODIS MOD11A1 (converted to Celsius)
   - Precipitation from CHIRPS Daily (summed over date range)

2. **Regional Threshold Computation** (Server-Side):
   ```python
   mean_lst = ee.Number(lst_img.reduceRegion(...).get("LST_Day_1km"))
   mean_rain = ee.Number(precip_img.reduceRegion(...).get("precipitation"))
   ```

3. **Pixel-Wise Classification**:
   ```python
   low_risk = ndvi.lt(0).And(lst.lt(mean_lst)).And(rain.lt(mean_rain))
   med_risk = ndvi.lte(0.3).Or(lst.eq(mean_lst)).Or(rain.eq(mean_rain))
   high_risk = ndvi.gt(0.3).And(lst.gt(mean_lst)).And(rain.gt(mean_rain))
   
   risk = low_risk.multiply(0).add(med_risk.multiply(1)).add(high_risk.multiply(2))
   ```

4. **Output**: `ee.Image` with "Risk_Level" band (0=Low, 1=Medium, 2=High)

**Design Patterns**:
- **Strategy Pattern**: Classification algorithm encapsulated in function
- **Server-Side Computation**: All operations use Earth Engine server-side primitives (no `.getInfo()`)

#### 5. Infrastructure Layer (`infra/`)

**Responsibility**: External service integration, configuration, caching

**Key Modules**:

**`ee_client.py`**: Earth Engine initialization and authentication
**`ee_tiles.py`**: Converts `ee.Image` to XYZ tile URLs via `getMapId()`
**`ee_geometry.py`**: Region and viewport utilities from geocoding results
**`geocoding.py`**: Nominatim-based geocoding (httpx client)
**`sources.py`**: YAML config loading for Earth Engine dataset IDs
**`cache.py`**: Caching abstraction (future: Redis/disk cache)
**`logging.py`**: Structured logging configuration

**Configuration** (`resources/sources.yaml`):
```yaml
googleearthengine:
  projectid: "anr-41793"
eeimagesets:
  vegetation: "COPERNICUS/S2_SR_HARMONIZED"
  land_surface_temperature: "MODIS/061/MOD11A1"
  precipitation: "UCSB-CHG/CHIRPS/DAILY"
```

**Design Patterns**:
- **Adapter Pattern**: Wraps external APIs with domain-friendly interfaces
- **Singleton Pattern**: Earth Engine client initialized once
- **Configuration as Code**: YAML-based, version-controlled settings

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── index.html               # HTML entry point
├── vite.config.ts           # Vite build configuration
├── package.json             # Dependencies
├── src/
│   ├── main.tsx             # React app bootstrap
│   ├── App.tsx              # Root component with routing
│   ├── pages/               # Page-level components
│   │   ├── Home.tsx         # Default risk map view
│   │   └── Drivers.tsx      # Environmental drivers view
│   ├── components/          # Reusable UI components
│   │   ├── RiskMap.tsx      # Leaflet map with tile overlay
│   │   ├── RiskQueryForm.tsx # Location/date input form
│   │   ├── MultiLayerLegend.tsx # 4-layer legend display
│   │   ├── RiskLegend.tsx   # Single risk legend (legacy)
│   │   ├── DriverTile.tsx   # Individual driver visualization
│   │   └── ErrorConsole.tsx # Error message display
│   ├── services/            # API client layer
│   │   └── api.ts           # Fetch wrappers + TypeScript types
│   └── styles.css           # Global styles
└── tests/                   # (Future: Playwright/Vitest)
```

### Component Architecture

#### Pages

**`Home.tsx`**:
- Default view: ZIP 33172, 2023-01-01 to 2024-12-31
- Single map with 4-layer selector (Risk, LST, NDVI, Precipitation)
- `MultiLayerLegend` displays all 4 legends simultaneously
- Query form allows custom location/date range
- State management: `useState` for data, loading, errors

**`Drivers.tsx`**:
- Environmental drivers analysis for user-specified location
- 4 tiles: Vegetation (NDVI), Temperature (LST), Precipitation, Standing Water (NDWI)
- Each tile shows map + summary + legend
- Prefills query from Home page parameters

#### Components

**`RiskMap.tsx`**:
- Wraps `react-leaflet` `MapContainer`
- Renders OpenStreetMap base layer + Earth Engine tile overlay
- Props: `layer` (metadata), `overlayUrl` (XYZ tile template), `overlayAttribution`

**`MultiLayerLegend.tsx`**:
- Displays 4 legends (Risk, LST, NDVI, Precipitation)
- **Categorical legend** (Risk): Color boxes with labels (Low/Medium/High)
- **Continuous legends** (LST, NDVI, Precipitation): Gradient bars with min/max values + units
- Flexible type support: Accepts both `OverlayLayer` and `DriverTile` types

**`RiskQueryForm.tsx`**:
- Controlled form inputs: location (text), start_date, end_date
- Validation: Required fields, date format
- Submit handler triggers API call

**`ErrorConsole.tsx`**:
- Displays API errors in styled panel
- Auto-hides when error is null

**`DriverTile.tsx`**:
- Individual driver visualization (vegetation/temperature/precipitation/water)
- Leaflet map + summary text + legend
- Props: `tile` (driver data), `viewport` (map center/zoom)

### State Management

- **Local State**: `useState` for page-level data (no global store)
- **Data Flow**: Unidirectional (parent → child via props)
- **Side Effects**: `useEffect` for API calls on mount

### API Client (`services/api.ts`)

**Type Definitions**:
```typescript
export type RiskLayerResponse = {
  location_label: string
  date_range: DateRange
  tile_url_template: string
  layers: OverlayLayer[]  // 4 layers with legend metadata
  viewport?: Viewport
}
```

**API Functions**:
- `fetchDefaultRisk()`: GET `/api/risk/default`
- `fetchRiskQuery(body)`: POST `/api/risk/query`
- `fetchDrivers(body)`: POST `/api/drivers`

**Error Handling**: Throws errors with `detail` message from API

---

## Data Flow

### Risk Calculation Flow

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │ 1. GET /api/risk/default
       ▼
┌──────────────────────────────────────┐
│      FastAPI (risk.py)               │
│  - Validates request                 │
│  - Calls RiskService.get_default()   │
└──────┬───────────────────────────────┘
       │ 2. Orchestrates workflow
       ▼
┌──────────────────────────────────────┐
│      RiskService                     │
│  - Loads config (sources.yaml)       │
│  - Initializes Earth Engine client   │
│  - Geocodes location (if needed)     │
│  - Calls risk_mapping module         │
└──────┬───────────────────────────────┘
       │ 3. Compute risk image
       ▼
┌──────────────────────────────────────┐
│  risk_mapping.build_default_risk_image│
│  - Fetches NDVI, LST, precipitation  │
│  - Computes regional means           │
│  - Classifies pixels (low/med/high)  │
│  - Returns ee.Image                  │
└──────┬───────────────────────────────┘
       │ 4. Generate tile URL
       ▼
┌──────────────────────────────────────┐
│     ee_tiles.ee_image_tile_url_template│
│  - Calls ee.Image.getMapId()         │
│  - Returns XYZ tile URL template     │
└──────┬───────────────────────────────┘
       │ 5. Build response
       ▼
┌──────────────────────────────────────┐
│      RiskService._layers()           │
│  - Generates 4 layers (Risk, LST,    │
│    NDVI, Precipitation)              │
│  - Includes legend metadata          │
│  - Returns list[dict]                │
└──────┬───────────────────────────────┘
       │ 6. JSON response
       ▼
┌──────────────────────────────────────┐
│      FastAPI Response                │
│  {                                   │
│    "location_label": "33172",        │
│    "layers": [                       │
│      {                               │
│        "layer_id": "risk",           │
│        "tile_url_template": "...",   │
│        "legend": {...}               │
│      }, ...                          │
│    ]                                 │
│  }                                   │
└──────┬───────────────────────────────┘
       │ 7. Render map
       ▼
┌──────────────────────────────────────┐
│      React Frontend                  │
│  - RiskMap renders Leaflet map       │
│  - Loads tiles from Earth Engine     │
│  - MultiLayerLegend shows 4 legends  │
└──────────────────────────────────────┘
```

### Key Observations

1. **Server-Side Computation**: All Earth Engine operations run server-side (no `.getInfo()` calls)
2. **Tile-Based Rendering**: Frontend only receives tile URLs, not raw pixel data
3. **Lazy Evaluation**: Earth Engine computes tiles on-demand when browser requests specific zoom/x/y coordinates
4. **Stateless API**: Each request is independent (no session state)

---

## External Integrations

### Google Earth Engine

**Purpose**: Cloud-based geospatial processing platform

**Integration Pattern**:
1. **Authentication**: Service account credentials in `resources/ee-service-account.json` (gitignored)
2. **Initialization**: `ee.Initialize(project=...)` in `ee_client.py`
3. **Computation**: Server-side operations using `ee.ImageCollection`, `ee.Image`, `ee.Reducer`
4. **Visualization**: `getMapId()` generates signed tile URLs valid for ~24 hours

**Datasets Used**:
- **Sentinel-2 SR Harmonized**: High-resolution optical imagery (10-20m)
- **MODIS MOD11A1**: Land surface temperature (1km)
- **CHIRPS Daily**: Precipitation estimates (5km)

**Rate Limits**: Managed by Earth Engine (typically 3000 concurrent requests)

### Nominatim Geocoding

**Purpose**: Convert location text (ZIP, city/state) to lat/lon coordinates

**Integration**:
- Library: `geopy.geocoders.Nominatim`
- HTTP Client: `httpx` (async)
- User Agent: `"mosquito-risk-dashboard"`

**Fallback**: If geocoding fails, returns error to client

---

## Security & Performance

### Security Measures

1. **CORS Protection**: Whitelist `localhost:5173` and `127.0.0.1:5173`
2. **Rate Limiting**: Basic middleware (20 requests/minute per IP)
3. **Input Validation**: Pydantic schemas enforce type/format constraints
4. **Secret Management**: Service account credentials in gitignored files
5. **Error Sanitization**: Generic error messages to clients (no stack traces)

### Performance Optimizations

1. **Server-Side Processing**: Earth Engine handles heavy computation
2. **Tile-Based Rendering**: Only requested map tiles are computed
3. **Async Endpoints**: FastAPI async handlers for I/O-bound operations
4. **Caching (Future)**: Tile URLs cached for repeated queries
5. **Lazy Loading**: Frontend loads tiles on-demand during pan/zoom

### Monitoring & Logging

- **Structured Logging**: JSON logs with correlation IDs
- **Log Levels**: DEBUG (development), INFO (production), ERROR (failures)
- **Correlation IDs**: Trace requests across service boundaries

---

## Testing Strategy

### Backend Tests

**Unit Tests** (`tests/unit/`):
- Domain validation logic
- Service orchestration (mocked infrastructure)
- Utility functions

**Integration Tests** (`tests/integration/`):
- `test_api_risk_default.py`: Default endpoint behavior
- `test_layer_legends.py`: Legend metadata validation
- `test_risk_variation.py`: **Regression test for constant risk bug** (verifies pixel variation)

**Test Execution**:
```bash
pytest backend/tests -v
```

### Frontend Tests (Future)

- **Unit Tests**: Component rendering (Vitest + React Testing Library)
- **E2E Tests**: User workflows (Playwright)

---

## Deployment

### Development

**Backend**:
```bash
uv run python -m backend
# Runs on http://127.0.0.1:8000
```

**Frontend**:
```bash
cd frontend && npm run dev
# Runs on http://127.0.0.1:5173
```

### Production (Future)

**Backend**:
- **Container**: Dockerized FastAPI app
- **Server**: Uvicorn with Gunicorn workers
- **Platform**: Cloud Run, AWS Lambda, or Kubernetes

**Frontend**:
- **Build**: `npm run build` → static assets in `dist/`
- **Hosting**: Netlify, Vercel, S3 + CloudFront, or Nginx

**Environment Variables**:
- `VITE_API_BASE`: Backend API URL (frontend)
- `EE_SERVICE_ACCOUNT`: Path to service account JSON (backend)

---

## Design Decisions

### Why Clean Architecture?

- **Testability**: Domain logic tested without Earth Engine/geocoding
- **Flexibility**: Swap Earth Engine for local processing in future
- **Clarity**: Clear boundaries prevent "big ball of mud"

### Why FastAPI?

- **Performance**: Async support for I/O-bound operations
- **Developer Experience**: Auto-generated OpenAPI docs, type hints
- **Ecosystem**: Native Pydantic integration for validation

### Why React + TypeScript?

- **Type Safety**: Catch errors at compile time
- **Ecosystem**: Rich library ecosystem (Leaflet, Vite)
- **Developer Experience**: Fast HMR, modern tooling

### Why Pixel-Wise Classification?

- **Accuracy**: Captures spatial variation in risk
- **Scientific Validity**: Matches Jupyter notebook research algorithm
- **Scalability**: Earth Engine handles computation server-side

---

## Future Enhancements

### Short-Term

1. **Caching Layer**: Redis for tile URL caching (reduce Earth Engine calls)
2. **Advanced Rate Limiting**: Token bucket algorithm with user accounts
3. **Error Telemetry**: Sentry integration for production monitoring
4. **E2E Tests**: Playwright tests for critical user flows

### Medium-Term

1. **User Accounts**: Save queries, receive alerts for high-risk areas
2. **Real-Time Data**: Integrate near-real-time satellite feeds
3. **Mobile App**: React Native or PWA for field use
4. **Export Features**: Download risk maps as GeoTIFF or PDF

### Long-Term

1. **Predictive Modeling**: Machine learning for future risk forecasting
2. **Multi-Disease Support**: Expand to Zika, Dengue, West Nile virus
3. **Public Health Integration**: CDC/WHO data feeds for outbreak correlation
4. **Citizen Science**: User-submitted mosquito observations

---

## Key Files Reference

### Backend

| File | Purpose |
|------|---------|
| `backend/src/api/app.py` | FastAPI application factory |
| `backend/src/services/risk_service.py` | Risk calculation orchestration |
| `backend/src/eda/risk_mapping.py` | **Pixel-wise risk classification algorithm** |
| `backend/src/infra/ee_client.py` | Earth Engine initialization |
| `backend/src/infra/geocoding.py` | Nominatim geocoding client |
| `resources/sources.yaml` | Earth Engine dataset configuration |

### Frontend

| File | Purpose |
|------|---------|
| `frontend/src/App.tsx` | Root component with page routing |
| `frontend/src/pages/Home.tsx` | Default risk map view |
| `frontend/src/components/RiskMap.tsx` | Leaflet map wrapper |
| `frontend/src/components/MultiLayerLegend.tsx` | **4-layer legend display** |
| `frontend/src/services/api.ts` | API client with TypeScript types |

### Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python dependencies (uv/pip) |
| `frontend/package.json` | Node.js dependencies (npm) |
| `.gitignore` | Excludes credentials, build artifacts |
| `resources/ee-service-account.json` | **Earth Engine credentials (gitignored)** |

---

## Glossary

- **NDVI**: Normalized Difference Vegetation Index (vegetation health metric)
- **LST**: Land Surface Temperature (satellite-measured ground temperature)
- **CHIRPS**: Climate Hazards Group InfraRed Precipitation with Station data
- **NDWI**: Normalized Difference Water Index (standing water detection)
- **XYZ Tiles**: Standard web map tile format (zoom/x/y coordinates)
- **Earth Engine**: Google's planetary-scale geospatial analysis platform
- **Clean Architecture**: Layered architecture with dependency inversion principle

---

## Conclusion

The Mosquito Risk Dashboard demonstrates a production-ready architecture combining:

1. **Clean separation of concerns** (domain, services, infrastructure)
2. **Server-side geospatial computation** (Earth Engine)
3. **Modern web stack** (FastAPI, React, TypeScript)
4. **Scientific rigor** (peer-reviewed classification algorithm)
5. **Extensibility** (modular design for future enhancements)

The architecture prioritizes **maintainability**, **testability**, and **scalability** while delivering accurate, actionable mosquito risk insights to end users.
