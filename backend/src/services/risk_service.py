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

        s2_id = sources.eeimagesets.get("vegetation")
        lst_id = sources.eeimagesets.get("land_surface_temperature")
        chirps_id = sources.eeimagesets.get("precipitation")
        
        if not (s2_id and lst_id and chirps_id):
            raise DataUnavailableError("Earth Engine image sets are not configured")

        def _mask_s2_clouds(img):
            qa = img.select("QA60")
            cloud_bit_mask = 1 << 10
            cirrus_bit_mask = 1 << 11
            mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
            return img.updateMask(mask)

        s2 = (
            ee.ImageCollection(s2_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
            .map(_mask_s2_clouds)
        )
        s2_img = s2.median()
        ndvi = s2_img.normalizedDifference(["B8", "B4"]).rename("ndvi").clip(region)

        lst = (
            ee.ImageCollection(lst_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
            .select(["LST_Day_1km"])
        )
        lst_img = lst.mean().multiply(0.02).subtract(273.15).rename("lst_c").clip(region)

        chirps = (
            ee.ImageCollection(chirps_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
        )
        precip_img = chirps.sum().rename("precip_mm").clip(region)

        risk_image = build_default_risk_image(region=region, start_date=start, end_date=end, sources=sources)

        risk_vis = {"min": 0, "max": 2, "palette": ["#2E7D32", "#F9A825", "#C62828"]}
        lst_vis = {"min": 10, "max": 40, "palette": ["#2c7bb6", "#ffffbf", "#d7191c"]}
        ndvi_vis = {"min": 0.0, "max": 1.0, "palette": ["#f7fcf5", "#74c476", "#00441b"]}
        window_days = (end - start).days + 1
        precip_max = min(3000, max(100, window_days * 20))
        precip_vis = {"min": 0, "max": precip_max, "palette": ["#f7fbff", "#6baed6", "#08306b"]}

        risk_tile = ee_image_tile_url_template(risk_image, risk_vis)
        lst_tile = ee_image_tile_url_template(lst_img, lst_vis)
        ndvi_tile = ee_image_tile_url_template(ndvi, ndvi_vis)
        precip_tile = ee_image_tile_url_template(precip_img, precip_vis)

        return [
            {
                "layer_id": "risk",
                "label": "Mosquito Risk",
                "tile_url_template": risk_tile.url,
                "attribution": "Google Earth Engine",
                "legend": {
                    "type": "categorical",
                    "min": risk_vis["min"],
                    "max": risk_vis["max"],
                    "palette": risk_vis["palette"],
                    "categories": [
                        {"value": 0, "label": "Low", "color": "#2E7D32"},
                        {"value": 1, "label": "Medium", "color": "#F9A825"},
                        {"value": 2, "label": "High", "color": "#C62828"}
                    ]
                }
            },
            {
                "layer_id": "land_surface_temperature",
                "label": "Land Surface Temperature",
                "tile_url_template": lst_tile.url,
                "attribution": "MODIS LST (MOD11A1) via Google Earth Engine",
                "legend": {
                    "type": "continuous",
                    "min": lst_vis["min"],
                    "max": lst_vis["max"],
                    "palette": lst_vis["palette"],
                    "unit": "°C"
                }
            },
            {
                "layer_id": "land_cover",
                "label": "Vegetation (NDVI)",
                "tile_url_template": ndvi_tile.url,
                "attribution": "Sentinel-2 SR Harmonized (Copernicus) via Google Earth Engine",
                "legend": {
                    "type": "continuous",
                    "min": ndvi_vis["min"],
                    "max": ndvi_vis["max"],
                    "palette": ndvi_vis["palette"],
                    "unit": "NDVI"
                }
            },
            {
                "layer_id": "precipitation",
                "label": "Precipitation",
                "tile_url_template": precip_tile.url,
                "attribution": "CHIRPS Daily Precipitation via Google Earth Engine",
                "legend": {
                    "type": "continuous",
                    "min": precip_vis["min"],
                    "max": precip_vis["max"],
                    "palette": precip_vis["palette"],
                    "unit": "mm"
                }
            },
        ]

    def get_default(self) -> dict:
        # Fixed default parameters per spec: ZIP 33172, date range 2023-01-01 to 2024-12-31
        default_location = "33172"
        start = date(2023, 1, 1)
        end = date(2024, 12, 31)

        sources = load_sources_config(default_sources_yaml_path(self._repo_root))
        sources = merge_local_auth_token(sources, repo_root=self._repo_root)

        ee_project = sources.googleearthengine.projectid
        client = EarthEngineClient(project=ee_project)
        client.initialize()

        geocoder = default_geocoder()
        result = geocoder.geocode(default_location)
        location = location_from_geocoding(str(uuid4()), default_location, result)

        import ee  # type: ignore

        region, viewport = region_and_viewport_from_location(
            location_geometry=location.geometry,
            location_bbox=location.bbox,
        )

        layers = self._layers(region=region, start=start, end=end, sources=sources)
        tile_url = layers[0]["tile_url_template"]
        if not tile_url:
            raise DataUnavailableError("No tile URL returned")

        return {
            "location_label": location.label,
            "date_range": {"start_date": start, "end_date": end},
            "tile_url_template": tile_url,
            "attribution": layers[0].get("attribution"),
            "legend": self._legend(),
            "layers": layers,
            "viewport": viewport,
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
