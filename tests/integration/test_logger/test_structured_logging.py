"""Integration tests for structured logging in the MetaExpert logging system."""

import json
import tempfile
import os

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestStructuredLoggingIntegration:
    """Integration tests for structured logging functionality."""
    
    def test_structured_logging_with_json_format(self):
        """Test that structured logging produces valid JSON output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="structured_json_test.log",
                log_level="DEBUG",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log with various contextual information
            logger.info("Structured info message", 
                       expert_name="TestExpert", 
                       symbol="BTCUSDT", 
                       trade_id="trade_123")
            
            logger.error("Structured error message",
                        expert_name="TestExpert",
                        error_code="ERR-1001",
                        details="Connection timeout")
            
            # Read the log file and verify JSON format
            log_path = os.path.join(temp_dir, "structured_json_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Each line should be a valid JSON object
            for line in lines:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        parsed = json.loads(line)
                        # Verify it has required fields
                        assert 'timestamp' in parsed
                        assert 'severity' in parsed
                        assert 'message' in parsed
                    except json.JSONDecodeError:
                        assert False, f"Line is not valid JSON: {line}"
    
    def test_structured_logging_with_all_context_fields(self):
        """Test that structured logging includes all required context fields."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="all_context_test.log",
                log_level="INFO",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log with all required context fields
            with logger.context(
                expert_name="FullContextExpert",
                symbol="ETHUSDT",
                trade_id="trade_456",
                order_id="order_789",
                strategy_id="TestStrategy",
                account_id="account_abc"
            ):
                logger.info("Full context message", additional_param="value")
            
            # Read the log and verify all context fields are present
            log_path = os.path.join(temp_dir, "all_context_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Parse JSON and verify all fields
            parsed = json.loads(content)
            
            assert parsed['expert_name'] == "FullContextExpert"
            assert parsed['symbol'] == "ETHUSDT"
            assert parsed['trade_id'] == "trade_456"
            assert parsed['order_id'] == "order_789"
            assert parsed['strategy_id'] == "TestStrategy"
            assert parsed['account_id'] == "account_abc"
            assert parsed['message'] == "Full context message"
            assert parsed['additional_param'] == "value"
            assert parsed['severity'] == "info"
    
    def test_structured_logging_with_different_log_levels(self):
        """Test that structured logging works with different log levels."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="log_levels_test.log",
                errors_log_file="errors_levels_test.log",
                log_level="DEBUG",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log at different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
            
            # Read the expert log file (should contain debug+ levels)
            expert_log_path = os.path.join(temp_dir, "log_levels_test.log")
            
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_lines = f.readlines()
            
            # All messages except error and critical should be in expert log
            messages_found = 0
            for line in expert_lines:
                line = line.strip()
                if line:
                    parsed = json.loads(line)
                    if parsed['message'] in ["Debug message", "Info message", "Warning message"]:
                        assert parsed['severity'] in ['debug', 'info', 'warning']
                        messages_found += 1
            
            assert messages_found >= 3  # Should have at least the debug, info, and warning messages
            
            # Read the errors log file (should contain error+ levels)
            errors_log_path = os.path.join(temp_dir, "errors_levels_test.log")
            
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_lines = f.readlines()
            
            # Error and critical messages should be in errors log
            error_messages_found = 0
            for line in errors_lines:
                line = line.strip()
                if line:
                    parsed = json.loads(line)
                    if parsed['message'] in ["Error message", "Critical message"]:
                        assert parsed['severity'] in ['error', 'critical']
                        error_messages_found += 1
            
            assert error_messages_found >= 2  # Should have error and critical messages
    
    def test_structured_logging_with_trade_events(self):
        """Test that structured logging works with trade events."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="trade_structured_expert.log",
                trades_log_file="trade_structured_trades.log",
                log_level="INFO",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log trade events
            logger.trade("Trade executed", 
                        expert_name="TradeExpert",
                        symbol="BTCUSDT",
                        trade_id="trade_111",
                        order_id="order_222",
                        strategy_id="TradeStrategy")
            
            # Read the trades log file
            trades_log_path = os.path.join(temp_dir, "trade_structured_trades.log")
            
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Verify JSON structure
            parsed = json.loads(content)
            
            assert parsed['message'] == "Trade executed"
            assert parsed['expert_name'] == "TradeExpert"
            assert parsed['symbol'] == "BTCUSDT"
            assert parsed['trade_id'] == "trade_111"
            assert parsed['order_id'] == "order_222"
            assert parsed['strategy_id'] == "TradeStrategy"
            assert parsed['severity'] == "info"  # trade() method uses info level
    
    def test_structured_logging_with_contextual_bound_logger(self):
        """Test that structured logging works with bound contextual loggers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="bound_context_test.log",
                log_level="INFO",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Create a contextual logger by binding
            contextual_logger = logger.bind({
                "expert_name": "BoundExpert",
                "symbol": "ADAUSDT",
                "strategy_id": "BoundStrategy"
            })
            
            # Log with the contextual logger
            contextual_logger.info("Message from bound logger", 
                                 trade_id="bound_trade_123",
                                 custom_field="custom_value")
            
            # Read the log file
            log_path = os.path.join(temp_dir, "bound_context_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Verify all context is preserved
            parsed = json.loads(content)
            
            assert parsed['message'] == "Message from bound logger"
            assert parsed['expert_name'] == "BoundExpert"
            assert parsed['symbol'] == "ADAUSDT"
            assert parsed['strategy_id'] == "BoundStrategy"
            assert parsed['trade_id'] == "bound_trade_123"
            assert parsed['custom_field'] == "custom_value"
            assert parsed['severity'] == "info"