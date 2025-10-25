"""Tests for CLI configuration management."""

import os
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
from pydantic import ValidationError

from metaexpert.cli.core.config import CLIConfig


def test_default_config_values():
    """Test loading configuration with default values."""
    config = CLIConfig()
    
    assert config.verbose is False
    assert config.no_color is False
    assert config.output_format == "table"
    assert config.default_exchange == "binance"
    assert config.default_strategy == "template"
    assert config.pid_dir == Path.cwd()
    assert config.log_dir == Path("logs")
    assert config.template_dir is None


def test_load_default_config():
    """Test loading configuration using the load method."""
    config = CLIConfig.load()
    
    assert isinstance(config, CLIConfig)
    assert config.verbose is False
    assert config.output_format == "table"


def test_config_with_env_vars(monkeypatch):
    """Test configuration values can be overridden with environment variables."""
    # Set environment variables
    monkeypatch.setenv("METAEXPERT_CLI_VERBOSE", "true")
    monkeypatch.setenv("METAEXPERT_CLI_OUTPUT_FORMAT", "json")
    monkeypatch.setenv("METAEXPERT_CLI_DEFAULT_EXCHANGE", "bybit")
    
    config = CLIConfig()
    
    assert config.verbose is True
    assert config.output_format == "json"
    assert config.default_exchange == "bybit"


def test_config_with_env_vars_false_values(monkeypatch):
    """Test configuration handles false boolean values from environment variables."""
    monkeypatch.setenv("METAEXPERT_CLI_VERBOSE", "false")
    monkeypatch.setenv("METAEXPERT_CLI_NO_COLOR", "false")
    
    config = CLIConfig()
    
    assert config.verbose is False
    assert config.no_color is False


def test_config_with_env_vars_path_values(monkeypatch):
    """Test configuration handles Path values from environment variables."""
    monkeypatch.setenv("METAEXPERT_CLI_PID_DIR", "/tmp/test_pid")
    monkeypatch.setenv("METAEXPERT_CLI_LOG_DIR", "/tmp/test_logs")
    
    config = CLIConfig()
    
    assert config.pid_dir == Path("/tmp/test_pid")
    assert config.log_dir == Path("/tmp/test_logs")


def test_config_validation_error_invalid_types():
    """Test configuration validation with invalid types."""
    # Test invalid boolean value
    with pytest.raises(ValidationError):
        CLIConfig(verbose="not_a_boolean")
    
    # Test invalid output format type
    with pytest.raises(ValidationError):
        CLIConfig(output_format=123)


def test_config_ensure_dir_exists(mocker):
    """Test that directories are created when they don't exist."""
    mock_mkdir = mocker.patch("pathlib.Path.mkdir")
    
    # Create config with custom paths
    config = CLIConfig(
        pid_dir=Path("/tmp/test_pid"),
        log_dir=Path("/tmp/test_logs")
    )
    
    # Verify that mkdir was called for both directories
    assert mock_mkdir.call_count == 2
    assert config.pid_dir == Path("/tmp/test_pid")
    assert config.log_dir == Path("/tmp/test_logs")


def test_save_config_to_file(mocker):
    """Test saving configuration to a file."""
    # Mock file operations
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)
    
    config = CLIConfig(
        verbose=True,
        output_format="json",
        default_exchange="bybit"
    )
    
    # Save to specific path
    test_path = Path("/tmp/test_config")
    config.save(test_path)
    
    # Verify file was opened with correct path
    mock_file.assert_called_once_with(test_path, "w")
    
    # Verify the content written to the file
    handle = mock_file()
    expected_calls = [
        mocker.call("METAEXPERT_CLI_VERBOSE=True\n"),
        mocker.call("METAEXPERT_CLI_NO_COLOR=False\n"),
        mocker.call("METAEXPERT_CLI_OUTPUT_FORMAT=json\n"),
        mocker.call("METAEXPERT_CLI_DEFAULT_EXCHANGE=bybit\n"),
        mocker.call("METAEXPERT_CLI_DEFAULT_STRATEGY=template\n"),
        mocker.call("METAEXPERT_CLI_PID_DIR=" + str(Path.cwd()) + "\n"),
        mocker.call("METAEXPERT_CLI_LOG_DIR=logs\n"),
    ]
    handle.write.assert_has_calls(expected_calls, any_order=True)


def test_save_config_to_default_path(mocker):
    """Test saving configuration to the default path."""
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)
    
    config = CLIConfig(verbose=True)
    config.save()
    
    # Verify file was opened with default path
    expected_path = Path.cwd() / ".metaexpert"
    mock_file.assert_called_once_with(expected_path, "w")


def test_load_config_from_file(monkeypatch, tmp_path, mocker):
    """Test loading configuration from a file."""
    # Create a temporary config file
    config_file = tmp_path / ".metaexpert"
    config_file.write_text(
        "METAEXPERT_CLI_VERBOSE=true\n"
        "METAEXPERT_CLI_OUTPUT_FORMAT=json\n"
        "METAEXPERT_CLI_DEFAULT_EXCHANGE=bybit\n"
    )
    
    # Set up environment to prevent loading from environment variables
    monkeypatch.delenv("METAEXPERT_CLI_VERBOSE", raising=False)
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
        assert config.verbose is True
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
    assert config.verbose is False
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
    
    assert "verbose" in field_info
    assert field_info["verbose"].description == "Verbose output"
    
    assert "no_color" in field_info
    assert field_info["no_color"].description == "Disable colored output"
    
    assert "output_format" in field_info
    assert field_info["output_format"].description == "Default output format"
    
    assert "default_exchange" in field_info
    assert field_info["default_exchange"].description == "Default exchange"
    
    assert "default_strategy" in field_info
    assert field_info["default_strategy"].description == "Default strategy"
    
    assert "pid_dir" in field_info
    assert field_info["pid_dir"].description == "PID files directory"
    
    assert "log_dir" in field_info
    assert field_info["log_dir"].description == "Logs directory"
    
    assert "template_dir" in field_info
    assert field_info["template_dir"].description == "Custom template directory"