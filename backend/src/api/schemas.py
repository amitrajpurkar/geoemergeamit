from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class DateRangeSchema(BaseModel):
    start_date: date
    end_date: date


class RiskBandSchema(BaseModel):
    code: str
    label: str
    color: str


class RiskLayerResponseSchema(BaseModel):
    location_label: str
    date_range: DateRangeSchema
    tile_url_template: str
    attribution: str | None = None
    legend: list[RiskBandSchema]


class ErrorResponseSchema(BaseModel):
    detail: str = Field(..., description="Human-readable error")


JsonObject = dict[str, Any]
