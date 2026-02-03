# Feature Specification: Mosquito Risk Dashboard
 
**Feature Branch**: `001-mosquito-risk-dashboard`  
**Created**: 2026-02-02  
**Status**: Draft  
**Input**: User description: "Create a python application with frontend and backend. The application uses EDA to show mosquito risk for a given location and date range; as first feature, extract the data exploration and analysis methods from the jupyter notebooks which are under ./notebooks/ folder; modularize these methods so that these can be re-used in the backend service classes; as second feature, when the application runs, on the home page it should show two charts; one being the mosquito risk for a default location (state of florida) and first chart showing the risk overlayed on a map for last month (last 30 days) and second chart showing the risk overlayed on a map for last year (last 12 months); as third feature, on the top of the home page above these two charts, it should show form elements to select a location and date range; as fourth feature, provide a link to another page, which takes as input a location and shows three tiles; first tile should show vegetation cover changes over last two years; second tile showing temperature changes over last two years; third tile showing precipitation changes and standing water changes over last two years"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - View Default Mosquito Risk Maps (Priority: P1)
 
As a user, I can open the application home page and immediately see mosquito risk
overlaid on a map for Florida for two default time windows (last 30 days and last
12 months).
 
**Why this priority**: Provides immediate value and a working end-to-end experience
without requiring configuration.
 
**Independent Test**: Can be fully tested by loading the home page in a browser and
verifying that two map-based charts are rendered with labels indicating Florida and
the correct default time windows.
 
**Acceptance Scenarios**:
 
1. **Given** the application is running, **When** I load the home page, **Then** I
  see a map-based risk chart for Florida for the last 30 days.
2. **Given** the application is running, **When** I load the home page, **Then** I
  see a map-based risk chart for Florida for the last 12 months.

---

### User Story 2 - Explore Risk by Location and Date Range (Priority: P2)
 
As a user, I can choose a location and a date range on the home page and refresh
the displayed risk maps to match my selections.

When I enter a ZIP code, the application analyzes an area within a 100-mile
radius of that ZIP code.

The application also allows me to view mosquito risk alongside environmental
layers (land-surface temperature, land coverage, and precipitation) on the same
map panels.
 
**Why this priority**: Enables analysis beyond a single default view and makes the
application useful for other locations/time windows.
 
**Independent Test**: Can be tested by selecting a different location and date
range and verifying both charts update to match the selections. When using a ZIP
code, verify the map reflects the 100-mile analysis radius. Verify that mosquito
risk, land-surface temperature, land coverage, and precipitation layers are
available on both charts.
 
**Acceptance Scenarios**:
 
1. **Given** the home page is loaded, **When** I select a new location and submit,
  **Then** both charts update to show risk for the selected location.
2. **Given** the home page is loaded, **When** I select a custom date range and
  submit, **Then** both charts update to reflect the chosen date range.
3. **Given** the home page is loaded, **When** I enter a ZIP code and submit,
  **Then** the system analyzes and displays results for an area within a 100-mile
  radius of that ZIP code.
4. **Given** results are displayed for a location/date range, **When** I switch
  the visible overlay layer on either chart, **Then** I can view mosquito risk,
  land-surface temperature, land coverage, and precipitation for the same
  location/date range.

---

### User Story 3 - View Environmental Drivers (Priority: P3)
 
As a user, I can navigate to an “environmental drivers” page, provide a location,
and view three tiles summarizing changes over the last two years:
vegetation cover, temperature, and precipitation/standing water.
 
**Why this priority**: Provides explanatory context for why mosquito risk may
increase or decrease, improving trust and interpretability.
 
**Independent Test**: Can be tested by navigating to the page, entering a location,
and verifying three tiles render with the expected two-year window.
 
**Acceptance Scenarios**:
 
1. **Given** the application is running, **When** I open the environmental drivers
  page and enter a location, **Then** I see a vegetation cover change tile for the
  last two years.
2. **Given** the application is running, **When** I open the environmental drivers
  page and enter a location, **Then** I see a temperature change tile for the last
  two years.
3. **Given** the application is running, **When** I open the environmental drivers
  page and enter a location, **Then** I see a precipitation/standing water change
  tile for the last two years.

