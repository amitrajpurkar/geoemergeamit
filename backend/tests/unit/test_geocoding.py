from __future__ import annotations

import pytest

from backend.src.domain.errors import InvalidLocationError
from backend.src.infra.geocoding import (
    CachedGeocoder,
    GeocodingResult,
    NominatimGeocoder,
    StubGeocoder,
    default_geocoder,
    location_from_geocoding,
)


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


def test_cached_geocoder_returns_cached(monkeypatch) -> None:
    calls = {"n": 0}

    class _Inner:
        def geocode(self, _t: str) -> GeocodingResult:
            calls["n"] += 1
            return GeocodingResult(label="x", geometry={"type": "Point", "coordinates": [0, 0]})

    cg = CachedGeocoder(_Inner(), ttl_seconds=3600)
    cg.geocode("Miami")
    cg.geocode("Miami")
    assert calls["n"] == 1


def test_nominatim_retries_on_429(monkeypatch) -> None:
    import httpx

    class _Resp:
        def __init__(self, status_code: int, payload: dict):
            self.status_code = status_code
            self._payload = payload
            self.request = httpx.Request("GET", "https://example.com")

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError("err", request=self.request, response=self)

        def json(self):
            return self._payload

    seq = [
        _Resp(429, {}),
        _Resp(200, {"features": [{"geometry": {"type": "Point", "coordinates": [0, 0]}, "properties": {"display_name": "ok"}}]}),
    ]

    def _fake_get(*_a, **_kw):
        return seq.pop(0)

    sleeps: list[float] = []
    monkeypatch.setattr("backend.src.infra.geocoding.httpx.get", _fake_get)
    monkeypatch.setattr("backend.src.infra.geocoding.time.sleep", lambda s: sleeps.append(s))

    geo = NominatimGeocoder()
    res = geo.geocode("33101")
    assert res.label == "ok"
    assert sleeps
