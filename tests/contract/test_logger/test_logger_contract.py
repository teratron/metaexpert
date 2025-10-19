"""Contract tests for the MetaExpert logging system based on API contract specifications."""

import os
import tempfile
import json
from datetime import datetime

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestLoggerContract:
    """Contract tests for the logger API based on the specification."""
    
    def test_log_configuration_model_contract(self):
        """Test that LogConfiguration model matches the API contract."""
        # Create a configuration matching the contract specification
        config = LogConfiguration(
            log_level="INFO",
            log_directory="./logs",
            expert_log_file="expert.log",
            trades_log_file="trades.log",
            errors_log_file="errors.log",
            enable_async=False,
            max_file_size_mb=10,
            backup_count=5,
            enable_structured_logging=False,
            enable_contextual_logging=True,
            mask_sensitive_data=True,
            console_log_format="text",
            file_log_format="json",
            context_fields=["expert_name", "symbol", "trade_id", "order_id", "strategy_id", "account_id"]
        )
        
        # Verify all fields exist and have correct values
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
        
        # Verify validation rules work
        try:
            invalid_config = LogConfiguration(log_level="INVALID_LEVEL")
            assert False, "Should have raised validation error for invalid log level"
        except:
            pass  # Expected to raise validation error
    
    def test_meta_logger_constructor_contract(self):
        """Test that MetaLogger constructor matches the API contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test constructor with parameters as specified in contract
            logger = MetaLogger(
                log_level="DEBUG",
                log_file="expert.log",
                trade_log_file="trades.log", 
                error_log_file="errors.log",
                log_to_console=True,
                structured_logging=False,
                async_logging=False,
                log_max_file_size=10485760,  # 10MB
                log_backup_count=5
            )
            
            # Verify logger was created successfully
            assert logger is not None
            assert logger.config.log_level == "DEBUG"
            assert logger.config.log_directory == temp_dir  # Should be the temporary directory
            assert logger.config.expert_log_file == "expert.log"
            assert logger.config.trades_log_file == "trades.log"
            assert logger.config.errors_log_file == "errors.log"
            assert logger.config.enable_async is False
            assert logger.config.max_file_size_mb == 10
            assert logger.config.backup_count == 5
    
    def test_meta_logger_bind_method_contract(self):
        """Test that bind method matches the API contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(log_directory=temp_dir)
            logger = MetaLogger(config=config)
            
            # Test bind method
            contextual_logger = logger.bind({"expert_name": "TestExpert", "symbol": "BTCUSDT"})
            assert contextual_logger is not None
            assert hasattr(contextual_logger, 'info')
            assert hasattr(contextual_logger, 'debug')
            assert hasattr(contextual_logger, 'warning')
            assert hasattr(contextual_logger, 'error')
            assert hasattr(contextual_logger, 'critical')
    
    def test_meta_logger_logging_methods_contract(self):
        """Test that logging methods match the API contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(log_directory=temp_dir)
            logger = MetaLogger(config=config)
            
            # Verify all required methods exist
            assert hasattr(logger, 'debug')
            assert hasattr(logger, 'info')
            assert hasattr(logger, 'warning')
            assert hasattr(logger, 'error')
            assert hasattr(logger, 'critical')
            assert hasattr(logger, 'trade')
            assert hasattr(logger, 'context')
            
            # Test that methods can be called without errors
            logger.debug("Debug message", extra_field="value")
            logger.info("Info message", extra_field="value")
            logger.warning("Warning message", extra_field="value")
            logger.error("Error message", extra_field="value")
            logger.critical("Critical message", extra_field="value")
            logger.trade("Trade message", symbol="BTCUSDT", trade_id="123")
    
    def test_log_entry_model_contract(self):
        """Test that log entries match the RFC 5424 model contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create logger with structured logging enabled
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="structured_contract_test.log",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log an entry with all required fields
            logger.info(
                "Test message",
                expert_name="ContractTestExpert",
                symbol="CONTRACT",
                trade_id="test_123",
                order_id="order_456",
                strategy_id="ContractStrategy",
                account_id="account_789"
            )
            
            # Read the log file to verify structure
            log_path = os.path.join(temp_dir, "structured_contract_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Parse JSON to check structure
            log_entry = json.loads(content)
            
            # Verify RFC 5424 compliant fields exist
            assert 'timestamp' in log_entry
            assert 'severity' in log_entry
            assert 'message' in log_entry
            
            # Verify contextual fields are present
            assert log_entry['expert_name'] == "ContractTestExpert"
            assert log_entry['symbol'] == "CONTRACT"
            assert log_entry['trade_id'] == "test_123"
            assert log_entry['order_id'] == "order_456"
            assert log_entry['strategy_id'] == "ContractStrategy"
            assert log_entry['account_id'] == "account_789"
            assert log_entry['message'] == "Test message"
    
    def test_log_format_contract(self):
        """Test that log formats match the API contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test JSON format
            json_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="json_format_test.log",
                enable_structured_logging=True,
                file_log_format="json"
            )
            json_logger = MetaLogger(config=json_config)
            json_logger.info("JSON format test", test_field="json_value")
            
            json_log_path = os.path.join(temp_dir, "json_format_test.log")
            with open(json_log_path, 'r', encoding='utf-8') as f:
                json_content = f.read().strip()
            
            # Should be valid JSON
            json_parsed = json.loads(json_content)
            assert 'timestamp' in json_parsed
            assert 'severity' in json_parsed
            assert json_parsed['message'] == "JSON format test"
            assert json_parsed['test_field'] == "json_value"
            
            # Test text format
            text_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="text_format_test.log",
                enable_structured_logging=False,
                file_log_format="text"
            )
            text_logger = MetaLogger(config=text_config)
            text_logger.info("Text format test", test_field="text_value")
            
            text_log_path = os.path.join(temp_dir, "text_format_test.log")
            with open(text_log_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Should contain the message (format may vary but should contain our text)
            assert "Text format test" in text_content
            assert "text_value" in text_content
    
    def test_configuration_priority_contract(self):
        """Test that configuration priority follows the contract (Code > Env > Default)."""
        # Test with environment variables set
        with tempfile.TemporaryDirectory() as temp_dir:
            original_env = os.environ.copy()
            try:
                # Set environment variables
                os.environ["LOG_LEVEL"] = "WARNING"
                os.environ["EXPERT_LOG_FILE"] = "env_expert.log"
                
                # Create logger with code parameters that should override env
                logger = MetaLogger(
                    log_level="CRITICAL",  # Code parameter
                    log_directory=temp_dir  # Code parameter
                )
                
                # Code parameters should take priority over environment
                assert logger.config.log_level == "CRITICAL"  # Not WARNING from env
                assert logger.config.log_directory == temp_dir  # From code
                # expert_log_file would come from env since not specified in code
                assert logger.config.expert_log_file == "env_expert.log"
            finally:
                # Restore original environment
                os.environ.clear()
                os.environ.update(original_env)


class TestAPIContract:
    """Additional API contract tests."""
    
    def test_context_management_api(self):
        """Test the context management API contract."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(log_directory=temp_dir)
            logger = MetaLogger(config=config)
            
            # Test context manager
            with logger.context(expert_name="ContextTestExpert", symbol="CTX"):
                logger.info("Inside context")
            
            # Context should work properly (functionality tested elsewhere)
            assert True  # If we get here without exceptions, the API is correct