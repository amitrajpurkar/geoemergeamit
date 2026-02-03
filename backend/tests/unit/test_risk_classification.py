from __future__ import annotations

from backend.src.domain.models import RiskBandCode
from backend.src.eda.risk_mapping import classify_risk_score


def test_classify_risk_score_low() -> None:
    assert (
        classify_risk_score(ndvi=0.1, lst_c=10.0, precip_mm=0.0)
        == RiskBandCode.low
    )


def test_classify_risk_score_medium() -> None:
    assert (
        classify_risk_score(ndvi=0.4, lst_c=30.0, precip_mm=0.0)
        == RiskBandCode.medium
    )


def test_classify_risk_score_high() -> None:
    assert (
        classify_risk_score(ndvi=0.5, lst_c=30.0, precip_mm=20.0)
        == RiskBandCode.high
    )
