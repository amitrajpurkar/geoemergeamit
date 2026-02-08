from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from backend.src.infra.sources import load_sources_config, merge_local_auth_token


def test_load_sources_config_parses_mappings_and_merges_local_auth(tmp_path: Path) -> None:
    repo_root = tmp_path
    sources_path = repo_root / "resources" / "sources.yaml"
    sources_path.parent.mkdir(parents=True, exist_ok=True)
    sources_path.write_text(
        dedent(
            """
            datasets:
              foo: "https://example.com/foo.zip"
            googleearthengine: {}
            eeimagesets:
              vegetation: "COPERNICUS/S2"
            """
        ).strip(),
        encoding="utf-8",
    )

    auth_path = repo_root / "env" / "local-auth.yaml"
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    auth_path.write_text(
        dedent(
            """
            googleearthengine:
              projectid: "p"
              token: "t"
            """
        ).strip(),
        encoding="utf-8",
    )

    cfg = load_sources_config(sources_path)
    cfg = merge_local_auth_token(cfg, repo_root=repo_root)
    assert cfg.datasets["foo"].startswith("https://")
    assert cfg.googleearthengine.projectid == "p"
    assert cfg.googleearthengine.token == "t"
    assert cfg.eeimagesets["vegetation"]


def test_load_sources_config_rejects_non_mapping(tmp_path: Path) -> None:
    p = tmp_path / "sources.yaml"
    p.write_text("- not-a-mapping\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_sources_config(p)
