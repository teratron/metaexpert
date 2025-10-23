"""Unit tests for LoggerConfig class in src/metaexpert/logger/config.py"""

import pytest
from pydantic import ValidationError

from metaexpert.logger.config import LoggerConfig


class TestLoggerConfig:
    """Test suite for LoggerConfig class."""

    def test_logger_config_default_values(self):
        """Test LoggerConfig with default values."""
        config = LoggerConfig()

        # Test default values
        assert config.log_level == "DEBUG"
        assert config.log_trade_level == "INFO"
        assert config.log_error_level == "ERROR"
        assert config.log_file == "expert.log"
        assert config.trade_log_file == "trades.log"
        assert config.error_log_file == "errors.log"
        assert config.log_directory == "logs"
        assert config.log_max_file_size == 10 * 1024 * 1024  # 10MB
        assert config.log_backup_count == 5
        assert config.console_logging is True
        assert config.structured_logging is False
        assert config.async_logging is False
        assert config.log_name == "MetaExpert"

    def test_logger_config_custom_values(self):
        """Test LoggerConfig with custom values."""
        config = LoggerConfig(
            log_level="DEBUG",
            log_trade_level="WARNING",
            log_error_level="CRITICAL",
            log_file="custom.log",
            trade_log_file="custom_trades.log",
            error_log_file="custom_errors.log",
            log_directory="custom_logs",
            log_max_file_size=5 * 1024 * 1024,  # 5MB
            log_backup_count=3,
            console_logging=False,
            structured_logging=True,
            async_logging=True,
            log_name="CustomLogger",
        )

        assert config.log_level == "DEBUG"
        assert config.log_trade_level == "WARNING"
        assert config.log_error_level == "CRITICAL"
        assert config.log_file == "custom.log"
        assert config.trade_log_file == "custom_trades.log"
        assert config.error_log_file == "custom_errors.log"
        assert config.log_directory == "custom_logs"
        assert config.log_max_file_size == 5 * 1024 * 1024
        assert config.log_backup_count == 3
        assert config.console_logging is False
        assert config.structured_logging is True
        assert config.async_logging is True
        assert config.log_name == "CustomLogger"

    def test_logger_config_log_level_validation_valid_levels(self):
        """Test LoggerConfig log level validation with valid levels."""
        valid_levels = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ]

        for level in valid_levels:
            config = LoggerConfig(log_level=level)
            # Validation should convert to uppercase
            assert config.log_level == level.upper()

    def test_logger_config_log_level_validation_invalid_level(self):
        """Test LoggerConfig log level validation with invalid level."""
        with pytest.raises(ValidationError) as exc_info:
            LoggerConfig(log_level="INVALID_LEVEL")

        assert "Log level must be one of:" in str(exc_info.value)

    def test_logger_config_log_max_file_size_positive(self):
        """Test LoggerConfig log max file size validation with positive value."""
        config = LoggerConfig(log_max_file_size=1024 * 1024)  # 1MB

        assert config.log_max_file_size == 1024 * 1024

    def test_logger_config_log_max_file_size_zero(self):
        """Test LoggerConfig log max file size validation with zero."""
        with pytest.raises(ValidationError) as exc_info:
            LoggerConfig(log_max_file_size=0)

        assert "Log max file size must be positive" in str(exc_info.value)

    def test_logger_config_log_max_file_size_negative(self):
        """Test LoggerConfig log max file size validation with negative value."""
        with pytest.raises(ValidationError) as exc_info:
            LoggerConfig(log_max_file_size=-1024)

        assert "Log max file size must be positive" in str(exc_info.value)

    def test_logger_config_log_max_file_size_too_large(self):
        """Test LoggerConfig log max file size validation with value exceeding 1GB."""
        with pytest.raises(ValidationError) as exc_info:
            LoggerConfig(log_max_file_size=2 * 1024 * 1024 * 1024)  # 2GB

        assert "Log max file size must not exceed 1GB" in str(exc_info.value)

    def test_logger_config_extra_fields_forbidden(self):
        """Test that LoggerConfig doesn't allow extra fields."""
        with pytest.raises(ValidationError) as exc_info:
            LoggerConfig(invalid_field="some_value")

        # Pydantic should raise an error about extra fields
        assert "extra fields not permitted" in str(
            exc_info.value
        ) or "Extra inputs are not permitted" in str(exc_info.value)

    def test_logger_config_whitespace_stripping(self):
        """Test that LoggerConfig strips whitespace from string fields."""
        config = LoggerConfig(
            log_file=" test.log ",
            trade_log_file=" test_trades.log ",
            error_log_file=" test_errors.log ",
            log_directory=" logs ",
            log_name=" TestLogger ",
        )

        # Check that whitespace has been stripped
        assert config.log_file == "test.log"
        assert config.trade_log_file == "test_trades.log"
        assert config.error_log_file == "test_errors.log"
        assert config.log_directory == "logs"
        assert config.log_name == "TestLogger"

    def test_logger_config_case_insensitive_log_levels(self):
        """Test that log levels are properly validated regardless of case."""
        levels_to_test = [
            ("debug", "DEBUG"),
            ("DeBuG", "DEBUG"),
            ("INFO", "INFO"),
            ("info", "INFO"),
            ("Info", "INFO"),
            ("WARNING", "WARNING"),
            ("warning", "WARNING"),
            ("Warning", "WARNING"),
            ("ERROR", "ERROR"),
            ("error", "ERROR"),
            ("Error", "ERROR"),
            ("CRITICAL", "CRITICAL"),
            ("critical", "CRITICAL"),
            ("Critical", "CRITICAL"),
        ]

        for input_level, expected_level in levels_to_test:
            config = LoggerConfig(log_level=input_level)
            assert config.log_level == expected_level
