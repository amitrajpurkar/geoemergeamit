# Feature Specification: Four-Tile Map Layout

**Feature Branch**: `002-four-tile-layout`  
**Created**: 2026-02-10  
**Status**: Clarified  
**Input**: User description: "On both the home page and query page, replace the single tile with layer dropdown with four separate tiles, one for each layer (mosquito risk, land-surface-temperature, land-coverage, precipitation). Remove the dropdowns and label each tile. Keep existing legends. Application continues to work with default or user-supplied zip code."

## Context

The current application displays a single map panel with a dropdown selector that
lets the user switch between four overlay layers (Mosquito Risk, Land Surface
Temperature, Vegetation/NDVI, Precipitation). This feature replaces that single
map + dropdown pattern with four simultaneously visible map tiles arranged in a
grid, one per layer. Each tile is clearly labelled so the user can compare all
layers at a glance without toggling.

**What stays the same:**
- Default location (ZIP 33172) and date range (2023-01-01 to 2024-12-31)
- Query form allowing a user to supply a different location and date range
- Navigation to the Environmental Drivers page
- All existing legend components (categorical for Risk, continuous for the other three)
- Backend API contracts (no endpoint changes required)
- Error console behaviour

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Four Default Tiles on Home Page (Priority: P1)

As a user, I can open the home page and immediately see four map tiles arranged
in a grid, each showing a different environmental layer for the default location
(ZIP 33172) and date range (2023-01-01 to 2024-12-31):

1. Mosquito Risk
2. Land Surface Temperature
3. Vegetation / Land Coverage (NDVI)
4. Precipitation

Each tile is clearly labelled with the layer name; no dropdown selector is
present.

**Why this priority**: This is the core visual change and delivers the primary
value of simultaneous multi-layer comparison on the default view.

**Independent Test**: Load the home page in a browser and verify that four map
tiles are visible, each labelled, each rendering a distinct overlay for the
default ZIP and date range.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** I load the home page, **Then**
   I see four map tiles arranged in a 2x2 grid (or responsive equivalent).
2. **Given** the home page has loaded, **When** I inspect the tiles, **Then**
   each tile displays its layer name as a visible heading (Mosquito Risk, Land
   Surface Temperature, Vegetation (NDVI), Precipitation).
3. **Given** the home page has loaded, **When** I look at the page, **Then**
   there is no dropdown selector for choosing a layer.
4. **Given** the home page has loaded, **When** I inspect each tile, **Then**
   each tile renders its own Earth Engine overlay for ZIP 33172 and date range
   2023-01-01 to 2024-12-31.

---

### User Story 2 - Query and View Four Tiles for a Custom Location (Priority: P2)

As a user, I can enter a location and date range in the query form on the home
page, submit it, and see all four tiles update to display data for my chosen
location and date range.

**Why this priority**: Extends the core layout change to the interactive query
flow, making the feature complete for custom analysis.

**Independent Test**: Enter a different ZIP code (e.g., 90210) and a custom date
range, submit the form, and verify that all four tiles update to reflect the new
location and date range.

**Acceptance Scenarios**:

1. **Given** the home page is loaded, **When** I enter a new location and date
   range and submit, **Then** all four tiles update to show data for the new
   location and date range.
2. **Given** a query has been submitted, **When** the response returns
   successfully, **Then** the page title / heading reflects the queried location
   and date range.
3. **Given** a query is in progress, **When** the data is loading, **Then** all
   four tiles show a loading indicator simultaneously.

---

### User Story 3 - Legends Remain Visible Alongside the Four Tiles (Priority: P3)

As a user, I can see the existing multi-layer legend panel displayed alongside
the four tiles so that I can interpret the colour scales for every layer without
additional interaction.

**Why this priority**: Legends are already implemented; this story ensures they
are not inadvertently removed or broken by the layout change.

**Independent Test**: Load the home page and verify that the legend panel still
displays all four legends (categorical for Risk; continuous for LST, NDVI,
Precipitation) with correct colours, labels, and units.

**Acceptance Scenarios**:

