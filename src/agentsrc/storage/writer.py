import json
from datetime import datetime, timezone
from pathlib import Path

from agentsrc.models import PackageManifest, ProjectIndex, ProjectPackage


class StorageWriter:
    def __init__(self, root_dir: str = ".agentsrc"):
        self.root = Path(root_dir)
        self.pypi_dir = self.root / "pypi"
        self.cache_dir = self.root / "cache"
        self.sources_path = self.root / "sources.json"

    def initialize_structure(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.pypi_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.initialize_sources()

    def initialize_sources(self):
        if not self.sources_path.exists():
            now_iso = datetime.now(timezone.utc).isoformat()
            index = ProjectIndex(generated_at=now_iso, packages=[])
            with open(self.sources_path, "w", encoding="utf-8") as f:
                f.write(index.model_dump_json(indent=2))

    def write_config(self, config_toml_content: str):
        config_path = self.root / "config.toml"
        if config_path.exists():
            raise FileExistsError(f"Config file {config_path} already exists.")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_toml_content)

    def write_instructions(self, content: str):
        inst_path = self.root / "instructions.md"
        if inst_path.exists():
            # If it's the exact same content, we can skip or ignore,
            # but for safety we'll just check if it exists in init command
            pass
        with open(inst_path, "w", encoding="utf-8") as f:
            f.write(content)

    def write_manifest(self, manifest: PackageManifest):
        pkg_dir = self.pypi_dir / manifest.name / manifest.version
        pkg_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = pkg_dir / "manifest.json"

        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest.model_dump_json(indent=2))

        return manifest_path

    def write_analysis(self, manifest: PackageManifest, symbol_map, summary_md: str):
        pkg_dir = self.pypi_dir / manifest.name / manifest.version
        pkg_dir.mkdir(parents=True, exist_ok=True)

        symbols_path = pkg_dir / "symbols.json"
        with open(symbols_path, "w", encoding="utf-8") as f:
            f.write(symbol_map.model_dump_json(indent=2))

        summary_path = pkg_dir / "summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_md)

        self.update_sources_index(manifest)

    def update_sources_index(self, manifest: PackageManifest):
        # Use timezone-aware UTC now
        now_iso = datetime.now(timezone.utc).isoformat()
        index = ProjectIndex(generated_at=now_iso)
        if self.sources_path.exists():
            try:
                with open(self.sources_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    index = ProjectIndex.model_validate(data)
            except Exception:
                pass

        pkg_dir = self.pypi_dir / manifest.name / manifest.version
        rel_pkg_dir = pkg_dir.relative_to(self.root.parent)

        new_pkg = ProjectPackage(
            name=manifest.name,
            version=manifest.version,
            ecosystem=manifest.ecosystem,
            path=str(rel_pkg_dir).replace("\\", "/"),
            manifest=str(rel_pkg_dir / "manifest.json").replace("\\", "/"),
            summary=str(rel_pkg_dir / "summary.md").replace("\\", "/"),
            symbols=str(rel_pkg_dir / "symbols.json").replace("\\", "/"),
        )

        # Replace or add
        packages = []
        found = False
        for pkg in index.packages:
            if pkg.name == new_pkg.name:
                packages.append(new_pkg)
                found = True
            else:
                packages.append(pkg)

        if not found:
            packages.append(new_pkg)

        index.packages = packages
        index.generated_at = now_iso

        with open(self.sources_path, "w", encoding="utf-8") as f:
            f.write(index.model_dump_json(indent=2))
