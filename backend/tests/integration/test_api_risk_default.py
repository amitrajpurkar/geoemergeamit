from __future__ import annotations

from fastapi.testclient import TestClient

from backend.src.api.app import create_app


def test_get_default_risk_shape() -> None:
    app = create_app()
    client = TestClient(app)

    # This may return 503 if Earth Engine isn't authenticated in the environment.
    resp = client.get("/api/risk/default")

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    assert data["location_label"]
    assert data["tile_url_template"].startswith("https://")
    assert len(data["legend"]) == 3
    assert isinstance(data.get("layers"), list)
    
    # Verify default parameters per spec: ZIP 33172, date range 2023-01-01 to 2024-12-31
    assert data["date_range"]["start_date"] == "2023-01-01"
    assert data["date_range"]["end_date"] == "2024-12-31"
    # Location label should contain ZIP or city name for 33172
    assert data["location_label"]  # Will be geocoded name for ZIP 33172