1. **Given** the home page has loaded with four tiles, **When** I look at any
   tile, **Then** I see its legend displayed directly below or beside its map.
2. **Given** the legends are displayed, **When** I inspect them, **Then** the
   Risk tile shows categorical Low/Medium/High with colour boxes and the other
   three tiles show continuous gradient bars with min/max values and units.
3. **Given** the home page has loaded, **When** I look for the old shared legend
   panel above the grid, **Then** it is no longer present (replaced by per-tile
   legends).

---

### Edge Cases

- What happens when one or more tile URLs fail to load (e.g., Earth Engine
  timeout for one layer but not others)?
  - Each tile SHOULD display an individual error state without affecting the
    other three tiles.
- What happens on small screens / mobile viewports?
  - Tiles SHOULD stack vertically (single column) on narrow viewports to remain
    usable.
- What happens when the backend returns fewer than four layers?
  - The system SHOULD render only the tiles for which data is available and
    display a message for missing layers.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The home page MUST display four separate map tiles arranged in a
  grid layout, one for each of the following layers: Mosquito Risk, Land Surface
  Temperature, Vegetation (NDVI), and Precipitation.
- **FR-002**: Each map tile MUST display a visible heading that identifies the
  layer it represents.
- **FR-003**: The layer-selection dropdown MUST be removed from the home page.
- **FR-004**: When the user submits a query (location + date range), all four
  tiles MUST update to show data for the queried location and date range.
- **FR-005**: The default view MUST continue to use ZIP code 33172 and date range
  2023-01-01 to 2024-12-31, rendering all four tiles for that default.
- **FR-006**: Each map tile MUST display its own legend directly below or beside
  its map, replacing the current shared legend panel. The legend content (colour
  scales, labels, and units) MUST remain identical to the current implementation.
- **FR-007**: The four-tile grid MUST be responsive: on viewports narrower than a
  reasonable breakpoint the tiles SHOULD reflow to a single column.
- **FR-008**: Each tile MUST independently handle overlay loading errors so that
  a failure in one tile does not prevent the other three from rendering.
- **FR-009**: No changes are required to the backend API endpoints or response
  schemas; the frontend MUST consume the existing `layers` array from the risk
  API response and render one tile per layer entry.
- **FR-010**: The Environmental Drivers page layout is NOT changed by this
  feature; it already displays separate tiles per driver.
- **FR-011**: All four map tiles MUST synchronize their viewport — panning or
  zooming any one tile MUST update the other three to the same center and zoom
  level.
- **FR-012**: Each map tile MUST have a minimum height of 300 px to ensure
  overlays remain legible and interactive.

### Assumptions

- The backend already returns all four layers in the `layers` array of the
  `/api/risk/default` and `/api/risk/query` responses. No backend changes are
  needed.
- The Environmental Drivers page already uses a multi-tile layout and is
  excluded from this feature's scope.

### Key Entities *(include if feature involves data)*

- **OverlayLayer**: An individual map layer with `layer_id`, `label`,
  `tile_url_template`, `attribution`, and `legend` metadata. The frontend
  renders one tile per OverlayLayer.

## Clarifications

### Session 2026-02-10

- Q: Should all four map tiles synchronize pan/zoom (so panning one updates all)? → A: Yes, synchronized — panning or zooming any tile updates all four to the same viewport.
- Q: Should legends be a shared panel or per-tile? → A: Per-tile — each tile displays its own legend directly below or beside its map, replacing the shared legend panel.
- Q: What minimum height should each map tile have? → A: 300 px — larger than the Drivers page tiles (240 px), better readability for the primary analysis view.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user loading the home page sees four labelled map tiles (not a
  single map with a dropdown) within the same performance envelope as today
  (under 15 seconds on a typical developer laptop).
- **SC-002**: A user submitting a custom query sees all four tiles update
  successfully (or show clear error states) within 15 seconds.
- **SC-003**: The legend panel displays all four layer legends with correct
  colour scales, matching the current behaviour, without any user interaction
  required.
- **SC-004**: On a viewport narrower than 768 px the tiles reflow to a single
  column and remain scrollable and legible.
