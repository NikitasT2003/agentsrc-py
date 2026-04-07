from pathlib import Path

import requests

from agentsrc.fetch.cache import CacheManager
from agentsrc.models import PackageManifest


class ArtifactFetcher:
    def __init__(self, cache: CacheManager):
        self.cache = cache

    def download(self, manifest: PackageManifest) -> Path:
        if not manifest.artifact_url:
            raise ValueError(f"No artifact URL for {manifest.name}")

        # Use filename as hash if sha256 is missing
        cache_key = manifest.artifact_hash or manifest.artifact_filename
        cached_path = self.cache.get_path(cache_key)

        if self.cache.is_cached(cache_key):
            return cached_path

        # Download
        with requests.get(manifest.artifact_url, stream=True) as r:
            r.raise_for_status()
            with open(cached_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Verify
        if manifest.artifact_hash:
            if not self.cache.verify_hash(str(cached_path), manifest.artifact_hash):
                cached_path.unlink(missing_ok=True)
                raise ValueError("Hash verification failed")

        return cached_path
