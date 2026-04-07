import pytest
from pathlib import Path
from agentsrc.resolver import ProjectResolver

def test_resolve_from_uv_lock(tmp_path):
    uv_lock = tmp_path / "uv.lock"
    # Content of a sample uv.lock
    uv_lock.write_text("""
[[package]]
name = "requests"
version = "2.31.0"

[[package]]
name = "pydantic"
version = "2.6.0"
""", encoding="utf-8")
    
    resolver = ProjectResolver(root_dir=str(tmp_path))
    pkgs = resolver.resolve_from_uv_lock(uv_lock)
    
    assert pkgs["requests"] == "2.31.0"
    assert pkgs["pydantic"] == "2.6.0"

def test_resolve_all_merging(tmp_path):
    uv_lock = tmp_path / "uv.lock"
    uv_lock.write_text("""
[[package]]
name = "requests"
version = "2.31.0"
""", encoding="utf-8")
    
    resolver = ProjectResolver(root_dir=str(tmp_path))
    # We mock resolve_from_venv to return something else
    resolver.resolve_from_venv = lambda: {"pydantic": "2.6.0"}
    
    all_pkgs = resolver.resolve_all(prefer_venv=True, prefer_lockfile=True)
    
    # Convert list of dicts back to dict for easy assertion
    pkg_dict = {p["name"]: p["version"] for p in all_pkgs}
    assert pkg_dict["requests"] == "2.31.0"
    assert pkg_dict["pydantic"] == "2.6.0"

def test_resolve_all_excludes_self(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "myproject"
""", encoding="utf-8")
    
    resolver = ProjectResolver(root_dir=str(tmp_path))
    # Mocking environment/lock to include "myproject"
    resolver.resolve_from_venv = lambda: {"myproject": "0.1.0", "requests": "2.31.0"}
    
    all_pkgs = resolver.resolve_all()
    
    pkg_names = [p["name"] for p in all_pkgs]
    assert "requests" in pkg_names
    assert "myproject" not in pkg_names # This should fail initially since name is hardcoded to agentsrc
