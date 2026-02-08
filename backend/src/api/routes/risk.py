from __future__ import annotations

from fastapi import APIRouter

from backend.src.api.schemas import RiskLayerResponseSchema, RiskQueryRequestSchema
from backend.src.services.risk_service import RiskService


router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/default", response_model=RiskLayerResponseSchema)
def get_default_risk() -> RiskLayerResponseSchema:
    service = RiskService.from_repo_root()
    layer = service.get_default()
    return RiskLayerResponseSchema(
        location_label=layer["location_label"],
        date_range=layer["date_range"],
        tile_url_template=layer["tile_url_template"],
        attribution=layer.get("attribution"),
        legend=layer["legend"],
        layers=layer.get("layers", []),
        viewport=layer.get("viewport"),
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
        layers=layer.get("layers", []),
        viewport=layer.get("viewport"),
    )
