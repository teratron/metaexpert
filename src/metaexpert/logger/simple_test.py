"""Simple test script to verify the refactored logger works correctly."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test importing the logger module directly
try:
    from metaexpert.logger import MetaLogger
    
    # Test creating a logger instance
    logger = MetaLogger(
        log_level="INFO",
        log_file="test.log",
        trade_log_file="trade.log",
        error_log_file="error.log",
        log_to_console=True,
        structured_logging=True,
        async_logging=True,
    )
    
    # Test getting a logger
    main_logger = logger.get_main_logger()
    print("MetaLogger imported and instantiated successfully!")
    
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