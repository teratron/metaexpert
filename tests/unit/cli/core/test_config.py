"""Tests for CLI configuration management."""

import os
from pathlib import Path
from unittest.mock import mock_open

import pytest
from pydantic import ValidationError

from metaexpert.cli.core.config import CLIConfig


def test_default_config_values():
    """Test loading configuration with default values."""
    config = CLIConfig()

    assert config.debug is False
    assert config.verbose is False
    assert config.quiet is False
    assert config.log_level == "INFO"
    assert config.log_file is None
    assert config.log_max_size == "10MB"
    assert config.log_backup_count == 5
    assert config.no_color is False
    assert config.output_format == "table"
    assert config.default_exchange == "binance"
    assert config.default_strategy == "template"
    assert config.default_timeout == 30
    assert config.pid_dir == Path.cwd()
    assert config.pid_file_suffix == ".pid"
    assert config.log_dir == Path("logs")
    assert config.template_dir is None
    assert config.cache_enabled is True
    assert config.cache_ttl == 300
    assert config.max_workers == 4
    assert config.api_timeout == 10
    assert config.api_retries == 3
    assert config.api_delay == 0.1


def test_load_default_config():
    """Test loading configuration using the load method."""
    config = CLIConfig.load()

    assert isinstance(config, CLIConfig)
    assert config.debug is False
    assert config.log_level == "INFO"


def test_config_with_env_vars(monkeypatch):
    """Test configuration values can be overridden with environment variables."""
    # Set environment variables
    monkeypatch.setenv("METAEXPERT_CLI_DEBUG", "true")
    monkeypatch.setenv("METAEXPERT_CLI_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("METAEXPERT_CLI_OUTPUT_FORMAT", "json")
    monkeypatch.setenv("METAEXPERT_CLI_DEFAULT_EXCHANGE", "bybit")
    monkeypatch.setenv("METAEXPERT_CLI_MAX_WORKERS", "8")

    config = CLIConfig()

    assert config.debug is True
    assert config.log_level == "DEBUG"
    assert config.output_format == "json"
    assert config.default_exchange == "bybit"
    assert config.max_workers == 8


def test_config_with_env_vars_false_values(monkeypatch):
    """Test configuration handles false boolean values from environment variables."""
    monkeypatch.setenv("METAEXPERT_CLI_DEBUG", "false")
    monkeypatch.setenv("METAEXPERT_CLI_VERBOSE", "false")
    monkeypatch.setenv("METAEXPERT_CLI_CACHE_ENABLED", "false")

    config = CLIConfig()

    assert config.debug is False
    assert config.verbose is False
    assert config.cache_enabled is False


def test_config_with_env_vars_path_values(monkeypatch):
    """Test configuration handles Path values from environment variables."""
    monkeypatch.setenv("METAEXPERT_CLI_PID_DIR", "/tmp/test_pid")
    monkeypatch.setenv("METAEXPERT_CLI_LOG_DIR", "/tmp/test_logs")
    monkeypatch.setenv("METAEXPERT_CLI_LOG_FILE", "/tmp/app.log")

    config = CLIConfig()

    assert config.pid_dir == Path("/tmp/test_pid")
    assert config.log_dir == Path("/tmp/test_logs")
    assert config.log_file == Path("/tmp/app.log")


def test_config_validation_error_invalid_types():
    """Test configuration validation with invalid types."""
    # Test invalid boolean value
    with pytest.raises(ValidationError):
        CLIConfig(debug="not_a_boolean")

    # Test invalid output format type
    with pytest.raises(ValidationError):
        CLIConfig(output_format=123)

    # Test invalid log level
    with pytest.raises(ValidationError):
        CLIConfig(log_level="INVALID_LEVEL")


def test_config_ensure_dir_exists(mocker):
    """Test that directories are created when they don't exist."""
    mock_mkdir = mocker.patch("pathlib.Path.mkdir")

    # Create config with custom paths
    config = CLIConfig(
        pid_dir=Path("/tmp/test_pid"),
        log_file=Path("/tmp/test_logs/app.log"),
        template_dir=Path("/tmp/templates"),
    )

    # Verify that mkdir was called for directories
    assert mock_mkdir.call_count >= 2  # Called for parent of log_file and template_dir
    assert config.pid_dir == Path("/tmp/test_pid")
    assert config.log_file == Path("/tmp/test_logs/app.log")
    assert config.template_dir == Path("/tmp/templates")


def test_config_validate_log_level():
    """Test that log level validation works correctly."""
    # Valid log levels
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "debug", "info"]:
        config = CLIConfig(log_level=level)
        assert config.log_level == level.upper()

    # Invalid log level
    with pytest.raises(ValidationError):
        CLIConfig(log_level="INVALID")


