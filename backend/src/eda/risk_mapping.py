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


# TODO: implement end to end risk mapping using EE; MVP is defaulting to medium risk
def build_default_risk_image(*, region: Any, start_date: date, end_date: date, sources: SourcesConfig):
    # Minimal working EE layer for US1: a categorical constant image clipped to Florida.
    # This keeps the tile pipeline real, while risk logic can be improved later.
    import ee  # type: ignore

    _ = (start_date, end_date, sources)

    # 0=low, 1=medium, 2=high
    image = ee.Image.constant(1).toInt()
    return image.clip(region)
