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
# placeholder: frontend bootstrapping will be defined in implementation
```

Expected:
- Home page renders two Florida default risk overlays (last 30d and last 12mo).
- Form allows City/ZIP + date range selection.
- Drivers page shows 3 tiles (veg, temp, precip/standing water).

## Smoke Test

- Load home page: verify 2 map overlays are visible.
- Submit City/ZIP + date range: verify overlays refresh or show an actionable error.
- Open drivers page: verify 3 tiles render for given location.
