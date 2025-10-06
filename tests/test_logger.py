
import logging
import os
import shutil
import unittest
from pathlib import Path

# Temporarily adjust path to import from the source
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from metaexpert.config import (
    APP_NAME,
    LOG_DIRECTORY,
    LOG_FILE,
    LOG_TRADE_FILE,
    LOG_ERROR_FILE,
)
from metaexpert.logger import get_logger, shutdown_loggers, MetaLogger, TRADE_LEVEL_NUM, REPORT_LEVEL_NUM

class TestMetaLogger(unittest.TestCase):
    """Tests for the MetaLogger class and logging system."""

    def setUp(self):
        """Set up a temporary log directory for isolated testing."""
        self.test_log_dir = Path(LOG_DIRECTORY)
        # Clean up any previous test runs
        if self.test_log_dir.exists():
            shutil.rmtree(self.test_log_dir)
        self.test_log_dir.mkdir(exist_ok=True)

        # Ensure loggers are reset before each test
        shutdown_loggers()

    def tearDown(self):
        """Clean up temporary log files and directories after each test."""
        shutdown_loggers()
        if self.test_log_dir.exists():
            shutil.rmtree(self.test_log_dir)

    def test_initialization_and_get_logger(self):
        """Test that get_logger returns a configured MetaLogger instance."""
        logger = get_logger(APP_NAME)
        self.assertIsInstance(logger, MetaLogger)
        self.assertEqual(logger.name, APP_NAME)
        self.assertTrue(len(logger.handlers) > 0, "Logger should have handlers after initialization")

    def test_log_file_creation(self):
        """Test that log files are created upon logging."""
        logger = get_logger(APP_NAME)
        logger.info("Initial message to trigger file creation.")

        self.assertTrue((self.test_log_dir / LOG_FILE).exists())
        self.assertTrue((self.test_log_dir / LOG_TRADE_FILE).exists())
        self.assertTrue((self.test_log_dir / LOG_ERROR_FILE).exists())

    def test_standard_logging(self):
        """Test standard info and error logging to the correct files."""
        logger = get_logger(APP_NAME)
        
        # Log messages
        info_message = "This is an info message."
        error_message = "This is an error message."
        
        logger.info(info_message)
        logger.error(error_message)
        
        # Read log files
        main_log_content = (self.test_log_dir / LOG_FILE).read_text()
        error_log_content = (self.test_log_dir / LOG_ERROR_FILE).read_text()

        # Assertions
        self.assertIn(info_message, main_log_content)
        self.assertIn(error_message, main_log_content) # Errors also go to main log
        self.assertIn(error_message, error_log_content)
        self.assertNotIn(info_message, error_log_content)

    def test_custom_trade_logging(self):
        """Test the custom .trade() method and TRADE level."""
        logger = get_logger(APP_NAME)
        trade_logger = get_logger(f"{APP_NAME}.trade")

        trade_message = "Executing buy order for BTC/USDT."
        
        # The .trade() method is on the main logger instance
        logger.trade(trade_message)

        # Read log files
        main_log_content = (self.test_log_dir / LOG_FILE).read_text()
        trade_log_content = (self.test_log_dir / LOG_TRADE_FILE).read_text()

        # Assertions
        self.assertNotIn(trade_message, main_log_content) # Should not be in main log
        self.assertIn(trade_message, trade_log_content)

    def test_custom_report_logging(self):
        """Test the custom .report() method and REPORT level."""
        logger = get_logger(APP_NAME)
        
        report_message = "Weekly performance report generated."
        logger.report(report_message)

        main_log_content = (self.test_log_dir / LOG_FILE).read_text()
        
        # REPORT level messages should go to the main log file by default
        self.assertIn(report_message, main_log_content)
        self.assertIn("REPORT", main_log_content)

    def test_logger_idempotency(self):
        """Test that get_logger() returns the same instance (is idempotent)."""
        logger1 = get_logger(APP_NAME)
        logger2 = get_logger(APP_NAME)
        
        self.assertIs(logger1, logger2, "get_logger should return the same instance for the same name")
        self.assertEqual(len(logger1.handlers), len(logger2.handlers), "Handler count should not change on subsequent calls")

    def test_shutdown_loggers(self):
        """Test that shutdown_loggers clears the cache and allows re-configuration."""
        logger1 = get_logger("test_shutdown")
        self.assertIsInstance(logger1, MetaLogger)

        shutdown_loggers()

        # After shutdown, getting the logger should create a new instance
        logger2 = get_logger("test_shutdown")
        self.assertIsNot(logger1, logger2, "A new logger instance should be created after shutdown")
        self.assertIsInstance(logger2, MetaLogger)

if __name__ == '__main__':
    unittest.main()
