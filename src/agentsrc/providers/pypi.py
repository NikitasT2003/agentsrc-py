from datetime import datetime, timezone
from typing import Optional

import requests

from agentsrc.models import PackageManifest


class PyPIClient:
    BASE_URL = "https://pypi.org/pypi"

    def get_package_metadata(self, name: str, version: Optional[str] = None) -> PackageManifest:
        url = f"{self.BASE_URL}/{name}/json"
        if version:
            url = f"{self.BASE_URL}/{name}/{version}/json"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        info = data.get("info", {})
        actual_version = version or info.get("version")

        # Select artifact
        urls: list = data.get("urls", [])
        if version and "releases" in data and version in data["releases"]:
            urls = data["releases"][version]

        sdist = next((u for u in urls if u.get("packagetype") == "sdist"), None)
        wheel = next((u for u in urls if u.get("packagetype") == "bdist_wheel"), None)

        artifact = sdist or wheel
        if not artifact:
            raise ValueError(f"No sdist or wheel found for {name} {actual_version}")

        return PackageManifest(
            name=info.get("name", name),
            version=actual_version,
            normalized_name=name.lower().replace("-", "_"),
            source_type=artifact.get("packagetype", "unknown"),
            artifact_url=artifact.get("url", ""),
            artifact_filename=artifact.get("filename", ""),
            artifact_hash=artifact.get("digests", {}).get("sha256", ""),
            requires_python=info.get("requires_python"),
            summary=info.get("summary"),
            author=info.get("author"),
            license=info.get("license"),
            project_urls=info.get("project_urls") or {},
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
