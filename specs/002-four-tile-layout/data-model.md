# Data Model: Four-Tile Map Layout

**Feature**: 002-four-tile-layout  
**Date**: 2026-02-10

## Overview

This feature introduces no new backend entities or API changes. The data model
below documents the **existing** frontend types that are consumed and the **new**
component prop interfaces introduced by this feature.

## Existing Entities (unchanged)

### OverlayLayer (backend → frontend)

Returned by `GET /api/risk/default` and `POST /api/risk/query` in the `layers`
array.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `layer_id` | string | yes | Unique identifier (e.g., `risk`, `land_surface_temperature`) |
| `label` | string | yes | Human-readable layer name |
| `tile_url_template` | string | yes | XYZ tile URL template for Leaflet |
| `attribution` | string | no | Data source attribution text |
| `legend` | LayerLegend | no | Legend metadata (categorical or continuous) |

### LayerLegend

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `"categorical"` \| `"continuous"` | yes | Legend rendering mode |
| `min` | number | yes | Minimum value on scale |
| `max` | number | yes | Maximum value on scale |
| `palette` | string[] | yes | Ordered list of CSS colour strings |
| `unit` | string | no | Unit label (e.g., `°C`, `mm`, `NDVI`) |
| `categories` | LegendCategory[] | no | Only for categorical legends |

### LegendCategory

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | number | yes | Numeric value (e.g., 0, 1, 2) |
| `label` | string | yes | Human-readable label (e.g., `Low`, `Medium`, `High`) |
| `color` | string | yes | CSS colour for this category |

### Viewport

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `center_lat` | number | yes | Latitude of viewport center |
| `center_lng` | number | yes | Longitude of viewport center |
| `radius_meters` | number | yes | Analysis radius |

## New Frontend Interfaces (this feature)

### LayerTileProps

Props for the new `LayerTile` component.

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `layer` | OverlayLayer | yes | Layer data including tile URL and legend |
| `center` | [number, number] | yes | Shared viewport center [lat, lng] |
| `zoom` | number | yes | Shared viewport zoom level |
| `radius` | number | no | Analysis radius for circle overlay |
| `onViewportChange` | (center: [number, number], zoom: number) => void | yes | Callback when user pans/zooms this tile |

### FourTileGridProps

Props for the new `FourTileGrid` component.

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `layers` | OverlayLayer[] | yes | Array of layers to render (one tile per entry) |
| `viewport` | Viewport \| null | no | Initial viewport from API response |
| `loading` | boolean | no | Whether data is currently loading |

### Viewport State (internal to FourTileGrid)

| State | Type | Initial Value | Description |
|-------|------|---------------|-------------|
| `center` | [number, number] | From `viewport` prop or `[27.8, -81.7]` | Shared map center |
| `zoom` | number | `8` (if viewport provided) or `6` | Shared zoom level |

## Relationships

```
RiskLayerResponse
  ├── layers: OverlayLayer[]  ──→  FourTileGrid.layers
  │     └── legend: LayerLegend  ──→  LayerTile inline legend
  └── viewport: Viewport  ──→  FourTileGrid initial center/zoom
```

## Validation Rules

- `layers` array may contain 0–4 entries; render one tile per entry.
- If `layers` is empty, show an informational message instead of the grid.
- Each `layer.tile_url_template` must be a valid URL template with `{z}`, `{x}`,
  `{y}` placeholders.
- `legend` is optional per layer; if absent, the tile renders without a legend.
