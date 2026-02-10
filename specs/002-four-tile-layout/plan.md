# Implementation Plan: Four-Tile Map Layout

**Branch**: `002-four-tile-layout` | **Date**: 2026-02-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-four-tile-layout/spec.md`

## Summary

Replace the single map panel + layer dropdown on the Home page with a 2×2 grid
of four simultaneously visible map tiles (Mosquito Risk, Land Surface
Temperature, Vegetation/NDVI, Precipitation). Each tile has its own heading and
inline legend. All four tiles synchronize pan/zoom. The backend API is unchanged;
this is a **frontend-only** change.

## Technical Context

**Language/Version**: TypeScript 5.7+ (frontend), Python 3.12+ (backend — no changes)
**Primary Dependencies**: React 18.3+, Leaflet 1.9+, react-leaflet 4.2+, Vite 6.1+
**Storage**: N/A (no new storage; backend unchanged)
**Testing**: Manual browser verification; future Vitest/Playwright
**Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Home page with four tiles loads within 15 seconds on a developer laptop
**Constraints**: Each tile minimum 300 px height; responsive single-column below 768 px
**Scale/Scope**: 2 pages affected (Home, Query — same component); ~3 frontend files modified

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **1) Clean Architecture Boundaries** | ✅ PASS | No backend changes. Frontend change stays in presentation layer. |
| **2) Reproducible EDA Over Intuition** | ✅ N/A | No EDA changes. |
| **3) Tests for Non-Trivial Logic** | ✅ PASS | Viewport sync logic should have a test; otherwise minimal logic. |
| **4) Contract-Driven API** | ✅ PASS | No API contract changes; frontend consumes existing `layers` array. |
| **5) Observability, Safety, Simplicity** | ✅ PASS | Minimal change; per-tile error handling improves resilience. |
| **App & Data Standards** | ✅ N/A | No Python code changes. |
| **Dev Workflow & Quality Gates** | ✅ PASS | Small, aligned change; no unrelated refactors. |

**Gate result: PASS** — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-four-tile-layout/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (no new contracts — backend unchanged)
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── App.tsx                         # No change expected
│   ├── pages/
│   │   ├── Home.tsx                    # MODIFIED: replace single map + dropdown with 4-tile grid
│   │   └── Drivers.tsx                 # No change (already multi-tile)
│   ├── components/
│   │   ├── RiskMap.tsx                 # REVIEWED: may need viewport sync props
│   │   ├── LayerTile.tsx               # NEW: single tile component (map + heading + legend)
│   │   ├── FourTileGrid.tsx            # NEW: 2×2 grid container with viewport sync
│   │   ├── MultiLayerLegend.tsx        # REMOVED from Home usage (replaced by per-tile legends)
│   │   ├── RiskQueryForm.tsx           # No change
│   │   ├── RiskLegend.tsx              # No change (legacy)
│   │   ├── DriverTile.tsx              # No change
│   │   └── ErrorConsole.tsx            # No change
│   ├── services/
│   │   └── api.ts                      # MODIFIED: add `legend` to OverlayLayer type
│   └── styles.css                      # MODIFIED: add grid layout styles
└── tests/                              # Future: Vitest component tests
```

**Structure Decision**: Web application structure (existing). Two new components
(`LayerTile.tsx`, `FourTileGrid.tsx`) added to `frontend/src/components/`. The
existing `Home.tsx` page is refactored to use the new grid. Backend is untouched.

## Design Approach

### New Components

**`LayerTile` component:**
- Renders a single Leaflet map with an Earth Engine tile overlay
- Displays the layer `label` as a heading above the map
- Renders the layer's `legend` inline below the map (categorical or continuous)
- Map has minimum height of 300 px
- Accepts `center`/`zoom` props for synchronized viewport
- Fires `onViewportChange` callback when user pans/zooms

**`FourTileGrid` component:**
- Renders a CSS Grid of `LayerTile` components (2 columns on wide viewports,
  1 column below 768 px)
- Manages shared viewport state (`center`, `zoom`) — lifts state up
- When any tile fires `onViewportChange`, updates all tiles
- Accepts the `layers` array from the API response and renders one `LayerTile`
  per entry
- Shows loading placeholders while data is being fetched

### Viewport Synchronization Strategy

- `FourTileGrid` holds `center: [lat, lng]` and `zoom: number` in React state
- Each `LayerTile` receives these as props and uses Leaflet's `setView` or
  the `useMap()` hook to stay in sync
- When user interacts with any map, that map's `moveend`/`zoomend` event
  fires `onViewportChange(newCenter, newZoom)` up to the grid
- Grid updates state → all tiles re-render with new viewport
- Guard against infinite update loops by comparing previous vs new viewport
  values before propagating

### API Type Fix

- Add `legend?: LayerLegend` to the `OverlayLayer` TypeScript type in
  `frontend/src/services/api.ts` to match what the backend already returns

## Complexity Tracking

> No constitution violations — this section is intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
