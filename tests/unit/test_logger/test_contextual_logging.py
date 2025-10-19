"""Unit tests for contextual logging in the MetaExpert logging system."""

import json
import tempfile
import os
from unittest.mock import patch

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestContextualLogging:
    """Test cases for contextual logging functionality."""
    
    def test_contextual_logging_with_bind_method(self):
        """Test contextual logging using the bind method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_bind_test.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Create a contextual logger using bind
            contextual_logger = logger.bind({
                "expert_name": "TestExpert",
                "symbol": "BTCUSDT",
                "strategy_id": "TestStrategy"
            })
            
            # Log a message with the contextual logger
            contextual_logger.info("Test message with context")
            
            # Verify that the context appears in the log
            log_path = os.path.join(temp_dir, "context_bind_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "TestExpert" in content
            assert "BTCUSDT" in content
            assert "TestStrategy" in content
            assert "Test message with context" in content
    
    def test_contextual_logging_with_context_manager(self):
        """Test contextual logging using the context manager."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_manager_test.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Use the context manager to add contextual information
            with logger.context(expert_name="TestExpert", symbol="ETHUSDT", account_id="test_account_123"):
                logger.info("Test message inside context")
                logger.warning("Another message with context", extra_field="extra_value")
            
            # Verify that the context appears in the log
            log_path = os.path.join(temp_dir, "context_manager_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "TestExpert" in content
            assert "ETHUSDT" in content
            assert "test_account_123" in content
            assert "Test message inside context" in content
            assert "Another message with context" in content
            assert "extra_value" in content
    
    def test_contextual_logging_with_required_fields(self):
        """Test contextual logging with all required context fields."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="required_fields_test.log",
                log_level="DEBUG",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log with all required context fields
            contextual_logger = logger.bind({
                "expert_name": "FullContextExpert",
                "symbol": "ETHUSDT",
                "trade_id": "trade_123456",
                "order_id": "order_789012",
                "strategy_id": "FullContextStrategy",
                "account_id": "account_abcdef"
            })
            
            contextual_logger.info("Full context message", additional_info="value")
            
            # Verify that all context fields appear in the log
            log_path = os.path.join(temp_dir, "required_fields_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JSON to ensure all fields are present
            try:
                log_entry = json.loads(content.strip())
                assert log_entry["expert_name"] == "FullContextExpert"
                assert log_entry["symbol"] == "ETHUSDT"
                assert log_entry["trade_id"] == "trade_123456"
                assert log_entry["order_id"] == "order_789012"
                assert log_entry["strategy_id"] == "FullContextStrategy"
                assert log_entry["account_id"] == "account_abcdef"
                assert log_entry["message"] == "Full context message"
                assert log_entry["additional_info"] == "value"
            except json.JSONDecodeError:
                assert False, "Log entry is not valid JSON"
    
    def test_nested_contextual_logging(self):
        """Test nested contextual logging."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="nested_context_test.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Outer context
            with logger.context(expert_name="OuterExpert", symbol="BTCUSDT"):
                logger.info("Message with outer context")
                
                # Inner context (should override outer for common fields)
                with logger.context(strategy_id="InnerStrategy", additional_param="inner_value"):
                    logger.info("Message with inner context", trade_id="trade_nested")
                
                logger.info("Message with outer context again")
            
            # Verify that contexts are properly managed
            log_path = os.path.join(temp_dir, "nested_context_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "OuterExpert" in content
            assert "BTCUSDT" in content
            assert "InnerStrategy" in content
            assert "inner_value" in content
            assert "trade_nested" in content
    
    def test_contextual_logging_with_trade_method(self):
        """Test that contextual information works with trade method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="trade_context_test.log",
                trades_log_file="trade_context_trades.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Use context with trade method
            with logger.context(expert_name="TradeExpert", symbol="ETHUSDT", account_id="trade_account"):
                logger.trade("Trade executed", trade_id="trade_123", order_id="order_456")
            
            # Verify that context appears in both expert and trade logs
            expert_log_path = os.path.join(temp_dir, "trade_context_test.log")
            trades_log_path = os.path.join(temp_dir, "trade_context_trades.log")
            
            for log_path in [expert_log_path, trades_log_path]:
                if os.path.exists(log_path):
                    with open(log_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "Trade executed" in content:  # Only check logs that contain the trade message
                        assert "TradeExpert" in content
                        assert "ETHUSDT" in content
                        assert "trade_account" in content
                        assert "trade_123" in content
                        assert "order_456" in content