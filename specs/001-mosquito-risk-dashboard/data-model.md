# Data Model: Mosquito Risk Dashboard

**Branch**: `001-mosquito-risk-dashboard`
**Date**: 2026-02-02
**Spec**: `specs/001-mosquito-risk-dashboard/spec.md`

## Entities

### Location

Represents a user-requested geography.

- **id**: string (generated, stable for request scope)
- **label**: string (e.g., "Miami, FL" or "33301")
- **source**: enum
  - `default_state`
  - `geocoded_text`
- **geometry**: GeoJSON-like geometry (point/polygon) suitable for spatial operations
- **bbox**: optional bounding box for map viewport

### DateRange

- **start_date**: ISO date (YYYY-MM-DD)
- **end_date**: ISO date (YYYY-MM-DD)
- **preset**: optional enum
  - `last_30_days`
  - `last_12_months`
  - `last_24_months`

### RiskBand

- **code**: enum `low` | `medium` | `high`
- **label**: string
- **color**: string (hex or named color)

### RiskLayer

Map overlay for mosquito risk.

- **location**: Location
- **date_range**: DateRange
- **band_legend**: ordered list of RiskBand
- **tile_url_template**: string (XYZ tiles URL template)
- **attribution**: string

### EnvironmentalDriverTile

A single tile shown on the Drivers page.

- **driver_type**: enum
  - `vegetation`
  - `temperature`
  - `precipitation`
  - `standing_water`
- **location**: Location
- **date_range**: DateRange (expected: last 24 months)
- **summary**: string (human-readable)
- **metrics**: key/value mapping (numbers + units)
- **tile_url_template**: optional string (if map overlay needed)

### DatasetSource

Represents configured dataset inputs from `resources/sources.yaml`.

- **name**: string (e.g., `mosquito`, `countries`, `landcover`, `floridaboundaries`)
- **url**: string
- **kind**: enum `zip` | `geojson` | `other`
- **cache_path**: string (local)

## Validation Rules

- DateRange: `start_date <= end_date`.
- DateRange: end date cannot be in the future (unless explicitly supported).
- Location: geocoding failure must return a user-facing validation error.
- RiskLayer: must always include the 3-band legend.

## Notes on Boundaries

- Domain entities are framework-agnostic and should live under `backend/src/domain/`.
- Earth Engine objects (`ee.Image`, `ee.Geometry`) should be confined to infrastructure adapters under `backend/src/infra/`.
