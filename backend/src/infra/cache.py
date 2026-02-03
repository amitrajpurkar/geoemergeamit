from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