def test_save_config_to_file(mocker):
    """Test saving configuration to a file."""
    # Mock file operations
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)

    config = CLIConfig(
        debug=True,
        output_format="json",
        default_exchange="bybit",
        log_file=Path("/tmp/app.log"),
    )

    # Save to specific path
    test_path = Path("/tmp/test_config")
    config.save(test_path)

    # Verify file was opened with correct path
    mock_file.assert_called_once_with(test_path, "w")

    # Verify the content written to the file
    handle = mock_file()
    expected_calls = [
        mocker.call("METAEXPERT_CLI_DEBUG=True\n"),
        mocker.call("METAEXPERT_CLI_VERBOSE=False\n"),
        mocker.call("METAEXPERT_CLI_QUIET=False\n"),
        mocker.call("METAEXPERT_CLI_LOG_LEVEL=INFO\n"),
        mocker.call("METAEXPERT_CLI_LOG_FILE=/tmp/app.log\n"),
        mocker.call("METAEXPERT_CLI_LOG_MAX_SIZE=10MB\n"),
        mocker.call("METAEXPERT_CLI_LOG_BACKUP_COUNT=5\n"),
        mocker.call("METAEXPERT_CLI_NO_COLOR=False\n"),
        mocker.call("METAEXPERT_CLI_OUTPUT_FORMAT=json\n"),
        mocker.call("METAEXPERT_CLI_DEFAULT_EXCHANGE=bybit\n"),
        mocker.call("METAEXPERT_CLI_DEFAULT_STRATEGY=template\n"),
        mocker.call("METAEXPERT_CLI_DEFAULT_TIMEOUT=30\n"),
        mocker.call("METAEXPERT_CLI_PID_DIR=" + Path.cwd().as_posix() + "\n"),
        mocker.call("METAEXPERT_CLI_PID_FILE_SUFFIX=.pid\n"),
        mocker.call("METAEXPERT_CLI_LOG_DIR=logs\n"),
        mocker.call("METAEXPERT_CLI_TEMPLATE_DIR=None\n"),
        mocker.call("METAEXPERT_CLI_CACHE_ENABLED=True\n"),
        mocker.call("METAEXPERT_CLI_CACHE_TTL=300\n"),
        mocker.call("METAEXPERT_CLI_MAX_WORKERS=4\n"),
        mocker.call("METAEXPERT_CLI_API_TIMEOUT=10\n"),
        mocker.call("METAEXPERT_CLI_API_RETRIES=3\n"),
        mocker.call("METAEXPERT_CLI_API_DELAY=0.1\n"),
    ]
    handle.write.assert_has_calls(expected_calls, any_order=True)


def test_save_config_to_default_path(mocker):
    """Test saving configuration to the default path."""
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)

    config = CLIConfig(debug=True)
    config.save()

    # Verify file was opened with default path
    expected_path = Path.cwd() / ".metaexpert"
    mock_file.assert_called_once_with(expected_path, "w")


def test_load_config_from_file(monkeypatch, tmp_path, mocker):
    """Test loading configuration from a file."""
    # Create a temporary config file
    config_file = tmp_path / ".metaexpert"
    config_file.write_text(
        "METAEXPERT_CLI_DEBUG=true\n"
        "METAEXPERT_CLI_LOG_LEVEL=DEBUG\n"
        "METAEXPERT_CLI_OUTPUT_FORMAT=json\n"
        "METAEXPERT_CLI_DEFAULT_EXCHANGE=bybit\n"
    )

    # Set up environment to prevent loading from environment variables
    monkeypatch.delenv("METAEXPERT_CLI_DEBUG", raising=False)
    monkeypatch.delenv("METAEXPERT_CLI_LOG_LEVEL", raising=False)
    monkeypatch.delenv("METAEXPERT_CLI_OUTPUT_FORMAT", raising=False)
    monkeypatch.delenv("METAEXPERT_CLI_DEFAULT_EXCHANGE", raising=False)

    # Change to the temporary directory to make the config file discoverable
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Create a new CLIConfig instance which will load from the config file
        config = CLIConfig()

        # Note: Direct file loading is handled by pydantic_settings through env_file
        # This test ensures that the config can be loaded properly
        assert config.debug is True
        assert config.log_level == "DEBUG"
        assert config.output_format == "json"
        assert config.default_exchange == "bybit"
    finally:
        # Restore the original working directory
        os.chdir(original_cwd)


