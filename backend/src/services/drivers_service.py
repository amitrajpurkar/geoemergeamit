from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from backend.src.domain.errors import DataUnavailableError
from backend.src.domain.models import DateRange
from backend.src.domain.validation import validate_date_range
from backend.src.infra.ee_client import EarthEngineClient
from backend.src.infra.ee_tiles import ee_image_tile_url_template
from backend.src.infra.ee_geometry import region_and_viewport_from_location
from backend.src.infra.geocoding import default_geocoder, location_from_geocoding
from backend.src.infra.sources import default_sources_yaml_path, load_sources_config, merge_local_auth_token


def _repo_root_from_here() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise DataUnavailableError("Could not locate repo root (pyproject.toml not found)")


class DriversService:
    def __init__(self, *, repo_root: Path) -> None:
        self._repo_root = repo_root

    @classmethod
    def from_repo_root(cls) -> "DriversService":
        return cls(repo_root=_repo_root_from_here())

    def query(self, *, location_text: str, start_date: date | None = None, end_date: date | None = None) -> dict:
        geocoder = default_geocoder()
        result = geocoder.geocode(location_text)
        location = location_from_geocoding(str(uuid4()), location_text, result)

        if start_date is None or end_date is None:
            end = date.today()
            start = end - timedelta(days=365 * 2)
        else:
            start = start_date
            end = end_date

        validate_date_range(DateRange(start_date=start, end_date=end))

        sources = load_sources_config(default_sources_yaml_path(self._repo_root))
        sources = merge_local_auth_token(sources, repo_root=self._repo_root)

        client = EarthEngineClient(project=sources.googleearthengine.projectid)
        client.initialize()

        import ee  # type: ignore

        region, viewport = region_and_viewport_from_location(
            location_geometry=location.geometry,
            location_bbox=location.bbox,
        )

        window_days = (end - start).days + 1

        def _mask_s2_clouds(img):
            qa = img.select("QA60")
            cloud_bit_mask = 1 << 10
            cirrus_bit_mask = 1 << 11
            mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
            return img.updateMask(mask)

        s2_id = sources.eeimagesets.get("vegetation")
        lst_id = sources.eeimagesets.get("land_surface_temperature")
        chirps_id = sources.eeimagesets.get("precipitation")
        if not (s2_id and lst_id and chirps_id):
            raise DataUnavailableError("Earth Engine image sets are not configured")

        # Vegetation: NDVI from Sentinel-2 SR (B8 NIR, B4 RED)
        s2 = (
            ee.ImageCollection(s2_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
            .map(_mask_s2_clouds)
        )
        s2_img = s2.median()
        ndvi = s2_img.normalizedDifference(["B8", "B4"]).rename("ndvi").clip(region)
        ndvi_vis = {"min": 0.0, "max": 1.0, "palette": ["#f7fcf5", "#74c476", "#00441b"]}

        # Temperature: MODIS LST Day (Kelvin * 0.02). Convert to Celsius for visualization.
        lst = (
            ee.ImageCollection(lst_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
            .select(["LST_Day_1km"])
        )
        lst_img = lst.mean().multiply(0.02).subtract(273.15).rename("lst_c").clip(region)
        lst_vis = {"min": 10, "max": 40, "palette": ["#2c7bb6", "#ffffbf", "#d7191c"]}

        # Precipitation: CHIRPS daily mm/day, sum over window
        chirps = (
            ee.ImageCollection(chirps_id)
            .filterDate(str(start), str(end))
            .filterBounds(region)
        )
        precip = chirps.sum().rename("precip_mm").clip(region)
        precip_max = min(3000, max(100, window_days * 20))
        precip_vis = {"min": 0, "max": precip_max, "palette": ["#f7fbff", "#6baed6", "#08306b"]}

        # Standing water proxy: NDWI from Sentinel-2 (B3 green, B8 NIR)
        ndwi = s2_img.normalizedDifference(["B3", "B8"]).rename("ndwi").clip(region)
        ndwi_vis = {"min": -0.3, "max": 0.6, "palette": ["#bdbdbd", "#41b6c4", "#0c2c84"]}

        ndvi_tile = ee_image_tile_url_template(ndvi, ndvi_vis)
        lst_tile = ee_image_tile_url_template(lst_img, lst_vis)
        precip_tile = ee_image_tile_url_template(precip, precip_vis)
        ndwi_tile = ee_image_tile_url_template(ndwi, ndwi_vis)

        tiles = [
            {
                "driver_type": "vegetation",
                "title": "Vegetation",
                "summary": "NDVI composite for the selected date range.",
                "metrics": {"index": "NDVI"},
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
                "driver_type": "temperature",
                "title": "Temperature",
                "summary": "Mean land surface temperature (°C) for the selected date range.",
                "metrics": {"units": "C"},
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
                "driver_type": "precipitation",
                "title": "Precipitation / Standing Water",
                "summary": "Total precipitation (mm) and NDWI standing-water proxy for the selected date range.",
                "metrics": {"precip_units": "mm", "index": "NDWI"},
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
            {
                "driver_type": "standing_water",
                "title": "Standing Water (proxy)",
                "summary": "NDWI composite (water proxy) for the selected date range.",
                "metrics": {"index": "NDWI"},
                "tile_url_template": ndwi_tile.url,
                "attribution": "Sentinel-2 SR Harmonized (Copernicus) via Google Earth Engine",
                "legend": {
                    "type": "continuous",
                    "min": ndwi_vis["min"],
                    "max": ndwi_vis["max"],
                    "palette": ndwi_vis["palette"],
                    "unit": "NDWI"
                }
            },
        ]

        return {
            "location_label": location.label,
            "date_range": {"start_date": start, "end_date": end},
            "tiles": tiles,
            "viewport": viewport,
        }
