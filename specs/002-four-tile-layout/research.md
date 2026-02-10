# Research: Four-Tile Map Layout

**Feature**: 002-four-tile-layout  
**Date**: 2026-02-10

## Research Topics

### 1. Leaflet Viewport Synchronization in react-leaflet

**Decision**: Use lifted React state (`center`, `zoom`) in a parent grid component,
passed as props to each tile. Each tile uses `useMap()` + `useMapEvents()` to
detect user interaction and propagate viewport changes upward.

**Rationale**:
- `react-leaflet` 4.x provides `useMap()` for imperative map control and
  `useMapEvents()` for event listening — both are stable, well-documented APIs.
- Lifting viewport state to the grid parent is the idiomatic React pattern
  (single source of truth, unidirectional data flow).
- Alternative approaches (e.g., direct Leaflet-to-Leaflet event wiring outside
  React) break React's rendering model and are harder to debug.

**Alternatives considered**:
- **leaflet-sync plugin**: Provides native Leaflet map synchronization, but it
  is not maintained for react-leaflet 4.x and requires direct DOM access that
  conflicts with React's virtual DOM.
- **Shared ref approach**: Store a single Leaflet map ref and mirror events.
  Rejected because it couples components tightly and is fragile across
  re-renders.

**Implementation pattern**:
```tsx
// In FourTileGrid (parent):
const [center, setCenter] = useState<[number, number]>(initialCenter)
const [zoom, setZoom] = useState(initialZoom)

function onViewportChange(newCenter: [number, number], newZoom: number) {
  setCenter(newCenter)
  setZoom(newZoom)
}

// In LayerTile (child) — inner component using useMap():
function ViewportSync({ center, zoom, onViewportChange }) {
  const map = useMap()
  
  // Sync from parent state → map
  useEffect(() => {
    const currentCenter = map.getCenter()
    const currentZoom = map.getZoom()
    if (currentCenter.lat !== center[0] || currentCenter.lng !== center[1] || currentZoom !== zoom) {
      map.setView(center, zoom, { animate: false })
    }
  }, [map, center, zoom])

  // Sync from map interaction → parent
  useMapEvents({
    moveend: () => {
      const c = map.getCenter()
      onViewportChange([c.lat, c.lng], map.getZoom())
    }
  })
  return null
}
```

**Loop guard**: Compare previous vs new center/zoom before calling `setView` to
prevent infinite re-render cycles. Use `{ animate: false }` on programmatic
`setView` to avoid animation jank when syncing.

---

### 2. CSS Grid Responsive Layout (2×2 → 1×4)

**Decision**: Use CSS Grid with `grid-template-columns: repeat(2, 1fr)` and a
`@media (max-width: 768px)` breakpoint that switches to `grid-template-columns: 1fr`.

**Rationale**:
- CSS Grid is natively supported in all target browsers.
- No additional library needed (the project uses plain CSS, not Tailwind).
- The existing `styles.css` already uses grid for the Drivers page `.grid` class.

**Alternatives considered**:
- **Flexbox wrap**: Works but requires more manual sizing rules for equal-width
  tiles. Grid is cleaner for a fixed 2×2 layout.
- **CSS Container Queries**: More modern but unnecessary for a simple breakpoint.

---

### 3. Per-Tile Legend Rendering

**Decision**: Reuse the legend rendering logic from `MultiLayerLegend.tsx` inside
the new `LayerTile` component. Extract the single-legend rendering into a helper
or simply inline it (the logic is ~30 lines).

**Rationale**:
- The existing `MultiLayerLegend` iterates over layers and renders each legend.
  The per-tile approach just renders one legend per tile instead of all in a loop.
- No new legend logic needed; only the layout changes.

**Alternatives considered**:
- **Keep MultiLayerLegend and render one per tile**: Possible but awkward — the
  component name implies "multi" and it would receive a single-element array.
- **Create a new `SingleLayerLegend` component**: Cleanest option if we want
  reusability. The existing categorical/continuous rendering logic can be
  extracted into this component, and `MultiLayerLegend` can optionally be
  refactored to use it (or left as-is for Drivers page).

**Decision**: Create a `LayerLegend` component that renders a single legend
(categorical or continuous). Use it inside `LayerTile`. Leave `MultiLayerLegend`
intact for the Drivers page.

---

### 4. TypeScript Type Alignment

**Decision**: Add `legend?: LayerLegend` to the `OverlayLayer` type in
`frontend/src/services/api.ts`.

**Rationale**:
- The backend already returns `legend` on each layer object.
- The current TS type omits it, which means the frontend silently drops the
  field (structural typing allows it at runtime but the type is incomplete).
- Adding it aligns the type with the actual API response.

---

## Summary

No external research or new dependencies required. All decisions use existing
libraries (react-leaflet 4.x, CSS Grid) and idiomatic React patterns. The only
new components are `LayerTile`, `FourTileGrid`, and `LayerLegend`.
