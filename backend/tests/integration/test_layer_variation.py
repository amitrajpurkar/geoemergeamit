from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.src.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


def test_risk_layer_has_variation(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])
    risk_layer = next((layer for layer in layers if layer["layer_id"] == "risk"), None)

    assert risk_layer is not None
    tile_url = risk_layer["tile_url_template"]
    assert tile_url.startswith("https://earthengine.googleapis.com/")
    assert "{z}" in tile_url
    assert "{x}" in tile_url
    assert "{y}" in tile_url
    assert "token=" in tile_url


def test_lst_layer_has_variation(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])
    lst_layer = next(
        (layer for layer in layers if layer["layer_id"] == "land_surface_temperature"), None
    )

    assert lst_layer is not None
    tile_url = lst_layer["tile_url_template"]
    assert tile_url.startswith("https://earthengine.googleapis.com/")
    assert "token=" in tile_url


def test_ndvi_layer_has_variation(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])
    ndvi_layer = next((layer for layer in layers if layer["layer_id"] == "land_cover"), None)

    assert ndvi_layer is not None
    assert ndvi_layer["label"] == "Vegetation (NDVI)"
    tile_url = ndvi_layer["tile_url_template"]
    assert tile_url.startswith("https://earthengine.googleapis.com/")
    assert "token=" in tile_url


def test_precipitation_layer_has_variation(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])
    precip_layer = next(
        (layer for layer in layers if layer["layer_id"] == "precipitation"), None
    )

    assert precip_layer is not None
    tile_url = precip_layer["tile_url_template"]
    assert tile_url.startswith("https://earthengine.googleapis.com/")
    assert "token=" in tile_url


def test_all_layers_present_and_distinct(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])

    assert len(layers) == 4

    layer_ids = {layer["layer_id"] for layer in layers}
    assert layer_ids == {"risk", "land_surface_temperature", "land_cover", "precipitation"}

    tile_urls = [layer["tile_url_template"] for layer in layers]
    assert len(set(tile_urls)) == 4


def test_layer_attributions_are_specific(client: TestClient) -> None:
    resp = client.get("/api/risk/default", params={"window": "last_30_days"})

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])

    lst_layer = next(
        (layer for layer in layers if layer["layer_id"] == "land_surface_temperature"), None
    )
    assert "MODIS" in lst_layer["attribution"]

    ndvi_layer = next((layer for layer in layers if layer["layer_id"] == "land_cover"), None)
    assert "Sentinel-2" in ndvi_layer["attribution"]

    precip_layer = next(
        (layer for layer in layers if layer["layer_id"] == "precipitation"), None
    )
    assert "CHIRPS" in precip_layer["attribution"]


def test_query_endpoint_layers_have_variation(client: TestClient) -> None:
    resp = client.get(
        "/api/risk/query",
        params={
            "location_text": "Miami, FL",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
        },
    )

    if resp.status_code == 503:
        pytest.skip("Earth Engine not authenticated")

    if resp.status_code == 400:
        pytest.skip("Geocoding failed or invalid location")

    assert resp.status_code == 200
    data = resp.json()
    layers = data.get("layers", [])

    assert len(layers) == 4

    tile_urls = [layer["tile_url_template"] for layer in layers]
    assert len(set(tile_urls)) == 4

    for tile_url in tile_urls:
        assert tile_url.startswith("https://earthengine.googleapis.com/")
        assert "token=" in tile_url
