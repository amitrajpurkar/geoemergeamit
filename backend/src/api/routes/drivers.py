from __future__ import annotations

from fastapi import APIRouter

from backend.src.api.schemas import DriversRequestSchema, DriversResponseSchema
from backend.src.services.drivers_service import DriversService


router = APIRouter(prefix="/api/drivers", tags=["drivers"])


@router.post("", response_model=DriversResponseSchema)
def post_drivers(body: DriversRequestSchema) -> DriversResponseSchema:
    service = DriversService.from_repo_root()
    resp = service.query(
        location_text=body.location_text,
        start_date=body.date_range.start_date if body.date_range else None,
        end_date=body.date_range.end_date if body.date_range else None,
    )
    return DriversResponseSchema(**resp)
