from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class LocationSource(str, Enum):
    default_state = "default_state"
    geocoded_text = "geocoded_text"


@dataclass(frozen=True)
class Location:
    id: str
    label: str
    source: LocationSource
    geometry: dict
    bbox: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date


class RiskBandCode(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(frozen=True)
class RiskBand:
    code: RiskBandCode
    label: str
    color: str


def default_risk_bands() -> list[RiskBand]:
    return [
        RiskBand(code=RiskBandCode.low, label="Low", color="#2E7D32"),
        RiskBand(code=RiskBandCode.medium, label="Medium", color="#F9A825"),
        RiskBand(code=RiskBandCode.high, label="High", color="#C62828"),
    ]
