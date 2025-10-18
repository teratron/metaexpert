"""Acceptance tests for log file separation in the MetaExpert logging system."""

import os
import tempfile

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestLogSeparationAcceptance:
    """Acceptance tests for user story 2: Log Different Event Types to Appropriate Files."""
    
    def test_general_events_appear_in_expert_log(self):
        """Verify general events appear in expert.log (acceptance scenario 1)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with custom file names to make verification easier
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="acceptance_expert.log",
                trades_log_file="acceptance_trades.log",
                errors_log_file="acceptance_errors.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Log various general events
            logger.info("General info message")
            logger.debug("General debug message")
            logger.warning("General warning message")
            
            # Check that expert log contains the general events
            expert_log_path = os.path.join(temp_dir, "acceptance_expert.log")
            
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
            
            # Verify that the general events appear in expert.log
            assert "General info message" in expert_content
            assert "General debug message" in expert_content
            assert "General warning message" in expert_content
    
    def test_trade_events_appear_in_trades_log(self):
        """Verify trade events appear in trades.log (acceptance scenario 2)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with custom file names to make verification easier
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="acceptance_expert.log",
                trades_log_file="acceptance_trades.log",
                errors_log_file="acceptance_errors.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Log trade events using the trade method
            logger.trade("Trade executed successfully", 
                        symbol="BTCUSDT", 
                        trade_id="trade_123456",
                        order_id="order_789012")
            
            # Also log an info message with category="trade"
            logger.info("Trade information", category="trade", symbol="ETHUSDT", trade_id="trade_789012")
            
            # Check that trades log contains the trade events
            trades_log_path = os.path.join(temp_dir, "acceptance_trades.log")
            
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                trades_content = f.read()
            
            # Verify that the trade events appear in trades.log
            assert "Trade executed successfully" in trades_content
            assert "BTCUSDT" in trades_content
            assert "trade_123456" in trades_content
            assert "order_789012" in trades_content
            
            assert "Trade information" in trades_content
            assert "ETHUSDT" in trades_content
            assert "trade_789012" in trades_content
    
    def test_error_events_appear_in_errors_log(self):
        """Verify error events appear in errors.log (acceptance scenario 3)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with custom file names to make verification easier
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="acceptance_expert.log",
                trades_log_file="acceptance_trades.log",
                errors_log_file="acceptance_errors.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Log error events
            logger.error("An error occurred", error_code="E001", details="Connection failed")
            logger.critical("A critical error occurred", error_code="C001", details="System down")
            
            # Check that errors log contains the error events
            errors_log_path = os.path.join(temp_dir, "acceptance_errors.log")
            
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_content = f.read()
            
            # Verify that the error events appear in errors.log
            assert "An error occurred" in errors_content
            assert "E001" in errors_content
            assert "Connection failed" in errors_content
            
            assert "A critical error occurred" in errors_content
            assert "C001" in errors_content
            assert "System down" in errors_content
            
            # Verify that error events do NOT appear in other logs
            expert_log_path = os.path.join(temp_dir, "acceptance_expert.log")
            trades_log_path = os.path.join(temp_dir, "acceptance_trades.log")
            
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
            
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                trades_content = f.read()
            
            # Error messages should not appear in expert.log or trades.log
            assert "An error occurred" not in expert_content or "E001" not in expert_content
            assert "A critical error occurred" not in expert_content or "C001" not in expert_content
            assert "An error occurred" not in trades_content or "E001" not in trades_content
            assert "A critical error occurred" not in trades_content or "C001" not in trades_content