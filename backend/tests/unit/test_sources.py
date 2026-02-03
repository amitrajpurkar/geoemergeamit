from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from backend.src.infra.sources import load_sources_config


def test_load_sources_config_parses_mappings(tmp_path: Path) -> None:
    p = tmp_path / "sources.yaml"
    p.write_text(
        dedent(
            """
            datasets:
              foo: "https://example.com/foo.zip"
            googleearthengine:
              projectid: "p"
              token: "t"
            eeimagesets:
              vegetation: "COPERNICUS/S2"
            """
        ).strip(),
        encoding="utf-8",
    )

    cfg = load_sources_config(p)
    assert cfg.datasets["foo"].startswith("https://")
    assert cfg.googleearthengine.projectid == "p"
    assert cfg.googleearthengine.token == "t"
    assert cfg.eeimagesets["vegetation"]


def test_load_sources_config_rejects_non_mapping(tmp_path: Path) -> None:
    p = tmp_path / "sources.yaml"
    p.write_text("- not-a-mapping\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_sources_config(p)
