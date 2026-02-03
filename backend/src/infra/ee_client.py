from __future__ import annotations

from dataclasses import dataclass

from backend.src.domain.errors import DataUnavailableError


@dataclass(frozen=True)
class EarthEngineClient:
    project: str | None = None

    def initialize(self) -> None:
        try:
            import ee  # type: ignore
        except Exception as e:  # pragma: no cover
            raise DataUnavailableError("earthengine-api is not available") from e

        try:
            if self.project:
                ee.Initialize(project=self.project)
            else:
                ee.Initialize()
        except Exception as e:
            raise DataUnavailableError(
                "Earth Engine is not initialized. Authenticate locally (earthengine authenticate) and retry."
            ) from e
