from __future__ import annotations

from pathlib import Path

import geopandas as gpd

from backend.src.domain.errors import DataUnavailableError
from backend.src.infra.cache import cache_paths
from backend.src.infra.datasets import prepare_dataset
from backend.src.infra.sources import SourcesConfig


def florida_boundary_geojson_path(*, repo_root: Path, sources: SourcesConfig) -> Path:
    url = sources.datasets.get("floridaboundaries")
    if not url:
        raise DataUnavailableError("Dataset source 'floridaboundaries' is not configured")

    cache = cache_paths(repo_root)
    artifact = prepare_dataset("floridaboundaries", url, cache)
    return artifact.local_path


# TODO: instead of gdf.geometry.unary_union, use a more robust method, eg union_all
def florida_geojson_geometry(*, repo_root: Path, sources: SourcesConfig) -> dict:
    path = florida_boundary_geojson_path(repo_root=repo_root, sources=sources)
    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        raise DataUnavailableError(f"Failed to read Florida boundary from {path}") from e

    if gdf.empty:
        raise DataUnavailableError("Florida boundary dataset is empty")

    geom = gdf.geometry.union_all()
    return geom.__geo_interface__


def florida_ee_geometry(*, repo_root: Path, sources: SourcesConfig):
    try:
        import ee  # type: ignore
    except Exception as e:  # pragma: no cover
        raise DataUnavailableError("earthengine-api is not available") from e

    geojson = florida_geojson_geometry(repo_root=repo_root, sources=sources)
    try:
        return ee.Geometry(geojson)
    except Exception as e:
        raise DataUnavailableError("Failed to convert Florida geometry to Earth Engine geometry") from e
