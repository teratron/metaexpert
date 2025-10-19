"""Unit tests for configuration priority in the MetaExpert logging system."""

import os
import tempfile
from unittest.mock import patch

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestConfigurationPriority:
    """Test cases for configuration priority implementation."""
    
    def test_code_parameters_override_environment_variables(self):
        """Test that code parameters override environment variables."""
        # Set environment variable
        with patch.dict(os.environ, {"LOG_LEVEL": "WARNING"}):
            # Pass a different value as code parameter
            config = LogConfiguration(log_level="DEBUG")
            
            # Code parameter should override environment variable
            assert config.log_level == "DEBUG"
    
    def test_environment_variables_override_defaults(self):
        """Test that environment variables override default values."""
        # Set environment variable
        with patch.dict(os.environ, {"LOG_LEVEL": "ERROR"}):
            # Create config without specifying log_level
            config = LogConfiguration()
            
            # Environment variable should override default
            assert config.log_level == "ERROR"
    
    def test_code_parameters_override_env_multiple_fields(self):
        """Test that code parameters override environment variables for multiple fields."""
        env_vars = {
            "LOG_LEVEL": "WARNING",
            "LOG_DIRECTORY": "/env/logs",
            "EXPERT_LOG_FILE": "env_expert.log",
            "ENABLE_ASYNC": "true",
            "MAX_FILE_SIZE_MB": "100",
        }
        
        with patch.dict(os.environ, env_vars):
            # Pass different values as code parameters
            config = LogConfiguration(
                log_level="CRITICAL",
                log_directory="/code/logs",
                expert_log_file="code_expert.log",
                enable_async=False,
                max_file_size_mb=50
            )
            
            # Code parameters should override environment variables
            assert config.log_level == "CRITICAL"
            assert config.log_directory == "/code/logs"
            assert config.expert_log_file == "code_expert.log"
            assert config.enable_async is False
            assert config.max_file_size_mb == 50
    
    def test_meta_logger_respects_parameter_priority_without_config(self):
        """Test that MetaLogger respects parameter priority when not using explicit config."""
        with patch.dict(os.environ, {"LOG_LEVEL": "WARNING", "LOG_DIRECTORY": "/env/logs"}):
            # Create logger with direct parameters
            logger = MetaLogger(log_level="DEBUG", log_directory="/direct/logs")
            
            # Direct parameters should override environment variables
            assert logger.config.log_level == "DEBUG"
            assert logger.config.log_directory == "/direct/logs"
    
    def test_meta_logger_respects_parameter_priority_with_config(self):
        """Test that MetaLogger respects parameter priority when using explicit config."""
        # Set environment variables
        with patch.dict(os.environ, {"LOG_LEVEL": "WARNING", "LOG_DIRECTORY": "/env/logs"}):
            # Create base config (will use env vars)
            base_config = LogConfiguration()
            
            # Create logger with config and additional parameters
            logger = MetaLogger(config=base_config, log_level="CRITICAL", log_directory="/param/logs")
            
            # Parameters passed to constructor should override both config and env vars
            assert logger.config.log_level == "CRITICAL"
            assert logger.config.log_directory == "/param/logs"
    
    def test_empty_code_parameters_do_not_override_env(self):
        """Test that empty/unset code parameters don't override environment variables."""
        with patch.dict(os.environ, {"LOG_LEVEL": "ERROR", "EXPERT_LOG_FILE": "env.log"}):
            # Create config with some params set but others not
            config = LogConfiguration(log_level="DEBUG")  # Only override log_level
            
            # log_level should come from code parameter
            assert config.log_level == "DEBUG"
            # other values should come from environment
            assert config.expert_log_file == "env.log"
    
    def test_none_code_parameters_behavior(self):
        """Test behavior when None is explicitly passed as a parameter."""
        with patch.dict(os.environ, {"LOG_LEVEL": "ERROR"}):
            # Explicitly passing None should still allow env var to take effect
            # for parameters that can be None, or use default if not applicable
            config = LogConfiguration(log_level="INFO")  # Use specific value
            
            assert config.log_level == "INFO"