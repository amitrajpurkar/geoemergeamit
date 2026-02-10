# API Contracts: Four-Tile Map Layout

**Feature**: 002-four-tile-layout  
**Date**: 2026-02-10

## No New API Contracts

This feature is **frontend-only**. The backend API endpoints and response schemas
are unchanged. The frontend consumes the existing contracts documented below.

## Existing Contracts (consumed, not modified)

### GET /api/risk/default

Returns default risk data for ZIP 33172, date range 2023-01-01 to 2024-12-31.

**Response** (`RiskLayerResponseSchema`):
```json
{
  "location_label": "string",
  "date_range": { "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD" },
  "tile_url_template": "string (XYZ tile URL — risk layer)",
  "attribution": "string | null",
  "legend": [
    { "code": "low|medium|high", "label": "string", "color": "#hex" }
  ],
  "layers": [
    {
      "layer_id": "string",
      "label": "string",
      "tile_url_template": "string (XYZ tile URL)",
      "attribution": "string | null",
      "legend": {
        "type": "categorical | continuous",
        "min": 0,
        "max": 2,
        "palette": ["#hex", "..."],
        "unit": "string | null",
        "categories": [
          { "value": 0, "label": "Low", "color": "#2E7D32" }
        ]
      }
    }
  ],
  "viewport": {
    "center_lat": 0.0,
    "center_lng": 0.0,
    "radius_meters": 160934.0
  }
}
```

**Frontend change**: The `layers[].legend` field is already returned by the
backend but was missing from the `OverlayLayer` TypeScript type. This feature
adds `legend?: LayerLegend` to the TS type to align with the actual response.

### POST /api/risk/query

Same response schema as above, for a user-specified location and date range.

**Request body** (`RiskQueryRequestSchema`):
```json
{
  "location_text": "string (max 200 chars)",
  "date_range": { "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD" }
}
```

### POST /api/drivers

Not affected by this feature (Drivers page is out of scope).
