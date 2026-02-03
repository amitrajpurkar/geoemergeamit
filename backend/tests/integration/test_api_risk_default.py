from __future__ import annotations

from fastapi.testclient import TestClient

from backend.src.api.app import create_app


def test_get_default_risk_shape() -> None:
    app = create_app()
    client = TestClient(app)

    # This may return 503 if Earth Engine isn't authenticated in the environment.
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    assert data["location_label"]
    assert data["tile_url_template"].startswith("https://")
    assert len(data["legend"]) == 3
