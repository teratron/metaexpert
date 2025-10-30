"""Tests for MetaExpert logger configuration."""

from pathlib import Path

import pytest

from metaexpert.logger.config import LoggerConfig


def test_logger_config_defaults():
    """Test default configuration values."""
    config = LoggerConfig()

    assert config.log_level == "DEBUG"
    assert config.log_to_console is True
    assert config.log_to_file is True
    assert config.log_dir == Path("logs")
    assert config.log_file == "expert.log"
    assert config.log_trade_file == "trades.log"
    assert config.log_error_file == "errors.log"
    assert config.max_bytes == 10 * 1024 * 1024  # 10MB
    assert config.backup_count == 5
    assert config.use_colors is True
    assert config.json_logging is False
    assert config.cache_logger_on_first_use is True


def test_logger_config_custom_values():
    """Test configuration with custom values."""
    custom_config = LoggerConfig(
        log_level="DEBUG",
        log_to_console=False,
        log_to_file=True,
        log_dir=Path("/custom/logs"),
        log_file="custom.log",
        log_trade_file="custom_trades.log",
        log_error_file="custom_errors.log",
        max_bytes=5 * 1024 * 1024,  # 5MB
        backup_count=10,
        use_colors=False,
        json_logging=True,
        cache_logger_on_first_use=False,
    )

    assert custom_config.log_level == "DEBUG"
    assert custom_config.log_to_console is False
    assert custom_config.log_to_file is True
    assert custom_config.log_dir == Path("/custom/logs")
    assert custom_config.log_file == "custom.log"
    assert custom_config.log_trade_file == "custom_trades.log"
    assert custom_config.log_error_file == "custom_errors.log"
    assert custom_config.max_bytes == 5 * 1024 * 1024
    assert custom_config.backup_count == 10
    assert custom_config.use_colors is False
    assert custom_config.json_logging is True
    assert custom_config.cache_logger_on_first_use is False


def test_logger_config_log_dir_creation():
    """Test that log directory is created if it doesn't exist."""
    test_dir = Path("test_logs")

    # Ensure the directory doesn't exist initially
    if test_dir.exists():
        test_dir.rmdir()

    LoggerConfig(log_dir=test_dir)

    # The directory should now exist
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_logger_config_max_bytes_validation_positive():
    """Test validation of max_bytes field with positive values."""
    # Valid values should not raise an exception
    valid_values = [1, 1024, 10 * 1024 * 1024]  # 1 byte, 1KB, 10MB

    for value in valid_values:
        config = LoggerConfig(max_bytes=value)
        assert config.max_bytes == value


def test_logger_config_max_bytes_validation_negative():
    """Test validation of max_bytes field with negative values."""
    # Invalid values should raise ValueError
    invalid_values = [0, -1, -100]

    for value in invalid_values:
        with pytest.raises(ValueError, match="max_bytes must be positive"):
            LoggerConfig(max_bytes=value)


def test_logger_config_max_bytes_validation_too_large():
    """Test validation of max_bytes field with values exceeding 1GB."""
    # Values larger than 1GB should raise ValueError
    too_large_values = [
        1024 * 1024 * 1024 + 1,
        2 * 1024 * 1024 * 1024,
    ]  # 1GB + 1 byte, 2GB

    for value in too_large_values:
        with pytest.raises(ValueError, match="max_bytes must not exceed 1GB"):
            LoggerConfig(max_bytes=value)


def test_logger_config_immutability():
    """Test that configuration is immutable after creation."""
    LoggerConfig()

    # Attempting to modify should raise ValidationError due to Pydantic
    with pytest.raises(
        (ValueError, TypeError)
    ):  # Could be ValidationError or TypeError
        LoggerConfig().log_level = "DEBUG"

    with pytest.raises(
        (ValueError, TypeError)
    ):  # Could be ValidationError or TypeError
        LoggerConfig().log_to_console = False
