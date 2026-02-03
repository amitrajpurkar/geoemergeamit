from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisualizationSpec:
    title: str
    caption: str | None = None


def ensure_labeled(spec: VisualizationSpec) -> VisualizationSpec:
    if not spec.title.strip():
        raise ValueError("Visualization title is required")
    return spec
