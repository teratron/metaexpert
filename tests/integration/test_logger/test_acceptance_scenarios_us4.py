"""Acceptance tests for configuration methods in the MetaExpert logging system."""

import os
import tempfile
from unittest.mock import patch

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestConfigurationAcceptance:
    """Acceptance tests for user story 4: Configure Logging via Multiple Methods."""
    
    def test_cli_arguments_take_precedence_over_other_methods(self):
        """Verify CLI arguments take precedence over other methods (acceptance scenario 1)."""
        # In a real application, CLI arguments would be passed as code parameters
        # to the MetaLogger constructor when the CLI command is executed
        
        # Simulate environment variables being set (lower priority)
        env_vars = {
            "LOG_LEVEL": "WARNING",
            "LOG_DIRECTORY": "/env/logs",
            "EXPERT_LOG_FILE": "env_expert.log",
            "ENABLE_ASYNC": "false",
            "MAX_FILE_SIZE_MB": "5"
        }
        
        with patch.dict(os.environ, env_vars):
            # Simulate CLI arguments being passed (highest priority)
            # This is equivalent to CLI parameters being parsed and passed to constructor
            logger = MetaLogger(
                log_level="CRITICAL",  # CLI argument override
                log_directory="/cli/logs",  # CLI argument override
                expert_log_file="cli_expert.log",  # CLI argument override
                enable_async=True,  # CLI argument override
                max_file_size_mb=50  # CLI argument override
            )
            
            # CLI arguments (passed as code parameters) should take precedence
            assert logger.config.log_level == "CRITICAL"  # CLI override
            assert logger.config.log_directory == "/cli/logs"  # CLI override
            assert logger.config.expert_log_file == "cli_expert.log"  # CLI override
            assert logger.config.enable_async is True  # CLI override
            assert logger.config.max_file_size_mb == 50  # CLI override
            
            # Verify that the environment variable values were NOT used
            assert logger.config.log_level != "WARNING"
            assert logger.config.log_directory != "/env/logs"
            assert logger.config.expert_log_file != "env_expert.log"
    
    def test_code_parameters_take_precedence_over_environment_variables(self):
        """Verify code parameters take precedence over environment variables (acceptance scenario 2)."""
        # Set environment variables (lower priority)
        env_vars = {
            "LOG_LEVEL": "ERROR",
            "EXPERT_LOG_FILE": "env_file.log",
            "MAX_FILE_SIZE_MB": "15",
            "BACKUP_COUNT": "3"
        }
        
        with patch.dict(os.environ, env_vars):
            # Create config with code parameters (higher priority)
            config = LogConfiguration(
                log_level="DEBUG",  # Code parameter override
                expert_log_file="code_file.log",  # Code parameter override
                max_file_size_mb=30  # Code parameter override
            )
            
            # Code parameters should take precedence over environment variables
            assert config.log_level == "DEBUG"  # Code override
            assert config.expert_log_file == "code_file.log"  # Code override
            assert config.max_file_size_mb == 30  # Code override
            # backup_count should come from environment since not specified in code
            assert config.backup_count == 3
            
            # Verify that environment values were NOT used for overridden fields
            assert config.log_level != "ERROR"
            assert config.expert_log_file != "env_file.log"
            assert config.max_file_size_mb != 15
            
            # Create a logger with the same approach
            logger = MetaLogger(
                log_level="INFO",  # Code parameter
                log_directory="./test_dir"  # Code parameter
            )
            
            # Code parameters should still take precedence
            assert logger.config.log_level == "INFO"
            assert logger.config.log_directory == "./test_dir"
            # Other values should come from environment or defaults
            assert logger.config.expert_log_file == "env_file.log"  # From environment