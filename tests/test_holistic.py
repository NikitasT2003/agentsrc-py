import os

from typer.testing import CliRunner

from agentsrc.analysis.ast_symbols import ASTAnalyzer
from agentsrc.analysis.plugins.pydantic import PydanticPlugin
from agentsrc.cli import app
from agentsrc.resolver import ProjectResolver

runner = CliRunner()


def test_init_fresh_directory(tmp_path):
    # Change to tmp_path to simulate a fresh directory
    os.chdir(tmp_path)

    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0

    assert (tmp_path / ".agentsrc").exists()
    assert (tmp_path / ".agentsrc" / "config.toml").exists()
    assert (tmp_path / ".agentsrc" / "instructions.md").exists()
    assert (tmp_path / ".agentsrc" / "sources.json").exists()


def test_resolve_from_requirements_txt(tmp_path):
    os.chdir(tmp_path)
    reqs = tmp_path / "requirements.txt"
    reqs.write_text("requests==2.32.3\nrich>=13.0.0")

    resolver = ProjectResolver()
    # We need to ensure ProjectResolver checks requirements.txt if passed or present
    packages = resolver.resolve_all(prefer_venv=False, prefer_lockfile=False)

    names = [p["name"] for p in packages]
    assert "requests" in names
    assert "rich" in names


def test_resolve_from_pyproject_toml(tmp_path):
    os.chdir(tmp_path)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
dependencies = [
    "pydantic>=2.0.0",
]
""")

    resolver = ProjectResolver()
    packages = resolver.resolve_all(prefer_venv=False, prefer_lockfile=False)

    names = [p["name"] for p in packages]
    assert "pydantic" in names


def test_resolve_from_uv_lock(tmp_path):
    os.chdir(tmp_path)
    uv_lock = tmp_path / "uv.lock"
    # Simplified uv.lock format for testing
    uv_lock.write_text("""
[[package]]
name = "fastapi"
version = "0.115.0"
""")

    resolver = ProjectResolver()
    packages = resolver.resolve_all(prefer_venv=False, prefer_lockfile=True)

    names = [p["name"] for p in packages]
    assert "fastapi" in names


def test_pydantic_plugin_detection(tmp_path):
    # Mock a file with a Pydantic model
    src = tmp_path / "models.py"
    src.write_text("""
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
""")

    analyzer = ASTAnalyzer()
    symbol_map = analyzer.analyze_directory(str(tmp_path))

    # Check if Pydantic plugin detected it
    plugin = PydanticPlugin()
    findings = plugin.analyze(str(tmp_path), symbol_map)

    assert "User" in [f.get("name") for f in findings.get("models", [])]


def test_query_search_logic(tmp_path):
    # This requires a synced package. We can mock the Storage structure.
    os.chdir(tmp_path)
    runner.invoke(app, ["init"])

    # Mock a synced package in .agentsrc/pypi/testpkg/1.0.0
    pkg_dir = tmp_path / ".agentsrc" / "pypi" / "testpkg" / "1.0.0"
    pkg_dir.mkdir(parents=True)

    symbols_file = pkg_dir / "symbols.json"
    symbols_file.write_text("""
{
  "classes": [{"name": "MyClient", "module": "testpkg.client"}],
  "functions": [{"name": "process", "module": "testpkg.core"}]
}
""")

    manifest_file = pkg_dir / "manifest.json"
    manifest_file.write_text('{"name": "testpkg", "version": "1.0.0", "summary": "A test package"}')

    # Update sources.json
    sources_file = tmp_path / ".agentsrc" / "sources.json"
    sources_file.write_text("""
{
  "packages": [
    {
      "name": "testpkg",
      "version": "1.0.0",
      "path": ".agentsrc/pypi/testpkg/1.0.0",
      "symbols": ".agentsrc/pypi/testpkg/1.0.0/symbols.json"
    }
  ]
}
""")

    # Run query search
    result = runner.invoke(app, ["query", "search", "MyClient"])
    assert result.exit_code == 0
    assert "MyClient" in result.output
