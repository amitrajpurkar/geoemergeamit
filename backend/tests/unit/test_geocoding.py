from __future__ import annotations

import pytest

from backend.src.domain.errors import InvalidLocationError
from backend.src.infra.geocoding import GeocodingResult, StubGeocoder, default_geocoder, location_from_geocoding


def test_stub_geocoder_raises() -> None:
    with pytest.raises(InvalidLocationError):
        StubGeocoder().geocode("Miami")


def test_location_from_geocoding_label_fallback() -> None:
    loc = location_from_geocoding(
        "id1",
        "input",
        GeocodingResult(label="", geometry={"type": "Point", "coordinates": [0, 0]}),
    )
    assert loc.label == "input"


def test_default_geocoder_exists() -> None:
    assert default_geocoder() is not None
