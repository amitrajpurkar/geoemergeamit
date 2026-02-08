from __future__ import annotations

from datetime import date
from typing import Any

from backend.src.domain.models import RiskBandCode
from backend.src.infra.sources import SourcesConfig


def classify_risk_score(*, ndvi: float, lst_c: float, precip_mm: float) -> RiskBandCode:
    score = 0

    # Greener vegetation (NDVI) can indicate habitat suitability.
    if ndvi > 0.3:
        score += 1

    # Moderate-to-warm temps increase mosquito activity.
    if 20.0 <= lst_c <= 35.0:
        score += 1

    # Some rainfall increases standing water.
    if precip_mm > 10.0:
        score += 1

    if score <= 1:
        return RiskBandCode.low
    if score == 2:
        return RiskBandCode.medium
    return RiskBandCode.high


def build_default_risk_image(*, region: Any, start_date: date, end_date: date, sources: SourcesConfig):
    import ee  # type: ignore
    import logging

    from backend.src.domain.errors import DataUnavailableError

    logger = logging.getLogger(__name__)

    s2_id = sources.eeimagesets.get("vegetation")
    lst_id = sources.eeimagesets.get("land_surface_temperature")
    chirps_id = sources.eeimagesets.get("precipitation")

    if not (s2_id and lst_id and chirps_id):
        raise DataUnavailableError("Earth Engine image sets are not configured")

    logger.info(f"Building risk image for region {region} from {start_date} to {end_date}")

    # Cloud masking function for Sentinel-2
    def _mask_s2_clouds(img):
        qa = img.select("QA60")
        cloud_bit_mask = 1 << 10
        cirrus_bit_mask = 1 << 11
        mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
        return img.updateMask(mask)

    # T104: Process and combine image bands
    # NDVI from Sentinel-2
    s2 = (
        ee.ImageCollection(s2_id)
        .filterDate(str(start_date), str(end_date))
        .filterBounds(region)
        .map(_mask_s2_clouds)
    )
    s2_img = s2.median()
    ndvi = s2_img.normalizedDifference(["B8", "B4"]).rename("NDVI").clip(region)

    # LST from MODIS (convert to Celsius)
    lst = (
        ee.ImageCollection(lst_id)
        .filterDate(str(start_date), str(end_date))
        .filterBounds(region)
        .select(["LST_Day_1km"])
    )
    lst_img = lst.mean().multiply(0.02).subtract(273.15).rename("LST_Day_1km").clip(region)

    # Precipitation from CHIRPS
    chirps = (
        ee.ImageCollection(chirps_id)
        .filterDate(str(start_date), str(end_date))
        .filterBounds(region)
    )
    precip_img = chirps.sum().rename("precipitation").clip(region)

    # T104: Combine bands into single image for pixel-aligned operations
    combined = ndvi.addBands(lst_img).addBands(precip_img)

    # T103: Compute regional means server-side (as ee.Number for conditional operations)
    # Use larger scale for faster computation, maxPixels for large regions
    mean_lst_dict = lst_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=1000,
        maxPixels=1e12
    )
    mean_rain_dict = precip_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=5566,
        maxPixels=1e12
    )

    # Extract as ee.Number (server-side) - NOT .getInfo() (client-side)
    mean_lst = ee.Number(mean_lst_dict.get("LST_Day_1km"))
    mean_rain = ee.Number(mean_rain_dict.get("precipitation"))

    # T107: Log regional statistics (will appear in server logs)
    logger.info(f"Computing pixel-wise risk classification for date range {start_date} to {end_date}")

    # T102 & T105: Pixel-wise classification matching notebook cell 8 logic
    # Select bands from combined image
    ndvi_band = combined.select("NDVI")
    lst_band = combined.select("LST_Day_1km")
    rain_band = combined.select("precipitation")

    # Classification conditions (matching notebook thresholds)
    low_risk = ndvi_band.lt(0).And(lst_band.lt(mean_lst)).And(rain_band.lt(mean_rain))
    med_risk = ndvi_band.lte(0.3).Or(lst_band.eq(mean_lst)).Or(rain_band.eq(mean_rain))
    high_risk = ndvi_band.gt(0.3).And(lst_band.gt(mean_lst)).And(rain_band.gt(mean_rain))

    # Combine classifications: 1=Low, 2=Medium, 3=High
    # Use 0, 1, 2 for our risk bands (Low=0, Medium=1, High=2)
    risk = (
        low_risk.multiply(0)
        .add(med_risk.multiply(1))
        .add(high_risk.multiply(2))
        .toInt()
        .rename("Risk_Level")
    )

    logger.info("Risk classification complete - pixel-wise conditional logic applied")

    return risk
