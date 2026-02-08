from __future__ import annotations

from fastapi.testclient import TestClient

from backend.src.api.app import create_app


def test_risk_layers_have_legend_metadata() -> None:
    """Verify that all four risk layers return legend metadata with correct structure."""
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/risk/default")

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    assert "layers" in data
    layers = data["layers"]
    assert len(layers) == 4

    # Expected layer IDs
    expected_ids = {"risk", "land_surface_temperature", "land_cover", "precipitation"}
    found_ids = {layer["layer_id"] for layer in layers}
    assert found_ids == expected_ids

    # Verify each layer has legend metadata
    for layer in layers:
        assert "legend" in layer, f"Layer {layer['layer_id']} missing legend"
        legend = layer["legend"]

        # Common legend fields
        assert "type" in legend
        assert "min" in legend
        assert "max" in legend
        assert "palette" in legend
        assert isinstance(legend["palette"], list)
        assert len(legend["palette"]) > 0

        # Type-specific validation
        if legend["type"] == "categorical":
            # Risk layer should have categories
            assert "categories" in legend
            assert isinstance(legend["categories"], list)
            assert len(legend["categories"]) == 3  # Low, Medium, High
            for cat in legend["categories"]:
                assert "value" in cat
                assert "label" in cat
                assert "color" in cat
        elif legend["type"] == "continuous":
            # Continuous layers should have units
            assert "unit" in legend
            assert legend["unit"] is not None

        # Verify min < max
        assert legend["min"] < legend["max"], f"Layer {layer['layer_id']} has invalid range"


def test_driver_tiles_have_legend_metadata() -> None:
    """Verify that all driver tiles return legend metadata with correct structure."""
    app = create_app()
    client = TestClient(app)

    resp = client.post(
        "/api/drivers",
        json={"location_text": "33172", "date_range": {"start_date": "2023-01-01", "end_date": "2024-12-31"}},
    )

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    assert "tiles" in data
    tiles = data["tiles"]
    assert len(tiles) == 4

    # Expected driver types
    expected_types = {"vegetation", "temperature", "precipitation", "standing_water"}
    found_types = {tile["driver_type"] for tile in tiles}
    assert found_types == expected_types

    # Verify each tile has legend metadata
    for tile in tiles:
        assert "legend" in tile, f"Tile {tile['driver_type']} missing legend"
        legend = tile["legend"]

        # Common legend fields
        assert "type" in legend
        assert legend["type"] == "continuous"  # All driver tiles are continuous
        assert "min" in legend
        assert "max" in legend
        assert "palette" in legend
        assert "unit" in legend

        assert isinstance(legend["palette"], list)
        assert len(legend["palette"]) > 0

        # Verify min < max
        assert legend["min"] < legend["max"], f"Tile {tile['driver_type']} has invalid range"

        # Verify units are meaningful
        assert legend["unit"] in {"NDVI", "°C", "mm"}, f"Unexpected unit: {legend['unit']}"


def test_legend_palette_colors_valid() -> None:
    """Verify that palette colors are valid hex color codes."""
    app = create_app()
    client = TestClient(app)

    resp = client.get("/api/risk/default")

    assert resp.status_code in {200, 503}
    if resp.status_code == 503:
        return

    data = resp.json()
    layers = data["layers"]

    for layer in layers:
        legend = layer["legend"]
        for color in legend["palette"]:
            # Check if it's a valid hex color
            assert color.startswith("#"), f"Color {color} doesn't start with #"
            assert len(color) == 7, f"Color {color} not 7 characters"
            # Verify hex characters
            try:
                int(color[1:], 16)
            except ValueError:
                assert False, f"Color {color} is not valid hex"
