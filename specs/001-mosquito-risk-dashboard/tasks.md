---

description: "Task list for Mosquito Risk Dashboard implementation"
---

# Tasks: Mosquito Risk Dashboard

**Input**: Design documents from `/specs/001-mosquito-risk-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Include tests for any non-trivial domain logic. Tests are optional only for trivial glue code.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish backend/frontend project skeletons, dependency tooling, and test harness.

- [X] T001 Create backend package skeleton per plan in backend/src/{api,domain,services,infra,eda}/__init__.py
- [X] T002 Create backend test skeleton per plan in backend/tests/{unit,integration}/__init__.py
- [X] T003 Create frontend skeleton folders per plan in frontend/src/{pages,components,services}/ and frontend/tests/
- [X] T004 [P] Add `backend/README.md` describing local dev run for backend
- [X] T005 [P] Add `frontend/README.md` describing local dev run for frontend
- [X] T006 Add pytest configuration and ensure `pytest` is available via pyproject.toml (update pyproject.toml)
- [X] T007 Add backend runnable entrypoint (module) in backend/__main__.py
- [X] T008 Add backend application config loader stub in backend/src/infra/config.py
- [X] T009 Add shared typing models module stub in backend/src/domain/types.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required by all user stories (datasets config, caching, Earth Engine adapter, geocoding adapter, validation, and reusable EDA methods).

 **⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T010 Implement `resources/sources.yaml` loader in backend/src/infra/sources.py
- [X] T011 Implement filesystem cache layout and helpers in backend/src/infra/cache.py
- [X] T012 Implement dataset download/extract utilities (zip + geojson) in backend/src/infra/datasets.py
- [X] T013 Add dataset EDA summary utilities (schema, missingness, basic stats) in backend/src/eda/data_exploration.py
- [X] T014 Add visualization helpers contract (no decorative charts; clear labels/captions) in backend/src/eda/visualization.py
- [X] T015 Implement Earth Engine initialization adapter in backend/src/infra/ee_client.py (no tokens logged)
- [X] T016 Implement Folium/Leaflet tile URL generation helper (EE getMapId wrapper) in backend/src/infra/ee_tiles.py
- [X] T017 Implement geocoding interface + stub adapter in backend/src/infra/geocoding.py
- [X] T018 Implement domain models for Location/DateRange/RiskBand in backend/src/domain/models.py
- [X] T019 Implement input validation helpers (date range, empty strings) in backend/src/domain/validation.py
- [X] T020 Add domain exceptions (e.g., InvalidLocationError, InvalidDateRangeError, DataUnavailableError) in backend/src/domain/errors.py
- [X] T021 Add structured logging setup for backend in backend/src/infra/logging.py
- [X] T022 Add FastAPI app factory in backend/src/api/app.py
- [X] T023 Add API error handlers mapping domain errors to 400/404/500 in backend/src/api/errors.py

### Tests for Foundational

- [X] T024 [P] Add unit tests for sources.yaml parsing in backend/tests/unit/test_sources.py
- [X] T025 [P] Add unit tests for DateRange validation in backend/tests/unit/test_validation.py
- [X] T026 [P] Add unit tests for RiskBand mapping and legend ordering in backend/tests/unit/test_risk_bands.py

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - View Default Mosquito Risk Maps (Priority: P1) 

**Goal**: Home page shows two Florida-wide risk overlays (last 30 days and last 12 months) as categorical bands with a legend.

**Independent Test**: Start backend + frontend; load home page; verify two map overlays render for Florida with distinct titles/labels and a Low/Med/High legend.

### Tests for User Story 1

- [X] T027 [P] [US1] Add API contract test for GET /api/risk/default in backend/tests/integration/test_api_risk_default.py
- [X] T028 [P] [US1] Add unit tests for risk classification thresholds (Low/Med/High) in backend/tests/unit/test_risk_classification.py

### Implementation for User Story 1

- [X] T029 [US1] Implement RiskService default-window orchestration in backend/src/services/risk_service.py
- [X] T030 [US1] Implement Florida geometry loader from configured dataset in backend/src/infra/regions.py
- [X] T031 [US1] Implement risk layer computation from EE image sets (NDVI/LST/precip) in backend/src/eda/risk_mapping.py
- [X] T032 [US1] Implement GET /api/risk/default endpoint in backend/src/api/routes/risk.py
- [X] T033 [US1] Implement backend response schema (RiskLayerResponse) in backend/src/api/schemas.py
- [X] T034 [P] [US1] Create frontend API client for default risk in frontend/src/services/api.ts
- [X] T035 [P] [US1] Create Leaflet map component supporting raster tile overlays in frontend/src/components/RiskMap.tsx
- [X] T036 [US1] Create home page rendering two RiskMap panels in frontend/src/pages/Home.tsx
- [X] T037 [US1] Add legend UI (Low/Med/High) with clear labels in frontend/src/components/RiskLegend.tsx

**Checkpoint**: User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 - Explore Risk by Location and Date Range (Priority: P2)

**Goal**: User can input City/ZIP and date range on home page and refresh overlays. ZIP/point-based
queries analyze an area within a 100-mile radius. Both charts can show mosquito risk alongside
land-surface temperature, land coverage, and precipitation layers.

**Independent Test**: On home page, enter a ZIP + date range; submit; verify overlays update to the 100-mile
radius area or show a clear validation error. Verify both charts allow viewing mosquito risk, land-surface
temperature, land coverage, and precipitation layers for the same location/date range.

### Tests for User Story 2

- [X] T038 [P] [US2] Add API contract test for POST /api/risk/query in backend/tests/integration/test_api_risk_query.py
- [X] T039 [P] [US2] Add unit tests for geocoding adapter error behavior in backend/tests/unit/test_geocoding.py

### Implementation for User Story 2

- [X] T040 [US2] Implement POST /api/risk/query endpoint in backend/src/api/routes/risk.py
- [X] T041 [US2] Implement request schema (RiskQueryRequest) validation in backend/src/api/schemas.py
- [X] T042 [US2] Implement geocoding adapter (city/zip -> geometry) in backend/src/infra/geocoding.py
- [X] T043 [US2] Implement RiskService query flow using geocoded Location + DateRange in backend/src/services/risk_service.py
- [X] T044 [P] [US2] Add home page form UI (City/ZIP + date range) in frontend/src/components/RiskQueryForm.tsx
- [X] T045 [US2] Wire form submission to API and update both map panels in frontend/src/pages/Home.tsx
- [X] T046 [US2] Add loading/empty/error states to Home page in frontend/src/pages/Home.tsx
- [X] T064 [US2] Adjust query region derivation to enforce 100-mile radius for ZIP/point-based queries in backend/src/services/risk_service.py
- [X] T065 [US2] Extend backend response to support multiple overlay layers (risk + LST + land cover + precipitation) for /api/risk/default and /api/risk/query (new response schema + service changes)
- [X] T066 [US2] Update frontend map panels to allow switching between overlay layers (risk/LST/land cover/precip) in frontend/src/components/RiskMap.tsx and frontend/src/pages/Home.tsx
- [X] T067 [P] [US2] Add integration test coverage for 100-mile radius behavior (mock geocoder point result) in backend/tests/integration/test_api_risk_query.py

- [X] T073 [US2] Add viewport metadata to POST /api/drivers response (center + radius) and use it to center driver mini-maps (remove hardcoded Florida center) in backend/src/services/drivers_service.py, backend/src/api/schemas.py, frontend/src/components/DriverTile.tsx
- [X] T074 [US3] Fix Drivers page query context behavior: make date range explicit/editable on Drivers page and ensure changing location does not silently reuse stale initialQuery date range in frontend/src/pages/Drivers.tsx and frontend/src/services/api.ts
- [X] T068 [US2] Fix home page UX mismatch after a query by updating panel titles and/or behavior to reflect the queried location/date range in frontend/src/pages/Home.tsx
- [X] T069 [US2] Add minimal API-level validation for RiskQueryRequestSchema.location_text (e.g., non-empty/trimmed + max length) in backend/src/api/schemas.py

**Checkpoint**: User Story 2 works independently (even if US3 is not implemented).

---

## Phase 5: User Story 3 - View Environmental Drivers (Priority: P3)

**Goal**: A second page provides 3 tiles (2-year window) for vegetation, temperature, precipitation/standing water changes.

**Independent Test**: Navigate to drivers page; enter City/ZIP; verify 3 tiles render with clear captions and a 2-year window label.

### Tests for User Story 3

- [X] T047 [P] [US3] Add API contract test for POST /api/drivers in backend/tests/integration/test_api_drivers.py

### Implementation for User Story 3

- [X] T048 [US3] Implement DriversService orchestration in backend/src/services/drivers_service.py
- [X] T049 [US3] Implement vegetation drivers (NDVI/NDWI summary) in backend/src/eda/drivers_vegetation.py
- [X] T050 [US3] Implement temperature drivers (LST summary) in backend/src/eda/drivers_temperature.py
- [X] T051 [US3] Implement precipitation/standing water drivers (CHIRPS + NDWI proxy) in backend/src/eda/drivers_precip_water.py
- [X] T052 [US3] Implement POST /api/drivers endpoint in backend/src/api/routes/drivers.py
- [X] T053 [US3] Implement DriversResponse schema in backend/src/api/schemas.py
- [X] T054 [P] [US3] Add frontend API client for drivers in frontend/src/services/api.ts
- [X] T055 [P] [US3] Implement driver tiles UI in frontend/src/components/DriverTile.tsx
- [X] T056 [US3] Implement drivers page in frontend/src/pages/Drivers.tsx
- [X] T057 [US3] Add navigation link from home page to drivers page in frontend/src/pages/Home.tsx

**Checkpoint**: User Story 3 is independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improve reliability, reproducibility, and usability across all user stories.

- [X] T058 [P] Add documentation about clearing notebook outputs before commits in README.md
- [X] T059 Add backend request logging (without secrets) and correlation IDs in backend/src/infra/logging.py
- [X] T060 Add caching of dataset downloads and EE tile map IDs with TTL in backend/src/infra/cache.py
- [X] T061 Add rate limiting or basic request throttling in backend/src/api/middleware.py
- [X] T062 Add end-to-end smoke test script described in specs/001-mosquito-risk-dashboard/quickstart.md
- [X] T063 Run quickstart.md validation and update quickstart.md if steps diverge
- [X] T070 [US2] Move Earth Engine geometry conversion and buffering logic out of backend/src/services/risk_service.py into an infra adapter (e.g., backend/src/infra/ee_geometry.py) and keep RiskService orchestration-focused
- [X] T071 [US2] Add caching and basic rate-limit protection for geocoding requests (e.g., TTL cache keyed by normalized location_text + simple retry/backoff on 429/5xx) in backend/src/infra/geocoding.py
- [X] T072 Harden dataset download/extraction: safe zip extraction and streaming downloads to reduce memory usage in backend/src/infra/datasets.py

- [X] T075 [US3] Improve Sentinel-2 vegetation/water composites by applying cloud masking before NDVI/NDWI generation in backend/src/services/drivers_service.py
- [X] T076 [US3] Improve precipitation visualization scaling based on window length and add dataset attribution strings to driver tiles in backend/src/services/drivers_service.py, backend/src/api/schemas.py, frontend/src/services/api.ts, frontend/src/components/DriverTile.tsx
- [X] T077 [US3] Align DriversResponse contract: ensure date_range is always present (or update frontend typing to match) in backend/src/api/schemas.py and frontend/src/services/api.ts

- [ ] T078 [P1] Remove token-leakage footgun for EE tile URLs: ensure request logging cannot accidentally log `tile_url_template` values (e.g., add URL redaction helper + explicitly avoid logging response bodies containing `?token=`) and add a regression test
- [ ] T079 [P1] Fix EE map-id caching effectiveness in backend/src/infra/ee_tiles.py by replacing `id(image)` cache keying with a stable image identity (and include vis params) so cache survives across requests
- [ ] T080 [P1] Harden dataset downloads in backend/src/infra/datasets.py: add explicit timeouts, validate HTTP status, and reuse shared TTL helper (`is_fresh`) instead of ad-hoc mtime math
- [ ] T081 [P2] Reduce rate limiter memory growth risk in backend/src/api/middleware.py: cap number of tracked clients / add periodic cleanup, and add unit tests for 429 behavior + cleanup
- [ ] T082 [P2] Align docs references to agent principles: fix references to `AGENTS.md` to match actual filename (`AGENT.md`) in docs (e.g., docs/prompt_journal.md) to avoid drift

### Phase 6b: Fix Flat Layer Rendering (Code Analysis Follow-up)

- [X] T083 [P1] Replace RiskService environmental layer constant stubs with real Earth Engine ImageCollection queries: implement LST (MODIS/061/MOD11A1 with mean aggregation and Kelvin to Celsius conversion), precipitation (UCSB-CHG/CHIRPS/DAILY with sum aggregation), and NDVI (Sentinel-2 SR Harmonized with cloud masking and normalizedDifference) in backend/src/services/risk_service.py `_layers()` method, matching notebook cell 4 implementation
- [X] T084 [P1] Implement real risk classification logic in backend/src/eda/risk_mapping.py `build_default_risk_image()`: compute NDVI, LST, and precipitation from Earth Engine ImageCollections, calculate regional mean thresholds via reduceRegion, apply pixel-wise classification using conditional logic (low/medium/high risk based on vegetation, temperature, and rainfall), matching notebook cells 7-8 implementation
- [X] T085 [P1] Add NDVI computation and cloud masking helper to RiskService: implement `_mask_s2_clouds()` function using QA60 band bit masking (bits 10 and 11 for clouds and cirrus) and integrate NDVI calculation via normalizedDifference(['B8', 'B4']) in backend/src/services/risk_service.py, matching notebook cell 2 and DriversService pattern
- [X] T086 [P2] Add integration test to verify non-constant pixel variation in generated tile layers: create test that fetches risk/LST/NDVI/precipitation tiles via API, samples multiple pixels from returned Earth Engine images, and asserts non-uniform values to prevent regression to constant stubs in backend/tests/integration/test_layer_variation.py

### Phase 6c: Error Console Logging (User Error Visibility)

- [X] T087 [P1] Create ErrorConsole component in frontend/src/components/ErrorConsole.tsx: implement component that displays error messages with interpreted user-friendly guidance (503 → "Earth Engine is not initialized", 500 → "Internal server error", 400 → "Bad request", 404 → "Resource not found"), shows last 5 lines of stack trace when available, and uses clear visual styling (red border, monospace font, positioned at top of page)
- [X] T088 [P1] Integrate ErrorConsole into Home page (frontend/src/pages/Home.tsx): update error state to capture full Error objects (not just strings), replace simple error div with ErrorConsole component, preserve stack traces from API calls, and position error console at top of page above all other content
- [X] T089 [P1] Integrate ErrorConsole into Drivers page (frontend/src/pages/Drivers.tsx): update error state to capture full Error objects, replace simple error div with ErrorConsole component, preserve stack traces from API calls, and position error console at top of page above form inputs

### Phase 6d: Single Map View with Default Parameters (Simplification)

- [ ] T090 [P1] Update backend default query parameters in backend/src/api/routers/risk.py: change default location from "Florida" to ZIP code "33172" and default date range from last_30_days/last_12_months to fixed range 2023-01-01 to 2024-12-31
- [ ] T091 [P1] Update Home page to single map view in frontend/src/pages/Home.tsx: remove second map component, update layout to display single RiskMap component, update default form values to ZIP 33172 and date range 2023-01-01 to 2024-12-31
- [ ] T092 [P1] Update Drivers page to single map view in frontend/src/pages/Drivers.tsx: ensure single map display for user-specified location and date range, update form handling to match new single map pattern
- [ ] T093 [P2] Update API response schemas in backend/src/domain/schemas.py: ensure DriversResponse and related schemas support single map view (remove any dual-window artifacts if present)
- [ ] T094 [P2] Add integration tests for default parameters in backend/tests/integration/test_api_risk_default.py: verify API returns correct response for default ZIP 33172 and date range 2023-01-01 to 2024-12-31
- [ ] T095 [P2] Update frontend E2E tests (if present) to verify single map view on Home page loads with correct defaults (ZIP 33172, date range 2023-01-01 to 2024-12-31)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup; blocks all user stories
- **User Stories (Phase 3-5)**: Depend on Foundational; can proceed in parallel if staffed
- **Polish (Phase 6)**: Depends on whichever user stories are in scope

### User Story Dependencies

- **US1 (P1)**: No dependencies after Phase 2
- **US2 (P2)**: No dependencies after Phase 2
- **US3 (P3)**: No dependencies after Phase 2

### Parallel Opportunities

- Tasks marked **[P]** are safe to parallelize (different files, minimal coupling).
- Within backend, EDA modules under `backend/src/eda/` can often be developed in parallel.
- Within frontend, component work (maps, legend, tiles, forms) can proceed in parallel with API work once contracts are stable.

---

## Parallel Example: User Story 1

```bash
Task: "T034 [P] [US1] Create frontend API client for default risk in frontend/src/services/api.ts"
Task: "T035 [P] [US1] Create Leaflet map component supporting raster tile overlays in frontend/src/components/RiskMap.tsx"
Task: "T028 [P] [US1] Add unit tests for risk classification thresholds (Low/Med/High) in backend/tests/unit/test_risk_classification.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and validate US1 independently

### Incremental Delivery

1. US1 (default Florida overlays)
2. US2 (City/ZIP + date range exploration)
3. US3 (drivers page tiles)

## Notes

- EDA tasks must follow the EDA skills guidance:
  - Prefer summary statistics over intuition.
  - Surface data quality issues early.
  - Do not mutate original datasets.
  - Visualizations must be clear, labeled, and non-decorative.
- Do not log secrets (Earth Engine token or any credentials).
