from __future__ import annotations

from dataclasses import dataclass

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


def location_from_geocoding(id_: str, location_text: str, result: GeocodingResult) -> Location:
    return Location(
        id=id_,
        label=result.label or location_text,
        source=LocationSource.geocoded_text,
        geometry=result.geometry,
        bbox=result.bbox,
    )
