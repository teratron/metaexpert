"""Standalone test for the refactored logger module."""

import logging
import logging.handlers
import sys
import os
import tempfile
from pathlib import Path

# Add the current directory to sys.path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

# Import our custom modules
from formatter import MainFormatter, TradeFormatter, ErrorFormatter
from async_handler import AsyncHandler

# Mock the config values that the logger module depends on
class MockConfig:
    LOG_BACKUP_COUNT = 5
    LOG_DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIRECTORY = "./logs"
    LOG_ERROR_LEVEL = "ERROR"
    LOG_FALLBACK_FORMAT = "%(levelname)s:%(name)s:%(message)s"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_NAME = "metaexpert"
    LOG_TRADE_LEVEL = "INFO"

# Replace the config imports with mock values
sys.modules['metaexpert.config'] = MockConfig

# Now try to import the logger module
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "logger", 
        Path(__file__).parent / "__init__.py"
    )
    logger_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logger_module)
    
    # Test creating a MetaLogger instance
    MetaLogger = getattr(logger_module, 'MetaLogger')
    logger = MetaLogger(
        log_level="INFO",
        log_file="test.log",
        trade_log_file="trade.log",
        error_log_file="error.log",
        log_to_console=True,
        structured_logging=True,
        async_logging=True,
    )
    
    print("MetaLogger module loaded successfully!")
    print("MetaLogger instance created successfully!")
    
    # Test getting a logger
    main_logger = logger.get_main_logger()
    print("Main logger retrieved successfully!")
    
    # Test logging a message
    main_logger.info("Test message", test_id=1, category="test")
    print("Logging works correctly!")
    
    # Test shutting down the logger
    logger.shutdown()
    print("Logger shutdown successfully!")
    
except Exception as e:
    print(f"Error testing logger: {e}")
    import traceback
    traceback.print_exc()