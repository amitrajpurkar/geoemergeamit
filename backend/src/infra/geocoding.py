from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from backend.src.domain.errors import InvalidLocationError
from backend.src.domain.models import Location, LocationSource


@dataclass(frozen=True)
class GeocodingResult:
    label: str
    geometry: dict
    bbox: tuple[float, float, float, float] | None = None


class Geocoder:
    def geocode(self, location_text: str) -> GeocodingResult:
        raise NotImplementedError


class StubGeocoder(Geocoder):
    def geocode(self, location_text: str) -> GeocodingResult:
        raise InvalidLocationError(
            "Geocoding is not configured yet. Provide a geocoding provider in a later phase."
        )


class NominatimGeocoder(Geocoder):
    def geocode(self, location_text: str) -> GeocodingResult:
        if not location_text.strip():
            raise InvalidLocationError("Location text is required")

        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location_text, "format": "geojson", "limit": 1}
        headers = {"User-Agent": "geoemerge/0.1 (local dev)"}

        try:
            resp = httpx.get(url, params=params, headers=headers, timeout=10.0)
            resp.raise_for_status()
        except Exception as e:
            raise InvalidLocationError("Failed to geocode location") from e

        data: Any
        try:
            data = resp.json()
        except Exception as e:
            raise InvalidLocationError("Geocoding response was not valid JSON") from e

        features = data.get("features") if isinstance(data, dict) else None
        if not isinstance(features, list) or not features:
            raise InvalidLocationError("Location not found")

        f0 = features[0]
        if not isinstance(f0, dict):
            raise InvalidLocationError("Location not found")

        geometry = f0.get("geometry")
        if not isinstance(geometry, dict):
            raise InvalidLocationError("Geocoding result is missing geometry")

        props = f0.get("properties") if isinstance(f0.get("properties"), dict) else {}
        label = props.get("display_name") if isinstance(props.get("display_name"), str) else location_text

        bbox_val = f0.get("bbox")
        bbox: tuple[float, float, float, float] | None = None
        if isinstance(bbox_val, list) and len(bbox_val) == 4 and all(isinstance(x, (int, float)) for x in bbox_val):
            bbox = (float(bbox_val[0]), float(bbox_val[1]), float(bbox_val[2]), float(bbox_val[3]))

        return GeocodingResult(label=label, geometry=geometry, bbox=bbox)


def default_geocoder() -> Geocoder:
    return NominatimGeocoder()


def location_from_geocoding(id_: str, location_text: str, result: GeocodingResult) -> Location:
    return Location(
        id=id_,
        label=result.label or location_text,
        source=LocationSource.geocoded_text,
        geometry=result.geometry,
        bbox=result.bbox,
    )
