from __future__ import annotations

from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from backend.src.domain.errors import DataUnavailableError, InvalidDateRangeError
from backend.src.domain.models import DateRange, RiskBand, default_risk_bands
from backend.src.domain.validation import validate_date_range
from backend.src.eda.risk_mapping import build_default_risk_image
from backend.src.infra.ee_client import EarthEngineClient
from backend.src.infra.ee_tiles import ee_image_tile_url_template
from backend.src.infra.ee_geometry import region_and_viewport_from_location
from backend.src.infra.geocoding import default_geocoder, location_from_geocoding
from backend.src.infra.regions import florida_ee_geometry
from backend.src.infra.sources import default_sources_yaml_path, load_sources_config, merge_local_auth_token


def _repo_root_from_here() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise DataUnavailableError("Could not locate repo root (pyproject.toml not found)")


class RiskService:
    def __init__(self, *, repo_root: Path) -> None:
        self._repo_root = repo_root

    @classmethod
    def from_repo_root(cls) -> "RiskService":
        return cls(repo_root=_repo_root_from_here())

    def _legend(self) -> list[dict]:
        bands: list[RiskBand] = default_risk_bands()
        return [asdict(b) | {"code": b.code.value} for b in bands]

    def _layers(self, *, region, start: date, end: date, sources) -> list[dict]:
        import ee  # type: ignore

        risk_image = build_default_risk_image(region=region, start_date=start, end_date=end, sources=sources)

        lst_image = ee.Image.constant(1).toInt().clip(region)
        land_cover_image = ee.Image.constant(1).toInt().clip(region)
        precip_image = ee.Image.constant(1).toInt().clip(region)

        risk_vis = {"min": 0, "max": 2, "palette": ["#2E7D32", "#F9A825", "#C62828"]}
        env_vis = {"min": 0, "max": 1, "palette": ["#1E88E5", "#90CAF9"]}

        risk_tile = ee_image_tile_url_template(risk_image, risk_vis)
        lst_tile = ee_image_tile_url_template(lst_image, env_vis)
        land_cover_tile = ee_image_tile_url_template(land_cover_image, env_vis)
        precip_tile = ee_image_tile_url_template(precip_image, env_vis)

        return [
            {
                "layer_id": "risk",
                "label": "Mosquito Risk",
                "tile_url_template": risk_tile.url,
                "attribution": "Google Earth Engine",
            },
            {
                "layer_id": "land_surface_temperature",
                "label": "Land Surface Temperature",
                "tile_url_template": lst_tile.url,
                "attribution": "Google Earth Engine",
            },
            {
                "layer_id": "land_cover",
                "label": "Land Cover",
                "tile_url_template": land_cover_tile.url,
                "attribution": "Google Earth Engine",
            },
            {
                "layer_id": "precipitation",
                "label": "Precipitation",
                "tile_url_template": precip_tile.url,
                "attribution": "Google Earth Engine",
            },
        ]

    def get_default(self, *, window: str) -> dict:
        today = date.today()
        if window == "last_30_days":
            start = today - timedelta(days=30)
        elif window == "last_12_months":
            start = today - timedelta(days=365)
        else:
            raise InvalidDateRangeError("Unsupported window")

        sources = load_sources_config(default_sources_yaml_path(self._repo_root))
        sources = merge_local_auth_token(sources, repo_root=self._repo_root)

        ee_project = sources.googleearthengine.projectid
        client = EarthEngineClient(project=ee_project)
        client.initialize()

        region = florida_ee_geometry(repo_root=self._repo_root, sources=sources)
        layers = self._layers(region=region, start=start, end=today, sources=sources)
        tile_url = layers[0]["tile_url_template"]
        if not tile_url:
            raise DataUnavailableError("No tile URL returned")

        return {
            "location_label": "Florida",
            "date_range": {"start_date": start, "end_date": today},
            "tile_url_template": tile_url,
            "attribution": layers[0].get("attribution"),
            "legend": self._legend(),
            "layers": layers,
        }

    def query(self, *, location_text: str, start_date: date, end_date: date) -> dict:
        date_range = DateRange(start_date=start_date, end_date=end_date)
        validate_date_range(date_range)

        sources = load_sources_config(default_sources_yaml_path(self._repo_root))
        sources = merge_local_auth_token(sources, repo_root=self._repo_root)

        ee_project = sources.googleearthengine.projectid
        client = EarthEngineClient(project=ee_project)
        client.initialize()

        geocoder = default_geocoder()
        result = geocoder.geocode(location_text)
        location = location_from_geocoding(str(uuid4()), location_text, result)

        import ee  # type: ignore

        region, viewport = region_and_viewport_from_location(
            location_geometry=location.geometry,
            location_bbox=location.bbox,
        )

        layers = self._layers(region=region, start=start_date, end=end_date, sources=sources)
        tile_url = layers[0]["tile_url_template"]
        if not tile_url:
            raise DataUnavailableError("No tile URL returned")

        return {
            "location_label": location.label,
            "date_range": {"start_date": start_date, "end_date": end_date},
            "tile_url_template": tile_url,
            "attribution": layers[0].get("attribution"),
            "legend": self._legend(),
            "layers": layers,
            "viewport": viewport,
        }
