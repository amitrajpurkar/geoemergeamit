from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DateRangeSchema(BaseModel):
    start_date: date
    end_date: date


class RiskQueryRequestSchema(BaseModel):
    location_text: str = Field(..., max_length=200)
    date_range: DateRangeSchema

    @field_validator("location_text")
    @classmethod
    def _validate_location_text(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("location_text must be a string")
        vv = v.strip()
        if not vv:
            raise ValueError("location_text is required")
        return vv


class RiskBandSchema(BaseModel):
    code: str
    label: str
    color: str


class OverlayLayerSchema(BaseModel):
    layer_id: str
    label: str
    tile_url_template: str
    attribution: str | None = None


class ViewportSchema(BaseModel):
    center_lat: float
    center_lng: float
    radius_meters: float


class RiskLayerResponseSchema(BaseModel):
    location_label: str
    date_range: DateRangeSchema
    tile_url_template: str
    attribution: str | None = None
    legend: list[RiskBandSchema]
    layers: list[OverlayLayerSchema] = Field(default_factory=list)
    viewport: ViewportSchema | None = None


class ErrorResponseSchema(BaseModel):
    detail: str = Field(..., description="Human-readable error")


JsonObject = dict[str, Any]
