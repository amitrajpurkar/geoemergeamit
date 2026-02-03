from __future__ import annotations

import hashlib
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from backend.src.domain.errors import DataUnavailableError
from backend.src.infra.cache import CachePaths


@dataclass(frozen=True)
class DatasetArtifact:
    name: str
    url: str
    local_path: Path


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# TODO: try streaming download to avoid loading entire file into memory
def download_to_cache(url: str, cache: CachePaths, *, subdir: str = "datasets") -> Path:
    target_dir = cache.subdir(subdir)
    filename = Path(urllib.parse.urlparse(url).path).name or _sha256(url)
    dest = target_dir / filename

    if dest.exists() and dest.stat().st_size > 0:
        return dest

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        dest.write_bytes(data)
        return dest
    except Exception as e:
        raise DataUnavailableError(f"Failed to download dataset from {url}") from e

# TODO: try safe zip extraction to avoid path traversal attacks; zip-slip vulnerability
def extract_zip(zip_path: Path, cache: CachePaths, *, subdir: str) -> Path:
    out_dir = cache.subdir(subdir)
    try:
        with ZipFile(zip_path) as zf:
            zf.extractall(out_dir)
    except Exception as e:
        raise DataUnavailableError(f"Failed to extract zip {zip_path}") from e
    return out_dir


def prepare_dataset(name: str, url: str, cache: CachePaths) -> DatasetArtifact:
    downloaded = download_to_cache(url, cache)
    suffix = downloaded.suffix.lower()

    if suffix == ".zip":
        extracted_dir = extract_zip(downloaded, cache, subdir=f"datasets/{name}")
        return DatasetArtifact(name=name, url=url, local_path=extracted_dir)

    return DatasetArtifact(name=name, url=url, local_path=downloaded)
