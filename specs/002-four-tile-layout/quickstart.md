# Quickstart: Four-Tile Map Layout

**Feature**: 002-four-tile-layout  
**Date**: 2026-02-10

## Prerequisites

- Node.js 18+ and npm installed
- Python 3.12+ with `uv` installed (backend — no changes needed, but required to run)
- Earth Engine credentials configured (`resources/ee-service-account.json` or
  `earthengine authenticate` locally)

## Setup

```bash
# 1. Switch to the feature branch
git checkout 002-four-tile-layout

# 2. Install frontend dependencies (if not already)
cd frontend && npm install && cd ..

# 3. Start the backend (no changes, but needed for API)
uv run python -m backend
# Backend runs at http://127.0.0.1:8000

# 4. In a separate terminal, start the frontend dev server
cd frontend && npm run dev
# Frontend runs at http://127.0.0.1:5173
```

## Verification

1. Open `http://127.0.0.1:5173` in a browser
2. **Home page** should display:
   - A query form (location + date range)
   - Four map tiles in a 2×2 grid, each labelled:
     - Mosquito Risk
     - Land Surface Temperature
     - Vegetation (NDVI)
     - Precipitation
   - Each tile has its own legend below/beside the map
   - Panning or zooming any tile updates all four
3. **Query**: Enter a ZIP code (e.g., `90210`) and a date range, submit
   - All four tiles should update with new overlays
4. **Responsive**: Narrow the browser to < 768 px width
   - Tiles should stack into a single column
5. **Drivers page**: Click "View environmental drivers"
   - Should be unchanged from current behaviour

## Files Changed (expected)

| File | Change |
|------|--------|
| `frontend/src/pages/Home.tsx` | Replace single map + dropdown with `FourTileGrid` |
| `frontend/src/components/FourTileGrid.tsx` | **NEW** — 2×2 grid with viewport sync |
| `frontend/src/components/LayerTile.tsx` | **NEW** — single tile (map + heading + legend) |
| `frontend/src/components/LayerLegend.tsx` | **NEW** — single-legend renderer |
| `frontend/src/services/api.ts` | Add `legend` to `OverlayLayer` type |
| `frontend/src/styles.css` | Add `.four-tile-grid` responsive styles |

## No Backend Changes

The backend API is unchanged. All four overlay layers are already returned in the
`layers` array of `/api/risk/default` and `/api/risk/query`.
