"""Unit tests for MetaLogger initialization in the MetaExpert logging system."""

import os
import tempfile
import pytest
from pathlib import Path

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestMetaLoggerInitialization:
    """Test cases for MetaLogger initialization."""
    
    def test_meta_logger_initializes_with_defaults(self):
        """Test that MetaLogger can be initialized with default configuration."""
        logger = MetaLogger()
        
        # Check that logger has been created with default config
        assert logger is not None
        assert logger.config.log_level == "INFO"
        assert logger.config.log_directory == "./logs"
        assert logger.config.expert_log_file == "expert.log"
        assert logger.config.trades_log_file == "trades.log"
        assert logger.config.errors_log_file == "errors.log"
        assert logger.config.enable_async is False
        assert logger.config.max_file_size_mb == 10
        assert logger.config.backup_count == 5
        assert logger.config.enable_structured_logging is False
        assert logger.config.enable_contextual_logging is True
        assert logger.config.mask_sensitive_data is True
    
    def test_meta_logger_initializes_with_custom_config(self):
        """Test that MetaLogger can be initialized with custom configuration."""
        config = LogConfiguration(
            log_level="DEBUG",
            log_directory="./custom_logs",
            expert_log_file="custom_expert.log",
            trades_log_file="custom_trades.log",
            errors_log_file="custom_errors.log",
            enable_async=True,
            max_file_size_mb=25,
            backup_count=10,
            enable_structured_logging=True,
            enable_contextual_logging=False,
            mask_sensitive_data=False
        )
        
        logger = MetaLogger(config=config)
        
        # Check that logger has been created with custom config
        assert logger is not None
        assert logger.config.log_level == "DEBUG"
        assert logger.config.log_directory == "./custom_logs"
        assert logger.config.expert_log_file == "custom_expert.log"
        assert logger.config.trades_log_file == "custom_trades.log"
        assert logger.config.errors_log_file == "custom_errors.log"
        assert logger.config.enable_async is True
        assert logger.config.max_file_size_mb == 25
        assert logger.config.backup_count == 10
        assert logger.config.enable_structured_logging is True
        assert logger.config.enable_contextual_logging is False
        assert logger.config.mask_sensitive_data is False
    
    def test_meta_logger_initializes_with_kwargs_override(self):
        """Test that MetaLogger can be initialized with kwargs that override config."""
        config = LogConfiguration(
            log_level="INFO",
            log_directory="./logs"
        )
        
        logger = MetaLogger(config=config, log_level="DEBUG", log_directory="./test_logs")
        
        # Check that logger has been created with kwargs overriding config
        assert logger is not None
        assert logger.config.log_level == "DEBUG"  # Overridden by kwargs
        assert logger.config.log_directory == "./test_logs"  # Overridden by kwargs
    
    def test_meta_logger_creates_log_directory(self):
        """Test that MetaLogger creates log directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = os.path.join(temp_dir, "new_log_dir")
            assert not os.path.exists(log_dir)
            
            config = LogConfiguration(log_directory=log_dir)
            logger = MetaLogger(config=config)
            
            # Check that the log directory was created
            assert os.path.exists(log_dir)
    
    def test_meta_logger_initializes_with_env_vars(self, monkeypatch):
        """Test that MetaLogger respects environment variables for configuration."""
        # Set environment variables
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        monkeypatch.setenv("LOG_DIRECTORY", "./env_logs")
        monkeypatch.setenv("EXPERT_LOG_FILE", "env_expert.log")
        monkeypatch.setenv("ENABLE_ASYNC", "true")
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "15")
        
        # Create logger without specific config (should use env vars)
        logger = MetaLogger()
        
        # Check that environment variables were used
        assert logger.config.log_level == "WARNING"
        assert logger.config.log_directory == "./env_logs"
        assert logger.config.expert_log_file == "env_expert.log"
        assert logger.config.enable_async is True
        assert logger.config.max_file_size_mb == 15
    
    def test_meta_logger_config_priority_order(self, monkeypatch):
        """Test that configuration priority order is respected (code > env > default)."""
        # Set environment variable
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        
        # Create logger with code parameter that should override env
        logger = MetaLogger(log_level="CRITICAL")
        
        # Code parameter should take precedence over environment variable
        assert logger.config.log_level == "CRITICAL"