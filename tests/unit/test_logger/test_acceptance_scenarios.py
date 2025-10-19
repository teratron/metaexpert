"""Acceptance tests for the MetaExpert logging system."""

from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration


class TestAcceptanceScenarios:
    """Acceptance tests for user story 1: Initialize Logging System."""
    
    def test_logger_creation_with_default_settings(self):
        """Verify logger can be created with default settings (acceptance scenario 1)."""
        # Create a logger with default settings
        logger = MetaLogger()
        
        # Verify the logger was created successfully
        assert logger is not None
        assert hasattr(logger, 'config')
        assert hasattr(logger, 'logger')
        
        # Verify default configuration values
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
        
        # Verify logger has the expected methods
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'critical')
        assert hasattr(logger, 'trade')
        assert hasattr(logger, 'bind')
        assert hasattr(logger, 'context')
    
    def test_logger_creation_with_custom_parameters(self):
        """Verify logger can be created with custom parameters (acceptance scenario 2)."""
        # Create a logger with custom parameters
        logger = MetaLogger(
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
        
        # Verify the logger was created successfully
        assert logger is not None
        assert hasattr(logger, 'config')
        assert hasattr(logger, 'logger')
        
        # Verify custom configuration values
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
        
        # Verify logger has the expected methods
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'critical')
        assert hasattr(logger, 'trade')
        assert hasattr(logger, 'bind')
        assert hasattr(logger, 'context')