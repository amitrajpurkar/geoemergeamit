from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.domain.errors import DataUnavailableError


@dataclass(frozen=True)
class TileUrlTemplate:
    url: str


def ee_image_tile_url_template(image: Any, vis_params: dict[str, Any]) -> TileUrlTemplate:
    try:
        map_id = image.getMapId(vis_params)
    except Exception as e:
        raise DataUnavailableError("Failed to generate Earth Engine tile URL") from e

    mapid = map_id.get("mapid")
    token = map_id.get("token")
    if not isinstance(mapid, str) or not isinstance(token, str):
        raise DataUnavailableError("Earth Engine returned invalid map id")

    url = f"https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}"
    return TileUrlTemplate(url=url)
