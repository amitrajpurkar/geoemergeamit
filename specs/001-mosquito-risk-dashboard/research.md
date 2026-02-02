# Research: Mosquito Risk Dashboard

**Branch**: `001-mosquito-risk-dashboard`
**Date**: 2026-02-02
**Spec**: `specs/001-mosquito-risk-dashboard/spec.md`

## Decisions

### Backend API framework

- **Decision**: Use a small Python HTTP API service (FastAPI).
- **Rationale**:
  - Clear contract-driven API development.
  - Good typing + request validation.
  - Works well with a frontend that needs JSON and/or map tile URLs.
- **Alternatives considered**:
  - Flask (lighter but less built-in typing/validation).
  - Notebook-first UI (e.g., Voilà/Streamlit) (faster demo but blurs domain/web boundaries).

### Map overlay delivery format

- **Decision**: Backend returns map overlay as a **tile URL template** (raster tiles) plus legend metadata.
- **Rationale**:
  - Earth Engine already exposes tile endpoints via `getMapId()`.
  - Frontend can use Leaflet to render a basemap + overlay tiles.
  - Keeps payloads small (no large GeoJSON).
- **Alternatives considered**:
  - Returning GeoJSON polygons (heavy, requires pre-processing).
  - Generating static PNGs server-side (less interactive).

### Data sources

- **Decision**: Use a combination of:
  - Static datasets referenced in `resources/sources.yaml` under `datasets` (download/cache locally).
  - Google Earth Engine image sets referenced in `resources/sources.yaml` under `eeimagesets`.
- **Rationale**:
  - Matches existing notebooks and provides both point-based and remote-sensing drivers.

### Earth Engine authentication + secrets

- **Decision**: Earth Engine authentication MUST be handled outside code and credentials MUST NOT be embedded in the UI or logs.
- **Rationale**:
  - Prevents leaking tokens/credentials.
  - Supports local developer auth flow.
- **Operational approach**:
  - For development, developers authenticate locally (e.g., `earthengine authenticate`) and the backend uses `ee.Initialize(project=...)`.
  - Any token stored in `resources/sources.yaml` MUST be treated as sensitive and should be moved to environment/secret storage before deployment.

### Location resolution (City/ZIP)

- **Decision**: Accept City/ZIP text input and geocode it into a geometry.
- **Rationale**:
  - Matches clarified spec.
  - Keeps UI simple.
- **Alternatives considered**:
  - Lat/Lon direct input (simpler, but less user-friendly).
  - GeoJSON upload (powerful, but higher UX complexity).

### Risk classification strategy

- **Decision**: Represent mosquito risk as categorical bands: Low/Med/High.
- **Rationale**:
  - Matches clarified spec.
  - Aligns with notebook approach that classifies based on NDVI/LST/precip thresholds.
- **Notes**:
  - Initial implementation can replicate notebook logic:
    - Derive NDVI, LST, precipitation from EE image collections.
    - Compute summary stats (e.g., mean LST/rain) for the region/time window.
    - Classify pixels into Low/Med/High.

## Open Questions (to be handled in implementation)

- Exact geocoding provider and error handling strategy.
- Cache strategy for dataset downloads and EE tile IDs.
- How to blend static mosquito habitat points with EE-derived risk overlays (layering and legend).
