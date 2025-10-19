"""Integration tests for multiple configuration methods in the MetaExpert logging system."""

import os
import tempfile
from unittest.mock import patch

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestMultipleConfigurationMethods:
    """Integration tests for multiple configuration methods."""
    
    def test_environment_variable_configuration(self):
        """Test configuration using environment variables."""
        env_vars = {
            "LOG_LEVEL": "WARNING",
            "LOG_DIRECTORY": "./env_test_logs",
            "EXPERT_LOG_FILE": "env_expert.log",
            "TRADES_LOG_FILE": "env_trades.log",
            "ERRORS_LOG_FILE": "env_errors.log",
            "ENABLE_ASYNC": "true",
            "MAX_FILE_SIZE_MB": "25",
            "BACKUP_COUNT": "8",
            "ENABLE_STRUCTURED_LOGGING": "true",
            "ENABLE_CONTEXTUAL_LOGGING": "false",
            "MASK_SENSITIVE_DATA": "false",
            "CONSOLE_LOG_FORMAT": "json",
            "FILE_LOG_FORMAT": "json"
        }
        
        with patch.dict(os.environ, env_vars):
            # Create logger without specifying parameters (should use env vars)
            logger = MetaLogger()
            
            # Verify that environment variables were used
            assert logger.config.log_level == "WARNING"
            assert logger.config.log_directory == "./env_test_logs"
            assert logger.config.expert_log_file == "env_expert.log"
            assert logger.config.trades_log_file == "env_trades.log"
            assert logger.config.errors_log_file == "env_errors.log"
            assert logger.config.enable_async is True
            assert logger.config.max_file_size_mb == 25
            assert logger.config.backup_count == 8
            assert logger.config.enable_structured_logging is True
            assert logger.config.enable_contextual_logging is False
            assert logger.config.mask_sensitive_data is False
            assert logger.config.console_log_format == "json"
            assert logger.config.file_log_format == "json"
    
    def test_code_parameter_configuration(self):
        """Test configuration using code parameters."""
        # Ensure no environment variables interfere
        with patch.dict(os.environ, {}, clear=True):
            # Create logger with code parameters
            logger = MetaLogger(
                log_level="CRITICAL",
                log_directory="./code_test_logs",
                expert_log_file="code_expert.log",
                trades_log_file="code_trades.log",
                errors_log_file="code_errors.log",
                enable_async=False,
                max_file_size_mb=50,
                backup_count=12,
                enable_structured_logging=False,
                enable_contextual_logging=True,
                mask_sensitive_data=True,
                console_log_format="text",
                file_log_format="json"
            )
            
            # Verify that code parameters were used
            assert logger.config.log_level == "CRITICAL"
            assert logger.config.log_directory == "./code_test_logs"
            assert logger.config.expert_log_file == "code_expert.log"
            assert logger.config.trades_log_file == "code_trades.log"
            assert logger.config.errors_log_file == "code_errors.log"
            assert logger.config.enable_async is False
            assert logger.config.max_file_size_mb == 50
            assert logger.config.backup_count == 12
            assert logger.config.enable_structured_logging is False
            assert logger.config.enable_contextual_logging is True
            assert logger.config.mask_sensitive_data is True
            assert logger.config.console_log_format == "text"
            assert logger.config.file_log_format == "json"
    
    def test_default_configuration(self):
        """Test configuration using default values."""
        # Ensure no environment variables interfere
        with patch.dict(os.environ, {}, clear=True):
            # Create logger without any parameters
            logger = MetaLogger()
            
            # Verify default values are used
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
            assert logger.config.console_log_format == "text"
            assert logger.config.file_log_format == "json"
            assert logger.config.context_fields == ["expert_name", "symbol", "trade_id", "order_id", "strategy_id", "account_id"]
    
    def test_configuration_with_explicit_config_object(self):
        """Test configuration using an explicit LogConfiguration object."""
        # Create a config object with specific settings
        config = LogConfiguration(
            log_level="DEBUG",
            log_directory="./config_obj_logs",
            expert_log_file="config_expert.log",
            enable_async=True,
            max_file_size_mb=100
        )
        
        # Create logger with the config object
        logger = MetaLogger(config=config)
        
        # Verify that the config object settings were used
        assert logger.config.log_level == "DEBUG"
        assert logger.config.log_directory == "./config_obj_logs"
        assert logger.config.expert_log_file == "config_expert.log"
        assert logger.config.enable_async is True
        assert logger.config.max_file_size_mb == 100
    
    def test_mixed_configuration_methods(self):
        """Test configuration using a mix of methods (env vars + code params)."""
        # Set environment variables
        env_vars = {
            "LOG_LEVEL": "ERROR",
            "LOG_DIRECTORY": "./mixed_logs",
            "EXPERT_LOG_FILE": "env_expert.log",
            "MAX_FILE_SIZE_MB": "20",
            "BACKUP_COUNT": "7"
        }
        
        with patch.dict(os.environ, env_vars):
            # Create logger with some parameters overridden in code
            logger = MetaLogger(
                log_level="INFO",  # Override env var
                trades_log_file="override_trades.log",  # New parameter
                enable_async=True  # New parameter
            )
            
            # Parameters specified in code should override environment
            assert logger.config.log_level == "INFO"  # Overrode env
            assert logger.config.log_directory == "./mixed_logs"  # From env
            assert logger.config.expert_log_file == "env_expert.log"  # From env
            assert logger.config.trades_log_file == "override_trades.log"  # Code param
            assert logger.config.max_file_size_mb == 20  # From env
            assert logger.config.backup_count == 7  # From env
            assert logger.config.enable_async is True  # Code param
    
    def test_functional_behavior_with_different_configs(self):
        """Test that different configurations result in different functional behavior."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test with structured logging enabled
            structured_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="structured.log",
                enable_structured_logging=True,
                file_log_format="json",
                log_level="DEBUG"
            )
            
            structured_logger = MetaLogger(config=structured_config)
            structured_logger.info("Structured test message", test_field="structured")
            
            # Test with structured logging disabled
            text_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="text.log",
                enable_structured_logging=False,
                file_log_format="text",
                log_level="DEBUG"
            )
            
            text_logger = MetaLogger(config=text_config)
            text_logger.info("Text test message", test_field="text")
            
            # Read both log files and verify different formats
            structured_path = os.path.join(temp_dir, "structured.log")
            text_path = os.path.join(temp_dir, "text.log")
            
            with open(structured_path, 'r', encoding='utf-8') as f:
                structured_content = f.read()
            
            with open(text_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Structured content should look like JSON with our fields
            assert "Structured test message" in structured_content
            assert "structured" in structured_content
            # Text content should be formatted differently
            
            # Text content should have the message but in text format
            assert "Text test message" in text_content
            assert "text" in text_content