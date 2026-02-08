from __future__ import annotations

from dataclasses import dataclass
import json
import logging
import time
from typing import Any

from backend.src.domain.errors import DataUnavailableError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TileUrlTemplate:
    url: str


_MAPID_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_MAPID_CACHE_TTL_SECONDS = 60 * 60


def _cache_key(image: Any, vis_params: dict[str, Any]) -> str:
    return json.dumps(
        {"image_id": id(image), "vis": vis_params},
        sort_keys=True,
        default=str,
    )

# TODO: at some point, we should validate the url is NOT logged; as it can leak the token value
def ee_image_tile_url_template(image: Any, vis_params: dict[str, Any]) -> TileUrlTemplate:
    key = _cache_key(image, vis_params)
    cached = _MAPID_CACHE.get(key)
    if cached is not None:
        ts, map_id = cached
        if (time.time() - ts) <= _MAPID_CACHE_TTL_SECONDS:
            mapid = map_id.get("mapid")
            token = map_id.get("token")
            if isinstance(mapid, str) and isinstance(token, str):
                url = f"https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}"
                return TileUrlTemplate(url=url)

    try:
        logger.info(f"Calling image.getMapId with vis_params: {vis_params}")
        map_id = image.getMapId(vis_params)
        logger.info(f"getMapId returned: {type(map_id)}")
    except Exception as e:
        logger.error(f"Failed to call image.getMapId: {e}", exc_info=True)
        raise DataUnavailableError("Failed to generate Earth Engine tile URL") from e

    # Prefer the canonical URL format when available. The Earth Engine Python API often
    # returns a tile_fetcher with a fully-formed url_format including token handling.
    try:
        tile_fetcher = map_id.get("tile_fetcher") if isinstance(map_id, dict) else None
        url_format = getattr(tile_fetcher, "url_format", None)
        if isinstance(url_format, str) and "{z}" in url_format and "{x}" in url_format and "{y}" in url_format:
            if isinstance(map_id, dict):
                _MAPID_CACHE[key] = (time.time(), map_id)
            return TileUrlTemplate(url=url_format)
    except Exception:
        # Fall back to mapid/token assembly below.
        pass

    if isinstance(map_id, dict):
        _MAPID_CACHE[key] = (time.time(), map_id)

    mapid = map_id.get("mapid")
    token = map_id.get("token")
    if not isinstance(mapid, str) or not isinstance(token, str) or not token:
        raise DataUnavailableError("Earth Engine returned invalid map id")

    url = f"https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}"
    return TileUrlTemplate(url=url)
