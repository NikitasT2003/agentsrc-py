import tomllib
from pathlib import Path
from typing import Dict, List


class ProjectResolver:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)

    def resolve_all(
        self, prefer_venv: bool = True, prefer_lockfile: bool = True
    ) -> List[Dict[str, str]]:
        packages = {}  # name -> version

        # 1. Active Environment
        if prefer_venv:
            venv_pkgs = self.resolve_from_venv()
            for name, version in venv_pkgs.items():
                if name not in packages:
                    packages[name] = version

        # 2. uv.lock
        uv_lock = self.root / "uv.lock"
        if uv_lock.exists():
            lock_pkgs = self.resolve_from_uv_lock(uv_lock)
            for name, version in lock_pkgs.items():
                if name not in packages:
                    packages[name] = version

        # 3. pyproject.toml
        pyproject = self.root / "pyproject.toml"
        if pyproject.exists():
            py_pkgs = self.resolve_from_pyproject(pyproject)
            for name, version in py_pkgs.items():
                if name not in packages:
                    packages[name] = version

        # 4. requirements.txt
        reqs = self.root / "requirements.txt"
        if reqs.exists():
            req_pkgs = self.resolve_from_requirements_txt(reqs)
            for name, version in req_pkgs.items():
                if name not in packages:
                    packages[name] = version

        # Filter out the current project itself
        project_name = self.get_project_name().lower()

        # Convert to list of dicts, filtering out the project
        return [
            {"name": name, "version": version}
            for name, version in packages.items()
            if name != project_name
        ]

    def get_project_name(self) -> str:
        pyproject = self.root / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("name", "")
            except Exception:
                pass
        return ""

    def resolve_from_venv(self) -> Dict[str, str]:
        import importlib.metadata

        pkgs = {}
        for dist in importlib.metadata.distributions():
            name = dist.metadata.get("Name")
            if name:
                pkgs[name.lower()] = dist.version
        return pkgs

    def resolve_from_uv_lock(self, path: Path) -> Dict[str, str]:
        pkgs = {}
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
                for pkg in data.get("package", []):
                    # We only care about registry packages for now, skip editables or local paths if needed
                    # but for v1 we'll take all named packages
                    name = pkg.get("name")
                    version = pkg.get("version")
                    if name and version:
                        pkgs[name.lower()] = version
        except Exception:
            pass
        return pkgs

    def resolve_from_pyproject(self, path: Path) -> Dict[str, str]:
        pkgs = {}
        try:
            from packaging.requirements import Requirement

            with open(path, "rb") as f:
                data = tomllib.load(f)
                deps = data.get("project", {}).get("dependencies", [])
                for dep in deps:
                    req = Requirement(dep)
                    # For pyproject.toml, versions might be ranges.
                    # This resolver is meant to find CONCRETE versions.
                    # If it's just a specifier, we might need to rely on the lockfile or venv.
                    # So we only take pinned versions if possible, or just the name.
                    # But the venv/lockfile resolution will likely override this anyway.
                    name = req.name.lower()
                    if name not in pkgs:
                        pkgs[name] = "latest"  # Placeholder if unpinned
        except Exception:
            pass
        return pkgs
    def resolve_from_requirements_txt(self, path: Path) -> Dict[str, str]:
        pkgs = {}
        try:
            from packaging.requirements import Requirement

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        req = Requirement(line)
                        name = req.name.lower()
                        # Extract exact version if present (e.g. requests==2.32.3)
                        # Otherwise use "latest"
                        version = "latest"
                        for spec in req.specifier:
                            if spec.operator == "==":
                                version = spec.version
                                break
                        pkgs[name] = version
                    except Exception:
                        continue
        except Exception:
            pass
        return pkgs
