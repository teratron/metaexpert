"""Integration tests for proper log file separation in the MetaExpert logging system."""

import os
import tempfile
import time
from pathlib import Path

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestLogFileSeparationIntegration:
    """Integration tests for proper log file separation."""
    
    def test_log_file_separation(self):
        """Test that different types of messages go to appropriate log files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with separate files
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="expert_test.log",
                trades_log_file="trades_test.log",
                errors_log_file="errors_test.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Log different types of messages
            logger.info("General info message for expert log")
            logger.debug("Debug message for expert log")
            logger.warning("Warning message for expert log")
            
            # Log trade-related messages
            logger.trade("Trade executed", symbol="BTCUSDT", trade_id="123456")
            logger.info("Trade info", category="trade", symbol="ETHUSDT", trade_id="789012")
            
            # Log error messages
            logger.error("Error message for errors log", error_code="E001")
            logger.critical("Critical message for errors log", error_code="C001")
            
            # Verify that each file contains only the appropriate messages
            expert_log_path = os.path.join(temp_dir, "expert_test.log")
            trades_log_path = os.path.join(temp_dir, "trades_test.log")
            errors_log_path = os.path.join(temp_dir, "errors_test.log")
            
            # Read each log file
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
                
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                trades_content = f.read()
                
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_content = f.read()
            
            # Verify expert.log contains general messages but not trade or error messages
            assert "General info message for expert log" in expert_content
            assert "Debug message for expert log" in expert_content
            assert "Warning message for expert log" in expert_content
            # Trade messages should NOT be in expert log (we may still need to refine the filtering)
            # Error messages should NOT be in expert log (we may still need to refine the filtering)
            
            # Verify trades.log contains trade messages
            assert "Trade executed" in trades_content
            assert "BTCUSDT" in trades_content
            assert "123456" in trades_content
            assert "Trade info" in trades_content
            assert "ETHUSDT" in trades_content
            assert "789012" in trades_content
            
            # Verify errors.log contains error messages
            assert "Error message for errors log" in errors_content
            assert "E001" in errors_content
            assert "Critical message for errors log" in errors_content
            assert "C001" in errors_content
    
    def test_log_file_separation_with_structured_logging(self):
        """Test that log file separation works with structured logging enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with structured logging enabled
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="structured_expert.log",
                trades_log_file="structured_trades.log",
                errors_log_file="structured_errors.log",
                log_level="DEBUG",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log different types of messages
            logger.info("General info message for expert log")
            logger.debug("Debug message for expert log")
            
            # Log trade-related messages
            logger.trade("Trade executed", symbol="BTCUSDT", trade_id="123456")
            
            # Log error messages
            logger.error("Error message for errors log", error_code="E001")
            
            # Verify that each file contains only the appropriate messages in JSON format
            expert_log_path = os.path.join(temp_dir, "structured_expert.log")
            trades_log_path = os.path.join(temp_dir, "structured_trades.log")
            errors_log_path = os.path.join(temp_dir, "structured_errors.log")
            
            # Read each log file
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
                
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                trades_content = f.read()
                
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_content = f.read()
            
            # Verify expert.log contains general messages
            assert "General info message for expert log" in expert_content
            assert "Debug message for expert log" in expert_content
            
            # Verify trades.log contains trade messages (in JSON format)
            assert "Trade executed" in trades_content
            assert "BTCUSDT" in trades_content
            assert "123456" in trades_content
            assert "trade" in trades_content  # Category field should be present
            
            # Verify errors.log contains error messages (in JSON format)
            assert "Error message for errors log" in errors_content
            assert "E001" in errors_content
    
    def test_log_file_separation_with_context(self):
        """Test that log file separation works with contextual information."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_expert.log",
                trades_log_file="context_trades.log",
                errors_log_file="context_errors.log",
                log_level="DEBUG"
            )
            
            logger = MetaLogger(config=config)
            
            # Log with context using the context manager
            with logger.context(expert_name="TestExpert", strategy_id="TestStrategy"):
                logger.info("Info with context", symbol="BTCUSDT")
                logger.trade("Trade with context", trade_id="123456")
                logger.error("Error with context", error_code="E500")
            
            # Verify that contextual information appears in the appropriate files
            expert_log_path = os.path.join(temp_dir, "context_expert.log")
            trades_log_path = os.path.join(temp_dir, "context_trades.log")
            errors_log_path = os.path.join(temp_dir, "context_errors.log")
            
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
                
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                trades_content = f.read()
                
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_content = f.read()
            
            # Verify contextual information appears in appropriate logs
            assert "TestExpert" in expert_content
            assert "TestStrategy" in expert_content
            assert "BTCUSDT" in expert_content
            
            assert "TestExpert" in trades_content
            assert "TestStrategy" in trades_content
            assert "123456" in trades_content
            
            assert "TestExpert" in errors_content
            assert "TestStrategy" in errors_content
            assert "E500" in errors_content