from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.api.errors import register_error_handlers
from backend.src.api.routes.drivers import router as drivers_router
from backend.src.api.routes.risk import router as risk_router
from backend.src.api.middleware import BasicRateLimitMiddleware, CorrelationIdMiddleware
from backend.src.infra.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Mosquito Risk Dashboard API", version="0.1.0")

    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(BasicRateLimitMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(risk_router)
    app.include_router(drivers_router)
    register_error_handlers(app)
    return app
