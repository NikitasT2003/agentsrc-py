import hashlib
from pathlib import Path


class CacheManager:
    def __init__(self, cache_dir: str = ".agentsrc/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def is_cached(self, artifact_hash: str) -> bool:
        if not artifact_hash:
            return False
        return (self.cache_dir / artifact_hash).exists()

    def get_path(self, artifact_hash: str) -> Path:
        return self.cache_dir / artifact_hash

    @staticmethod
    def verify_hash(file_path: str, expected_hash: str) -> bool:
        if not expected_hash:
            return True

        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest() == expected_hash
