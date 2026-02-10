# Tasks: Four-Tile Map Layout

**Input**: Design documents from `/specs/002-four-tile-layout/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No automated tests explicitly requested. Manual browser verification per quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: TypeScript type alignment and CSS foundation needed before any component work

- [x] T001 Add `LayerLegend` and `LegendCategory` types and add `legend?: LayerLegend` to `OverlayLayer` type in frontend/src/services/api.ts
- [x] T002 [P] Add `.four-tile-grid` responsive CSS Grid styles (2-column default, 1-column below 768 px) in frontend/src/styles.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: New shared components that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create `LayerLegend` component that renders a single legend (categorical with colour boxes or continuous with gradient bar) in frontend/src/components/LayerLegend.tsx
- [x] T004 Create `LayerTile` component that renders a Leaflet map with heading, Earth Engine tile overlay, optional analysis-radius circle, and inline `LayerLegend`; accepts `center`/`zoom`/`onViewportChange` props for viewport sync in frontend/src/components/LayerTile.tsx
- [x] T005 Create `FourTileGrid` component that manages shared viewport state (`center`, `zoom`), renders one `LayerTile` per entry in a `layers` array using CSS Grid, synchronizes pan/zoom across all tiles via lifted state, and shows loading placeholders in frontend/src/components/FourTileGrid.tsx

**Checkpoint**: Foundation ready — new components exist and can be imported. User story implementation can now begin.

---

## Phase 3: User Story 1 — View Four Default Tiles on Home Page (Priority: P1) 🎯 MVP

**Goal**: Replace the single map panel + layer dropdown on the Home page with four simultaneously visible, labelled map tiles for the default location (ZIP 33172, 2023-01-01 to 2024-12-31).

**Independent Test**: Load the home page in a browser → verify four labelled map tiles in a 2×2 grid, no dropdown, each rendering a distinct overlay for the default ZIP and date range.

### Implementation for User Story 1

- [x] T006 [US1] Refactor `Home.tsx` to replace the single `<RiskMap>` + layer `<select>` dropdown + `<MultiLayerLegend>` with a single `<FourTileGrid>` that receives `riskData.layers` and `riskData.viewport` in frontend/src/pages/Home.tsx
- [x] T007 [US1] Remove the `layerId` state variable and the `pickLayer` helper function that are no longer needed after dropdown removal in frontend/src/pages/Home.tsx
- [x] T008 [US1] Verify default view renders four tiles by starting backend (`uv run python -m backend`) and frontend (`npm run dev`) and loading http://127.0.0.1:5173 — confirm 2×2 grid, labelled tiles, no dropdown, correct overlays for ZIP 33172

**Checkpoint**: User Story 1 is complete — Home page shows four default tiles. This is the MVP.

---

## Phase 4: User Story 2 — Query and View Four Tiles for a Custom Location (Priority: P2)

**Goal**: When the user submits a custom location and date range via the query form, all four tiles update to show data for the new query.

**Independent Test**: Enter a different ZIP code (e.g., 90210) and date range, submit → verify all four tiles update with new overlays and the heading reflects the queried location/date range.

### Implementation for User Story 2

- [x] T009 [US2] Verify `onQuery` handler in `Home.tsx` correctly passes updated `riskData` (including new `layers` and `viewport`) to `FourTileGrid` after a successful query response in frontend/src/pages/Home.tsx
- [x] T010 [US2] Ensure `FourTileGrid` resets its internal viewport state (`center`, `zoom`) when the `viewport` prop changes (new query result) so tiles re-center on the new location in frontend/src/components/FourTileGrid.tsx
- [x] T011 [US2] Ensure all four tiles show a loading indicator simultaneously while a query is in progress (pass `loading` prop to `FourTileGrid`) in frontend/src/pages/Home.tsx and frontend/src/components/FourTileGrid.tsx
- [x] T012 [US2] Manually test: enter ZIP 90210 with date range 2023-06-01 to 2024-06-01, submit, confirm all four tiles update and heading reflects query

**Checkpoint**: User Stories 1 AND 2 are complete — default and custom queries both render four tiles.

---

## Phase 5: User Story 3 — Per-Tile Legends (Priority: P3)

**Goal**: Each tile displays its own legend inline (below the map), replacing the old shared `MultiLayerLegend` panel on the Home page. Legend content (colours, labels, units) is identical to current implementation.

**Independent Test**: Load Home page → verify each tile has its own legend beneath the map; Risk shows categorical Low/Medium/High; LST/NDVI/Precipitation show continuous gradients with units; no shared legend panel above the grid.

### Implementation for User Story 3

- [x] T013 [US3] Confirm `MultiLayerLegend` import and usage is removed from `Home.tsx` (should already be done in T006; verify no residual rendering) in frontend/src/pages/Home.tsx
- [x] T014 [US3] Verify `LayerLegend` renders correctly for all four legend types by inspecting each tile in the browser: Risk (categorical with 3 colour boxes), LST (continuous °C), NDVI (continuous 0–1), Precipitation (continuous mm)
- [x] T015 [US3] Confirm `MultiLayerLegend` is still used on the Drivers page (`Drivers.tsx`) and is NOT affected by this feature in frontend/src/pages/Drivers.tsx

**Checkpoint**: All three user stories are complete — four tiles with per-tile legends, synced viewports, working for default and custom queries.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, responsiveness, and cleanup

- [x] T016 [P] Verify responsive layout: narrow browser to < 768 px and confirm tiles reflow to single column, each tile remains scrollable and legible
- [x] T017 [P] Verify per-tile error handling: if one tile overlay fails to load (e.g., simulate by temporarily breaking one tile URL), confirm the other three tiles still render
- [x] T018 [P] Verify Drivers page is completely unchanged: navigate to Environmental Drivers and confirm existing multi-tile layout and legends work as before
- [x] T019 Verify viewport sync loop guard: rapidly pan/zoom a tile and confirm no infinite re-render or jank (check browser console for errors)
- [x] T020 Run full quickstart.md validation (all 5 verification steps) as a final acceptance check
- [x] T021 [P] Remove any dead code: if `RiskMap.tsx` is no longer imported anywhere, consider keeping it (used by other features) or marking as legacy in a comment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on T001 (TS types) — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion
- **User Story 2 (Phase 4)**: Depends on Phase 3 (US1 provides the refactored Home.tsx that US2 builds on)
- **User Story 3 (Phase 5)**: Depends on Phase 3 (legend integration is part of LayerTile created in Phase 2, verified in US3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 — no dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 (needs refactored Home.tsx with FourTileGrid)
- **User Story 3 (P3)**: Can start after Phase 2 in parallel with US2 (legend is built into LayerTile; US3 is verification-focused)

### Within Each User Story

- Implementation tasks are sequential within each story
- Verification tasks are the final step of each story

### Parallel Opportunities

- T001 and T002 can run in parallel (Phase 1)
- T003 and T004 are sequential (T004 uses T003), but T005 depends on T004
- US2 (Phase 4) and US3 (Phase 5) can run in parallel after US1 is complete
- All Phase 6 tasks marked [P] can run in parallel

---

## Parallel Example: Phase 1

```bash
# Launch both setup tasks in parallel (different files):
Task T001: "Add legend types to OverlayLayer in frontend/src/services/api.ts"
Task T002: "Add .four-tile-grid CSS Grid styles in frontend/src/styles.css"
```

## Parallel Example: Phase 6

```bash
# Launch all verification tasks in parallel:
Task T016: "Verify responsive layout"
Task T017: "Verify per-tile error handling"
Task T018: "Verify Drivers page unchanged"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T005)
3. Complete Phase 3: User Story 1 (T006–T008)
4. **STOP and VALIDATE**: Load home page, verify four tiles, no dropdown
5. Demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Four default tiles visible (MVP!)
3. Add User Story 2 → Custom queries update all tiles
4. Add User Story 3 → Per-tile legends verified
5. Polish → Responsive, error handling, cleanup
6. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- This is a **frontend-only** feature — no backend changes
- New components: `LayerLegend`, `LayerTile`, `FourTileGrid`
- Modified files: `Home.tsx`, `api.ts`, `styles.css`
- Unchanged: `Drivers.tsx`, `DriverTile.tsx`, `RiskQueryForm.tsx`, `ErrorConsole.tsx`, all backend code
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
