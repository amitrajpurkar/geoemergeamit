from __future__ import annotations

from backend.src.domain.models import RiskBandCode, default_risk_bands


def test_default_risk_bands_is_ordered_and_complete() -> None:
    bands = default_risk_bands()
    assert [b.code for b in bands] == [RiskBandCode.low, RiskBandCode.medium, RiskBandCode.high]
    assert all(b.label for b in bands)
    assert all(b.color for b in bands)
