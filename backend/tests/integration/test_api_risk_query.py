from __future__ import annotations

from datetime import date, timedelta

from fastapi.testclient import TestClient

from backend.src.api.app import create_app


class _FakeGeocoder:
    def geocode(self, location_text: str):
        _ = location_text
        return type(
            "_Result",
            (),
            {
                "label": "Miami, FL",
                "geometry": {"type": "Point", "coordinates": [-80.1918, 25.7617]},
                "bbox": None,
            },
        )()


def test_post_risk_query_shape(monkeypatch) -> None:
    import backend.src.infra.geocoding as geocoding

    monkeypatch.setattr(geocoding, "default_geocoder", lambda: _FakeGeocoder())

    app = create_app()
    client = TestClient(app)

    end = date.today()
    start = end - timedelta(days=14)

    resp = client.post(
        "/api/risk/query",
        json={
            "location_text": "Miami, FL",
            "date_range": {"start_date": start.isoformat(), "end_date": end.isoformat()},
        },
    )

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    assert data["location_label"]
    assert data["tile_url_template"].startswith("https://")
    assert len(data["legend"]) == 3


def test_post_risk_query_point_buffer_is_100_miles(monkeypatch) -> None:
    import sys
    from types import SimpleNamespace

    import backend.src.infra.geocoding as geocoding
    import backend.src.infra.ee_tiles as ee_tiles
    import backend.src.infra.ee_client as ee_client
    import backend.src.services.risk_service as risk_service

    monkeypatch.setattr(geocoding, "default_geocoder", lambda: _FakeGeocoder())
    monkeypatch.setattr(ee_client.EarthEngineClient, "initialize", lambda self: None)
    fake_tile = lambda image, vis: ee_tiles.TileUrlTemplate(url="https://example.com/{z}/{x}/{y}")
    monkeypatch.setattr(ee_tiles, "ee_image_tile_url_template", fake_tile)
    monkeypatch.setattr(risk_service, "ee_image_tile_url_template", fake_tile)

    captured: dict[str, float] = {}

    class _FakeGeom:
        def buffer(self, meters: float):
            captured["meters"] = float(meters)
            return self

        def bounds(self):
            return self

    class _FakeGeometry:
        @staticmethod
        def Point(_coords):
            return _FakeGeom()

        def __call__(self, _geojson):
            return _FakeGeom()

    class _FakeImage:
        @staticmethod
        def constant(_v):
            return SimpleNamespace(toInt=lambda: SimpleNamespace(clip=lambda _r: object()))

    sys.modules["ee"] = SimpleNamespace(Geometry=_FakeGeometry(), Image=_FakeImage())

    app = create_app()
    client = TestClient(app)

    end = date.today()
    start = end - timedelta(days=14)

    resp = client.post(
        "/api/risk/query",
        json={
            "location_text": "33101",
            "date_range": {"start_date": start.isoformat(), "end_date": end.isoformat()},
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert captured.get("meters") == 160_934.0
    assert isinstance(data.get("layers"), list)
    vp = data.get("viewport")
    assert isinstance(vp, dict)
    assert vp.get("radius_meters") == 160_934.0
