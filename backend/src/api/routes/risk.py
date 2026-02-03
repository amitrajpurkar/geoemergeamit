from __future__ import annotations

from enum import Enum

from fastapi import APIRouter, Query

from backend.src.api.schemas import RiskLayerResponseSchema, RiskQueryRequestSchema
from backend.src.services.risk_service import RiskService


router = APIRouter(prefix="/api/risk", tags=["risk"])


class DefaultWindow(str, Enum):
    last_30_days = "last_30_days"
    last_12_months = "last_12_months"


@router.get("/default", response_model=RiskLayerResponseSchema)
def get_default_risk(window: DefaultWindow = Query(...)) -> RiskLayerResponseSchema:
    service = RiskService.from_repo_root()
    layer = service.get_default(window=window.value)
    return RiskLayerResponseSchema(
        location_label=layer["location_label"],
        date_range=layer["date_range"],
        tile_url_template=layer["tile_url_template"],
        attribution=layer.get("attribution"),
        legend=layer["legend"],
    )


@router.post("/query", response_model=RiskLayerResponseSchema)
def post_risk_query(body: RiskQueryRequestSchema) -> RiskLayerResponseSchema:
    service = RiskService.from_repo_root()
    layer = service.query(
        location_text=body.location_text,
        start_date=body.date_range.start_date,
        end_date=body.date_range.end_date,
    )
    return RiskLayerResponseSchema(
        location_label=layer["location_label"],
        date_range=layer["date_range"],
        tile_url_template=layer["tile_url_template"],
        attribution=layer.get("attribution"),
        legend=layer["legend"],
    )
