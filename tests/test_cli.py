import pytest
from typer.testing import CliRunner
from agentsrc.cli import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "sync" in result.stdout
