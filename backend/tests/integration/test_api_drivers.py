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


def test_post_drivers_shape(monkeypatch) -> None:
    import backend.src.infra.ee_client as ee_client
    import backend.src.infra.ee_tiles as ee_tiles
    import backend.src.infra.geocoding as geocoding
    import backend.src.infra.sources as sources
    import backend.src.services.drivers_service as drivers_service

    monkeypatch.setattr(ee_client.EarthEngineClient, "initialize", lambda self: None)
    monkeypatch.setattr(
        drivers_service,
        "ee_image_tile_url_template",
        lambda _img, _vis: ee_tiles.TileUrlTemplate(url="https://example.com/{z}/{x}/{y}"),
    )

    monkeypatch.setattr(geocoding, "default_geocoder", lambda: _FakeGeocoder())

    monkeypatch.setattr(
        sources,
        "load_sources_config",
        lambda _path: sources.SourcesConfig(
            datasets={},
            eeimagesets={
                "vegetation": "COPERNICUS/S2_SR_HARMONIZED",
                "land_surface_temperature": "MODIS/061/MOD11A1",
                "precipitation": "UCSB-CHG/CHIRPS/DAILY",
            },
            googleearthengine=sources.GoogleEarthEngineConfig(projectid=None, token=None),
        ),
    )
    monkeypatch.setattr(sources, "merge_local_auth_token", lambda cfg, *, repo_root: cfg)

    import sys
    from types import SimpleNamespace

    class _FakeImage:
        def __init__(self):
            pass

        def filterDate(self, *_args, **_kwargs):
            return self

        def filterBounds(self, *_args, **_kwargs):
            return self

        def map(self, *_args, **_kwargs):
            return self

        def select(self, *_args, **_kwargs):
            return self

        def median(self):
            return self

        def mean(self):
            return self

        def sum(self):
            return self

        def normalizedDifference(self, *_args, **_kwargs):
            return self

        def rename(self, *_args, **_kwargs):
            return self

        def clip(self, *_args, **_kwargs):
            return self

        def multiply(self, *_args, **_kwargs):
            return self

        def subtract(self, *_args, **_kwargs):
            return self

    class _FakeGeom:
        def buffer(self, *_args, **_kwargs):
            return self

        def bounds(self):
            return self

    class _FakeGeometry:
        @staticmethod
        def Point(_coords):
            return _FakeGeom()

        def __call__(self, _geojson):
            return _FakeGeom()

    sys.modules["ee"] = SimpleNamespace(
        Geometry=_FakeGeometry(),
        ImageCollection=lambda _id: _FakeImage(),
    )

    app = create_app()
    client = TestClient(app)

    end = date.today()
    start = end - timedelta(days=30)

    resp = client.post(
        "/api/drivers",
        json={
            "location_text": "Miami, FL",
            "date_range": {"start_date": start.isoformat(), "end_date": end.isoformat()},
        },
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["location_label"]
    assert data.get("date_range")
    assert data.get("viewport")
    assert isinstance(data.get("tiles"), list)
    assert len(data["tiles"]) >= 3

    for tile in data["tiles"]:
        assert tile["driver_type"]
        assert tile["title"]
        assert tile["summary"]
        assert tile.get("tile_url_template")
