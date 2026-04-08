from pathlib import Path

from typer.testing import CliRunner

from agentsrc.cli import app

runner = CliRunner()


def test_init_creates_files(tmp_path):
    # Change CWD to tmp_path for the test
    import os

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert Path(".agentsrc/config.toml").exists()
        assert Path(".agentsrc/instructions.md").exists()
    finally:
        os.chdir(old_cwd)


def test_init_fails_if_exists(tmp_path):
    import os

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        os.makedirs(".agentsrc", exist_ok=True)
        Path(".agentsrc/config.toml").write_text("existing", encoding="utf-8")

        result = runner.invoke(app, ["init"])
        # This SHOULD fail or at least not overwrite without warning
        # Currently it overwrites, so this will be RED
        assert "already exists" in result.stdout or result.exit_code != 0
    finally:
        os.chdir(old_cwd)


def test_inject_updates_files(tmp_path):
    import os

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        Path("CLAUDE.md").write_text("# Claude Guidance\n", encoding="utf-8")
        Path("README.md").write_text("# Readme\n", encoding="utf-8")

        result = runner.invoke(app, ["inject"])
        assert result.exit_code == 0
        assert ".agentsrc/instructions.md" in Path("CLAUDE.md").read_text()
        assert ".agentsrc/instructions.md" in Path("README.md").read_text()
    finally:
        os.chdir(old_cwd)


def test_inject_fallback_to_agents_md(tmp_path):
    import os

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # No files exist
        result = runner.invoke(app, ["inject"])
        assert result.exit_code == 0
        assert Path("AGENTS.md").exists()
        assert ".agentsrc/instructions.md" in Path("AGENTS.md").read_text()
    finally:
        os.chdir(old_cwd)
