# Implementation Plan: Mosquito Risk Dashboard
 
 **Branch**: `001-mosquito-risk-dashboard` | **Date**: 2026-02-02 | **Spec**: `specs/001-mosquito-risk-dashboard/spec.md`
 **Input**: Feature specification from `/specs/001-mosquito-risk-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

 ## Summary
 
 Build a Python web application (frontend + backend) that visualizes mosquito risk as
 categorical bands (Low/Med/High) overlaid on a map.
 
 MVP home page shows a single default risk overlay for ZIP code 33172 with date range
 2023-01-01 to 2024-12-31.
 Users can also enter a City/ZIP and date range to refresh the risk overlay.
 For ZIP code (or point-resolved) queries, analysis uses an area within a
 100-mile radius of the resolved point.

 Home page map panel supports viewing mosquito risk alongside environmental
 layers (land-surface temperature, land coverage, precipitation) for the same
 location/date range.
 
 The application displays legends for all four map layers simultaneously (Risk,
 Land Surface Temperature, Vegetation/NDVI, Precipitation) on both the Home page
 and Environmental Drivers page, showing color scales and value ranges to enable
 proper interpretation regardless of which layer is currently active.
 
 A second page shows environmental driver tiles (2-year window): vegetation cover,
 temperature, and precipitation/standing water.
 
 Foundational work includes extracting reusable EDA/analysis logic from existing
 notebooks in `notebooks/` and modularizing it for backend service reuse.

 ## Technical Context

 **Language/Version**: Python 3.12 (repo `pyproject.toml`), targeting Python 3.10+ per constitution  
 **Primary Dependencies**: pandas, geopandas, folium, earthengine-api, geemap (existing); backend API framework to be confirmed in research (default: FastAPI)  
 **Storage**: Local files/cache (download static datasets from URLs in `resources/sources.yaml`); no DB required for MVP  
 **Testing**: pytest (required for non-trivial domain logic)  
 **Target Platform**: Local dev (mac) initially; deployable to a Linux server/container later
 **Project Type**: Web application (frontend + backend directories already present)
 **Performance Goals**: Initial render <10s; user-driven refresh <15s (from spec success criteria)
 **Constraints**: Do not expose secrets (Earth Engine token). Avoid long-running requests without progress/error states.
 **Scale/Scope**: Single-user / small-team demo; correctness + clarity prioritized

 ## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

 - **Clean Architecture Boundaries**: Domain logic isolated from web/framework code.
 - **Reproducible EDA**: Notebook-derived logic must be made reusable and rerunnable.
 - **Tests for Non-Trivial Logic**: Core risk classification + data transforms must be tested.
 - **Contract-Driven API**: Define clear API contracts for risk overlays and driver tiles.
 - **Observability & Safety**: Do not log secrets/PII; validate all external inputs.

 ## Project Structure

### Documentation (this feature)

 ```text
 specs/001-mosquito-risk-dashboard/
 ├── plan.md              # This file (/speckit.plan command output)
 ├── research.md          # Phase 0 output (/speckit.plan command)
 ├── data-model.md        # Phase 1 output (/speckit.plan command)
 ├── quickstart.md        # Phase 1 output (/speckit.plan command)
 ├── contracts/           # Phase 1 output (/speckit.plan command)
 └── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
 ```

### Source Code (repository root)

 ```text
 backend/
 ├── src/
 │   ├── api/                 # HTTP endpoints + request validation
 │   ├── domain/              # domain concepts (risk bands, date windows)
 │   ├── services/            # orchestration: risk + drivers use-cases
 │   ├── infra/               # datasets download/cache, GEE adapter, geocoding adapter
 │   └── eda/                 # extracted notebook logic (pure, testable)
 └── tests/
     ├── unit/
     └── integration/
 
 frontend/
 ├── src/
 │   ├── pages/               # home + drivers pages
 │   ├── components/          # map panels, tiles, form controls
 │   └── services/            # API client
 └── tests/
 ```

 **Structure Decision**: Web application with separate `backend/` and `frontend/`.
 Notebook-derived analysis code is extracted into `backend/src/eda/` and called by
 backend services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
