"""Unit tests for LogConfiguration model in the MetaExpert logging system."""

import os
import pytest
from pydantic import ValidationError

from src.metaexpert.logger.config import LogConfiguration, LogLevel


class TestLogConfiguration:
    """Test cases for LogConfiguration model."""
    
    def test_log_configuration_defaults(self):
        """Test that LogConfiguration uses correct default values."""
        config = LogConfiguration()
        
        assert config.log_level == "INFO"
        assert config.log_directory == "./logs"
        assert config.expert_log_file == "expert.log"
        assert config.trades_log_file == "trades.log"
        assert config.errors_log_file == "errors.log"
        assert config.enable_async is False
        assert config.max_file_size_mb == 10
        assert config.backup_count == 5
        assert config.enable_structured_logging is False
        assert config.enable_contextual_logging is True
        assert config.mask_sensitive_data is True
        assert config.console_log_format == "text"
        assert config.file_log_format == "json"
        assert config.context_fields == ["expert_name", "symbol", "trade_id", "order_id", "strategy_id", "account_id"]
    
    def test_log_configuration_validation_log_level_valid(self):
        """Test that valid log levels are accepted."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in valid_levels:
            config = LogConfiguration(log_level=level)
            assert config.log_level == level.upper()
    
    def test_log_configuration_validation_log_level_invalid(self):
        """Test that invalid log levels raise validation error."""
        invalid_levels = ["TRACE", "VERBOSE", "NOTSET", "debug", "info"]
        
        for level in invalid_levels:
            with pytest.raises(ValidationError):
                LogConfiguration(log_level=level)
    
    def test_log_configuration_validation_max_file_size_mb_valid(self):
        """Test that valid max file sizes are accepted."""
        valid_sizes = [1, 10, 500, 1000]
        
        for size in valid_sizes:
            config = LogConfiguration(max_file_size_mb=size)
            assert config.max_file_size_mb == size
    
    def test_log_configuration_validation_max_file_size_mb_invalid(self):
        """Test that invalid max file sizes raise validation error."""
        invalid_sizes = [0, -1, 1001, 2000]
        
        for size in invalid_sizes:
            with pytest.raises(ValidationError):
                LogConfiguration(max_file_size_mb=size)
    
    def test_log_configuration_validation_backup_count_valid(self):
        """Test that valid backup counts are accepted."""
        valid_counts = [1, 5, 50, 100]
        
        for count in valid_counts:
            config = LogConfiguration(backup_count=count)
            assert config.backup_count == count
    
    def test_log_configuration_validation_backup_count_invalid(self):
        """Test that invalid backup counts raise validation error."""
        invalid_counts = [0, -1, 101, 200]
        
        for count in invalid_counts:
            with pytest.raises(ValidationError):
                LogConfiguration(backup_count=count)
    
    def test_log_configuration_validation_format_types_valid(self):
        """Test that valid format types are accepted."""
        config = LogConfiguration(console_log_format="text", file_log_format="json")
        assert config.console_log_format == "text"
        assert config.file_log_format == "json"
        
        config = LogConfiguration(console_log_format="json", file_log_format="text")
        assert config.console_log_format == "json"
        assert config.file_log_format == "text"
    
    def test_log_configuration_validation_format_types_invalid(self):
        """Test that invalid format types raise validation error."""
        invalid_formats = ["xml", "yaml", "csv", "TEXT", "JSON"]
        
        for format_val in invalid_formats:
            with pytest.raises(ValidationError):
                LogConfiguration(console_log_format=format_val)
            
            with pytest.raises(ValidationError):
                LogConfiguration(file_log_format=format_val)
    
    def test_log_configuration_with_env_vars(self, monkeypatch):
        """Test that LogConfiguration can be initialized with environment variables."""
        # Set environment variables
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("LOG_DIRECTORY", "/custom/path")
        monkeypatch.setenv("EXPERT_LOG_FILE", "custom.log")
        monkeypatch.setenv("ENABLE_ASYNC", "true")
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "100")
        monkeypatch.setenv("BACKUP_COUNT", "15")
        monkeypatch.setenv("ENABLE_STRUCTURED_LOGGING", "true")
        monkeypatch.setenv("ENABLE_CONTEXTUAL_LOGGING", "false")
        monkeypatch.setenv("MASK_SENSITIVE_DATA", "false")
        monkeypatch.setenv("CONSOLE_LOG_FORMAT", "json")
        monkeypatch.setenv("FILE_LOG_FORMAT", "text")
        
        # Create config without explicit parameters to use env vars
        config = LogConfiguration()
        
        # Check that environment variables were used
        assert config.log_level == "DEBUG"
        assert config.log_directory == "/custom/path"
        assert config.expert_log_file == "custom.log"
        assert config.enable_async is True
        assert config.max_file_size_mb == 100
        assert config.backup_count == 15
        assert config.enable_structured_logging is True
        assert config.enable_contextual_logging is False
        assert config.mask_sensitive_data is False
        assert config.console_log_format == "json"
        assert config.file_log_format == "text"
    
    def test_log_configuration_override_env_vars_with_params(self, monkeypatch):
        """Test that explicit parameters override environment variables."""
        # Set environment variables
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        monkeypatch.setenv("LOG_DIRECTORY", "/env/path")
        
        # Create config with explicit parameters that should override env vars
        config = LogConfiguration(log_level="CRITICAL", log_directory="/param/path")
        
        # Check that explicit parameters override environment variables
        assert config.log_level == "CRITICAL"
        assert config.log_directory == "/param/path"
    
    def test_log_configuration_bool_env_vars_parsing(self, monkeypatch):
        """Test that boolean environment variables are parsed correctly."""
        # Test various true values
        true_values = ["true", "1", "yes", "on", "True", "TRUE"]
        for true_val in true_values:
            monkeypatch.setenv("ENABLE_ASYNC", true_val)
            monkeypatch.setenv("ENABLE_STRUCTURED_LOGGING", "false")  # Set other to avoid conflicts
            config = LogConfiguration()
            assert config.enable_async is True
        
        # Test various false values
        false_values = ["false", "0", "no", "off", "False", "FALSE", ""]
        for false_val in false_values:
            monkeypatch.setenv("ENABLE_ASYNC", false_val)
            monkeypatch.setenv("ENABLE_STRUCTURED_LOGGING", "true")  # Set other to avoid conflicts
            config = LogConfiguration()
            assert config.enable_async is False
    
    def test_log_configuration_int_env_vars_parsing(self, monkeypatch):
        """Test that integer environment variables are parsed correctly."""
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "25")
        monkeypatch.setenv("BACKUP_COUNT", "8")
        
        config = LogConfiguration()
        
        assert config.max_file_size_mb == 25
        assert config.backup_count == 8
    
    def test_log_configuration_invalid_int_env_vars(self, monkeypatch):
        """Test that invalid integer environment variables raise errors."""
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "invalid")
        
        with pytest.raises(ValueError):
            LogConfiguration()