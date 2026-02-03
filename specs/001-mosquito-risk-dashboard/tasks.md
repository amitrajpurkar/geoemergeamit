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

**Goal**: User can input City/ZIP and date range on home page and refresh overlays.

**Independent Test**: On home page, enter a City/ZIP + date range; submit; verify overlays update or show a clear validation error.

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

**Checkpoint**: User Story 2 works independently (even if US3 is not implemented).

---

## Phase 5: User Story 3 - View Environmental Drivers (Priority: P3)

**Goal**: A second page provides 3 tiles (2-year window) for vegetation, temperature, precipitation/standing water changes.

**Independent Test**: Navigate to drivers page; enter City/ZIP; verify 3 tiles render with clear captions and a 2-year window label.

### Tests for User Story 3

- [ ] T047 [P] [US3] Add API contract test for POST /api/drivers in backend/tests/integration/test_api_drivers.py

### Implementation for User Story 3

- [ ] T048 [US3] Implement DriversService orchestration in backend/src/services/drivers_service.py
- [ ] T049 [US3] Implement vegetation drivers (NDVI/NDWI summary) in backend/src/eda/drivers_vegetation.py
- [ ] T050 [US3] Implement temperature drivers (LST summary) in backend/src/eda/drivers_temperature.py
- [ ] T051 [US3] Implement precipitation/standing water drivers (CHIRPS + NDWI proxy) in backend/src/eda/drivers_precip_water.py
- [ ] T052 [US3] Implement POST /api/drivers endpoint in backend/src/api/routes/drivers.py
- [ ] T053 [US3] Implement DriversResponse schema in backend/src/api/schemas.py
- [ ] T054 [P] [US3] Add frontend API client for drivers in frontend/src/services/api.ts
- [ ] T055 [P] [US3] Implement driver tiles UI in frontend/src/components/DriverTile.tsx
- [ ] T056 [US3] Implement drivers page in frontend/src/pages/Drivers.tsx
- [ ] T057 [US3] Add navigation link from home page to drivers page in frontend/src/pages/Home.tsx

**Checkpoint**: User Story 3 is independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improve reliability, reproducibility, and usability across all user stories.

- [ ] T058 [P] Add documentation about clearing notebook outputs before commits in README.md
- [ ] T059 Add backend request logging (without secrets) and correlation IDs in backend/src/infra/logging.py
- [ ] T060 Add caching of dataset downloads and EE tile map IDs with TTL in backend/src/infra/cache.py
- [ ] T061 Add rate limiting or basic request throttling in backend/src/api/middleware.py
- [ ] T062 Add end-to-end smoke test script described in specs/001-mosquito-risk-dashboard/quickstart.md
- [ ] T063 Run quickstart.md validation and update quickstart.md if steps diverge

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