def test_config_with_nonexistent_file():
    """Test configuration behavior when specified file doesn't exist."""
    # Test that configuration still loads with defaults when file doesn't exist
    config = CLIConfig()

    assert isinstance(config, CLIConfig)
    # Default values should still be present
    assert config.debug is False
    assert config.log_level == "INFO"
    assert config.output_format == "table"


def test_config_template_dir_optional():
    """Test that template_dir can be None or a valid path."""
    # Test with None (default)
    config = CLIConfig()
    assert config.template_dir is None

    # Test with a path
    config_with_path = CLIConfig(template_dir=Path("/tmp/templates"))
    assert config_with_path.template_dir == Path("/tmp/templates")


def test_config_field_descriptions():
    """Test that configuration fields have appropriate descriptions."""
    # This test ensures the field definitions include descriptions
    field_info = CLIConfig.model_fields

    assert "debug" in field_info
    assert field_info["debug"].description == "Enable debug mode"

    assert "verbose" in field_info
    assert field_info["verbose"].description == "Verbose output"

    assert "quiet" in field_info
    assert field_info["quiet"].description == "Suppress non-critical output"

    assert "log_level" in field_info
    assert (
        field_info["log_level"].description
        == "Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    assert "log_file" in field_info
    assert field_info["log_file"].description == "Path to log file"

    assert "log_max_size" in field_info
    assert field_info["log_max_size"].description == "Maximum log file size"

    assert "log_backup_count" in field_info
    assert field_info["log_backup_count"].description == "Number of log backups to keep"

    assert "no_color" in field_info
    assert field_info["no_color"].description == "Disable colored output"

    assert "output_format" in field_info
    assert (
        field_info["output_format"].description
        == "Default output format (table, json, csv)"
    )

    assert "default_exchange" in field_info
    assert field_info["default_exchange"].description == "Default exchange"

    assert "default_strategy" in field_info
    assert field_info["default_strategy"].description == "Default strategy"

    assert "default_timeout" in field_info
    assert (
        field_info["default_timeout"].description
        == "Default timeout for operations in seconds"
    )

    assert "pid_dir" in field_info
    assert field_info["pid_dir"].description == "PID files directory"

    assert "pid_file_suffix" in field_info
    assert field_info["pid_file_suffix"].description == "PID file suffix"

    assert "log_dir" in field_info
    assert field_info["log_dir"].description == "Logs directory"

    assert "template_dir" in field_info
    assert field_info["template_dir"].description == "Custom template directory"

    assert "cache_enabled" in field_info
    assert field_info["cache_enabled"].description == "Enable caching"

    assert "cache_ttl" in field_info
    assert field_info["cache_ttl"].description == "Cache TTL in seconds"

    assert "max_workers" in field_info
    assert field_info["max_workers"].description == "Maximum number of worker threads"

    assert "api_timeout" in field_info
    assert field_info["api_timeout"].description == "API request timeout in seconds"

    assert "api_retries" in field_info
    assert field_info["api_retries"].description == "Number of API request retries"

    assert "api_delay" in field_info
    assert (
        field_info["api_delay"].description == "Delay between API requests in seconds"
    )


def test_get_pid_file_path():
    """Test getting PID file path for a project."""
    config = CLIConfig()
    pid_path = config.get_pid_file_path("my_project")

    assert pid_path == Path.cwd() / "my_project.pid"

    # Test with custom suffix
    config_with_suffix = CLIConfig(pid_file_suffix=".lock")
    pid_path_custom = config_with_suffix.get_pid_file_path("my_project")

    assert pid_path_custom == Path.cwd() / "my_project.lock"


def test_get_log_file_path():
    """Test getting log file path for a project."""
    config = CLIConfig()
    log_path = config.get_log_file_path("my_project")

    assert log_path == Path("logs") / "my_project.log"

    # Test with custom log file
    config_with_file = CLIConfig(log_file=Path("/tmp/app.log"))
    log_path_custom = config_with_file.get_log_file_path("my_project")

    assert log_path_custom == Path("/tmp/app.log")
