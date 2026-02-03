from __future__ import annotations

from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path

from backend.src.domain.errors import DataUnavailableError, InvalidDateRangeError
from backend.src.domain.models import RiskBand, default_risk_bands
from backend.src.eda.risk_mapping import build_default_risk_image
from backend.src.infra.ee_client import EarthEngineClient
from backend.src.infra.ee_tiles import ee_image_tile_url_template
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

    def get_default(self, *, window: str) -> dict:
        today = date.today()
        if window == "last_30_days":
            start = today - timedelta(days=30)
        elif window == "last_12_months":
            start = today - timedelta(days=365)
        else:
            raise InvalidDateRangeError

        sources = load_sources_config(default_sources_yaml_path(self._repo_root))
        sources = merge_local_auth_token(sources, repo_root=self._repo_root)

        ee_project = sources.googleearthengine.projectid
        client = EarthEngineClient(project=ee_project)
        client.initialize()

        region = florida_ee_geometry(repo_root=self._repo_root, sources=sources)
        image = build_default_risk_image(region=region, start_date=start, end_date=today, sources=sources)

        vis = {
            "min": 0,
            "max": 2,
            "palette": ["#2E7D32", "#F9A825", "#C62828"],
        }
        tile = ee_image_tile_url_template(image, vis)

        if not tile.url:
            raise DataUnavailableError("No tile URL returned")

        return {
            "location_label": "Florida",
            "date_range": {"start_date": start, "end_date": today},
            "tile_url_template": tile.url,
            "attribution": "Google Earth Engine",
            "legend": self._legend(),
        }
