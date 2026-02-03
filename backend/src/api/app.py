from __future__ import annotations

from fastapi import FastAPI

from backend.src.api.errors import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Mosquito Risk Dashboard API", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    register_error_handlers(app)
    return app
