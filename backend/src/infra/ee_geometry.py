from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Viewport:
    center_lat: float
    center_lng: float
    radius_meters: float


def region_and_viewport_from_location(*, location_geometry: dict, location_bbox: tuple[float, float, float, float] | None):
    import ee  # type: ignore

    geom_type = location_geometry.get("type") if isinstance(location_geometry, dict) else None
    viewport: dict | None = None

    if geom_type == "Point":
        coords = location_geometry.get("coordinates")
        if (
            isinstance(coords, list)
            and len(coords) == 2
            and all(isinstance(x, (int, float)) for x in coords)
        ):
            lng = float(coords[0])
            lat = float(coords[1])
            radius_meters = 160_934.0
            region = ee.Geometry.Point([lng, lat]).buffer(radius_meters).bounds()
            viewport = {"center_lat": lat, "center_lng": lng, "radius_meters": radius_meters}
            return region, viewport

    region = ee.Geometry(location_geometry)

    if location_bbox is not None:
        minx, miny, maxx, maxy = location_bbox
        viewport = {
            "center_lat": (miny + maxy) / 2.0,
            "center_lng": (minx + maxx) / 2.0,
            "radius_meters": 160_934.0,
        }
        return region, viewport

    viewport = {"center_lat": 27.8, "center_lng": -81.7, "radius_meters": 160_934.0}
    return region, viewport
