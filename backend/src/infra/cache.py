from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import time
from typing import Any


@dataclass(frozen=True)
class CachePaths:
    base_dir: Path

    def ensure(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def subdir(self, *parts: str) -> Path:
        path = self.base_dir.joinpath(*parts)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def file_path(self, *parts: str) -> Path:
        if not parts:
            raise ValueError("At least one path part is required")
        directory = self.subdir(*parts[:-1])
        return directory / parts[-1]


def default_cache_dir(repo_root: str | Path) -> Path:
    return Path(repo_root) / ".cache" / "geoemerge"


def cache_paths(repo_root: str | Path) -> CachePaths:
    paths = CachePaths(base_dir=default_cache_dir(repo_root))
    paths.ensure()
    return paths


def is_fresh(path: Path, *, ttl_seconds: int) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age <= ttl_seconds


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
