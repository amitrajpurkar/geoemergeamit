from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.src.domain.errors import DataUnavailableError, DomainError, InvalidDateRangeError, InvalidLocationError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidLocationError)
    def _invalid_location_handler(_request, exc: InvalidLocationError):
        return JSONResponse(status_code=400, content={"detail": str(exc) or "Invalid location"})

    @app.exception_handler(InvalidDateRangeError)
    def _invalid_date_range_handler(_request, exc: InvalidDateRangeError):
        return JSONResponse(status_code=400, content={"detail": str(exc) or "Invalid date range"})

    @app.exception_handler(DataUnavailableError)
    def _data_unavailable_handler(_request, exc: DataUnavailableError):
        return JSONResponse(status_code=503, content={"detail": str(exc) or "Data unavailable"})

    @app.exception_handler(DomainError)
    def _domain_error_handler(_request, exc: DomainError):
        return JSONResponse(status_code=400, content={"detail": str(exc) or "Request error"})
