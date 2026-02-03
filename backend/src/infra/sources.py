from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class GoogleEarthEngineConfig:
    projectid: str | None
    token: str | None


@dataclass(frozen=True)
class SourcesConfig:
    datasets: dict[str, str]
    eeimagesets: dict[str, str]
    googleearthengine: GoogleEarthEngineConfig


def _as_str_dict(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("Expected mapping")
    out: dict[str, str] = {}
    for k, v in value.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ValueError("Expected string-to-string mapping")
        out[k] = v
    return out


def load_sources_config(path: str | Path) -> SourcesConfig:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ValueError("sources.yaml must be a mapping")

    datasets = _as_str_dict(raw.get("datasets"))
    eeimagesets = _as_str_dict(raw.get("eeimagesets"))

    gee_raw = raw.get("googleearthengine")
    if gee_raw is None:
        gee_raw = {}
    if not isinstance(gee_raw, dict):
        raise ValueError("googleearthengine must be a mapping")

    projectid = gee_raw.get("projectid")
    token = gee_raw.get("token")
    if projectid is not None and not isinstance(projectid, str):
        raise ValueError("googleearthengine.projectid must be a string")
    if token is not None and not isinstance(token, str):
        raise ValueError("googleearthengine.token must be a string")

    return SourcesConfig(
        datasets=datasets,
        eeimagesets=eeimagesets,
        googleearthengine=GoogleEarthEngineConfig(projectid=projectid, token=token),
    )


def default_sources_yaml_path(repo_root: str | Path) -> Path:
    return Path(repo_root) / "resources" / "sources.yaml"
