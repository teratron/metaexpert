"""Integration tests for basic logger functionality in the MetaExpert logging system."""

import os
import tempfile
import time
from pathlib import Path

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestBasicLoggerIntegration:
    """Integration tests for basic logger functionality."""
    
    def test_basic_logging_creates_files(self):
        """Test that basic logging creates the expected log files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with custom directory
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="test_expert.log",
                trades_log_file="test_trades.log",
                errors_log_file="test_errors.log"
            )
            
            logger = MetaLogger(config=config)
            
            # Log some messages
            logger.info("This is an info message")
            logger.warning("This is a warning message")
            logger.error("This is an error message")
            logger.trade("Trade executed", symbol="BTCUSDT", trade_id="123456")
            
            # Verify that the expected log files were created
            expert_log_path = os.path.join(temp_dir, "test_expert.log")
            trades_log_path = os.path.join(temp_dir, "test_trades.log")
            errors_log_path = os.path.join(temp_dir, "test_errors.log")
            
            assert os.path.exists(expert_log_path), "Expert log file should exist"
            assert os.path.exists(trades_log_path), "Trades log file should exist"
            assert os.path.exists(errors_log_path), "Errors log file should exist"
    
    def test_logging_with_different_levels(self):
        """Test that logging works with different log levels."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with debug level to capture all messages
            config = LogConfiguration(
                log_directory=temp_dir,
                log_level="DEBUG",
                expert_log_file="level_test.log"
            )
            
            logger = MetaLogger(config=config)
            
            # Log messages at different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
            
            # Read the log file to verify messages were written
            log_path = os.path.join(temp_dir, "level_test.log")
            
            assert os.path.exists(log_path), "Log file should exist"
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check that messages appear in the log
            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content
            assert "Critical message" in content
    
    def test_logging_with_context(self):
        """Test that logging works with contextual information."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_test.log",
                enable_contextual_logging=True
            )
            
            logger = MetaLogger(config=config)
            
            # Log with context using bind
            contextual_logger = logger.bind({"expert_name": "TestExpert", "symbol": "BTCUSDT"})
            contextual_logger.info("Processing trade", trade_id="123456")
            
            # Log with context using context manager
            with logger.context(expert_name="ContextExpert", strategy_id="TestStrategy"):
                logger.info("Inside context", order_id="789012")
            
            # Read the log file to verify context was included
            log_path = os.path.join(temp_dir, "context_test.log")
            
            assert os.path.exists(log_path), "Log file should exist"
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check that contextual information appears in the log
            assert "TestExpert" in content
            assert "BTCUSDT" in content
            assert "123456" in content
            assert "ContextExpert" in content
            assert "TestStrategy" in content
            assert "789012" in content
    
    def test_async_logging_functionality(self):
        """Test that async logging works without blocking."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with async enabled
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="async_test.log",
                enable_async=True
            )
            
            logger = MetaLogger(config=config)
            
            # Log a series of messages
            start_time = time.time()
            for i in range(10):
                logger.info(f"Async message {i}", iteration=i)
            end_time = time.time()
            
            # With async logging, these operations should be very fast
            # (though they might still be synchronous in this test environment)
            elapsed_time = end_time - start_time
            print(f"Time to log 10 messages: {elapsed_time:.4f} seconds")
            
            # Verify that the log file exists
            log_path = os.path.join(temp_dir, "async_test.log")
            assert os.path.exists(log_path), "Log file should exist"
    
    def test_structured_logging_output(self):
        """Test that structured logging produces JSON output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with structured logging enabled
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="structured_test.log",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log a message
            logger.info("Structured log message", 
                       expert_name="TestExpert", 
                       symbol="ETHUSDT", 
                       trade_id="111222")
            
            # Read the log file to verify JSON format
            log_path = os.path.join(temp_dir, "structured_test.log")
            
            assert os.path.exists(log_path), "Log file should exist"
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check that the content looks like JSON (starts with '{')
            assert content.strip().startswith('{'), "Structured log should produce JSON"
            assert "Structured log message" in content
            assert "TestExpert" in content
            assert "ETHUSDT" in content
            assert "111222" in content