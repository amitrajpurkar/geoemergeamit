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