---

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when the user submits an invalid location (unknown name, malformed
  coordinates, unsupported region)?
- What happens when the user selects an invalid date range (end before start,
  range too long, or dates outside supported dataset coverage)?
- What happens when a valid request returns no data for the location/time window?
- How does the system behave when data sources are temporarily unavailable or time
  out?
- How are partial results handled (e.g., drivers available but risk not available)?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements
 
- **FR-001**: System MUST provide a home page that displays two mosquito risk map
  visualizations for the default location “Florida”.
- **FR-002**: System MUST default the two home page visualizations to the last
  30 days and last 12 months.
- **FR-003**: The home page MUST provide form controls to select a location and a
  date range.
- **FR-004**: When the user submits the home page form, the system MUST refresh the
  displayed risk visualizations to match the selected location and date range.
- **FR-005**: The system MUST provide navigation from the home page to an
  environmental drivers page.
- **FR-006**: The environmental drivers page MUST accept a location input.
- **FR-007**: The environmental drivers page MUST display three tiles for the given
  location showing changes over the last two years:
  - Vegetation cover changes
  - Temperature changes
  - Precipitation changes and standing water changes
- **FR-008**: The system MUST reuse a shared, modular set of data exploration and
  analysis methods originally derived from the project’s notebooks so that the same
  logic can be executed consistently for both interactive exploration and backend
  services.
- **FR-009**: The system MUST clearly communicate when inputs are invalid and when
  data is unavailable for a requested location/time window.
- **FR-010**: The system MUST represent mosquito risk as categorical bands
  (Low/Med/High) and explain how to interpret those bands.
- **FR-011**: The system MUST use a combination of:
  - Static datasets referenced in `resources/sources.yaml` (Geo-Emerge GitHub URLs),
    and
  - Google Earth Engine image sets referenced in `resources/sources.yaml` for map
    overlays.
  The system MUST treat Earth Engine credentials as secrets (do not expose in UI or
  logs).
- **FR-012**: The system MUST accept user-entered location text (city name and/or
  ZIP code) and resolve it to a geographic area for analysis.
  The system MUST still default the home page to the statewide Florida view when no
  user input is provided.
- **FR-013**: When the user enters a ZIP code (or a location that resolves to a
  point), the system MUST analyze an area within a 100-mile radius of that point.
  For locations that resolve to polygons (e.g., administrative boundaries), the
  system SHOULD analyze the polygon geometry directly.
- **FR-014**: The home page MUST allow the user to view, on each of the two map
  panels, mosquito risk alongside environmental layers for the same
  location/date range:
  - Land-surface temperature
  - Land coverage
  - Precipitation

### Key Entities *(include if feature involves data)*
 
- **Location**: A user-specified geographic area (name and/or geometry).
- **DateRange**: Start and end dates used to query or aggregate time-series data.
- **MosquitoRiskSurface**: Risk values associated with a location and date range,
  suitable for map overlay and summary.
- **EnvironmentalDriverSeries**: Time series or aggregated measures (vegetation,
  temperature, precipitation, standing water) for a location and time window.
- **EDA Method Set**: A named set of reusable exploration/analysis operations
  extracted from notebooks and executed consistently in the application.

## Clarifications

### Session 2026-02-02
 
 - Q: What does “mosquito risk” represent? → A: Categorical bands (Low/Med/High)
 - Q: What are the data sources for risk + drivers? → A: Static Geo-Emerge datasets
   from GitHub URLs + Google Earth Engine image sets configured in
   `resources/sources.yaml` (treat tokens as secrets)
 - Q: What location input format is supported in v1? → A: City/ZIP text input (default
   home page remains Florida statewide)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes
 
- **SC-001**: A user can load the home page and see two rendered risk map charts for
  Florida within 10 seconds on a typical developer laptop.
- **SC-002**: A user can submit a location/date range selection and see both charts
  refresh successfully (or show a clear error state) in under 15 seconds.
- **SC-003**: A user can navigate to the environmental drivers page and see three
  tiles rendered for a provided location within 15 seconds.
- **SC-004**: The application provides a clear explanation of what “mosquito risk”
  represents and how to interpret the map overlay (at least one visible
  explanation/legend in the UI).
