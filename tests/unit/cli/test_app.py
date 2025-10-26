"""Tests for the MetaExpert CLI application."""

import pytest
from typer.testing import CliRunner

from metaexpert.cli.app import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CliRunner instance for testing."""
    return CliRunner()


def test_app_version(cli_runner: CliRunner) -> None:
    """Test that the --version option works correctly."""
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "MetaExpert" in result.stdout


def test_app_help(cli_runner: CliRunner) -> None:
    """Test that the --help option works correctly."""
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "Manage your trading bots with ease" in result.stdout


def test_app_verbose_flag(cli_runner: CliRunner) -> None:
    """Test that the --verbose flag is accepted."""
    result = cli_runner.invoke(app, ["--verbose", "--help"])
    assert result.exit_code == 0
    # The verbose flag itself doesn't change the output of --help,
    # but it should be accepted without error.
