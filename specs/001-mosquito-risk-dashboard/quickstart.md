# Quickstart: Mosquito Risk Dashboard

**Branch**: `001-mosquito-risk-dashboard`

## Prerequisites

- Python 3.12 (repo currently uses `requires-python = ">=3.12"`)
- Access to Google Earth Engine project `anr-41793`
- Local Earth Engine auth configured (developer machine)

## Setup

1. Create and sync the environment (uv):

```bash
uv sync
```

2. Authenticate Earth Engine on your machine (developer step):

```bash
earthengine authenticate
```

3. Ensure the backend can read dataset configuration:

- `resources/sources.yaml` lists dataset URLs and EE image set IDs.
- **Do not commit new secrets**. If deploying, move credentials into secret storage.

## Run (development)

### Backend

From repo root:

```bash
uv run python -m backend
```

Expected:
- HTTP API is available locally.
- Endpoints for risk overlays and driver tiles respond with JSON.

### Frontend

From repo root:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Expected:
- Home page renders two Florida default risk overlays (last 30d and last 12mo).
- Form allows City/ZIP + date range selection.
- Drivers page shows 3 tiles (veg, temp, precip/standing water).

## Smoke Test

- Backend health:

```bash
curl -s http://127.0.0.1:8000/health
```

- Risk query (example):

```bash
curl -s -X POST http://127.0.0.1:8000/api/risk/query \
  -H 'content-type: application/json' \
  -d '{"location_text":"33101","date_range":{"start_date":"2025-01-01","end_date":"2025-02-01"}}'
```

- Drivers query (example):

```bash
curl -s -X POST http://127.0.0.1:8000/api/drivers \
  -H 'content-type: application/json' \
  -d '{"location_text":"33101","date_range":{"start_date":"2025-01-01","end_date":"2025-02-01"}}'
```

- UI:
  - Load `http://127.0.0.1:5173/` and verify 2 map overlays are visible.
  - Submit City/ZIP + date range: verify overlays refresh or show an actionable error.
  - Open drivers page: verify tiles render and mini-maps center on the queried location.
