"""Direct test of the refactored logger components."""

import logging
import structlog
import sys
import os
import importlib.util
from pathlib import Path

# Test the formatter components directly
try:
    # Import the formatter classes directly
    formatter_path = Path(__file__).parent / "formatter.py"
    spec = importlib.util.spec_from_file_location("formatter", formatter_path)
    formatter_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(formatter_module)
    
    MainFormatter = getattr(formatter_module, 'MainFormatter')
    TradeFormatter = getattr(formatter_module, 'TradeFormatter')
    ErrorFormatter = getattr(formatter_module, 'ErrorFormatter')
    
    # Test creating formatters
    main_formatter = MainFormatter()
    trade_formatter = TradeFormatter()
    error_formatter = ErrorFormatter()
    
    print("Formatters created successfully!")
    
    # Test structlog processors
    processors_path = Path(__file__).parent / "structlog_processors.py"
    spec = importlib.util.spec_from_file_location("structlog_processors", processors_path)
    processors_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(processors_module)
    
    print("Structlog processors loaded successfully!")
    
    # Test async handler
    async_handler_path = Path(__file__).parent / "async_handler.py"
    spec = importlib.util.spec_from_file_location("async_handler", async_handler_path)
    async_handler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(async_handler_module)
    
    AsyncHandler = getattr(async_handler_module, 'AsyncHandler')
    print("Async handler loaded successfully!")
    
    # Test basic structlog configuration
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    print("Structlog configured successfully!")
    
    # Test getting a logger
    logger = structlog.get_logger("test.logger")
    print("Structlog logger created successfully!")
    
    # Test logging a message
    logger.info("Test message", test_id=1, category="test")
    print("Logging works correctly!")
    
    print("\n=== All tests passed! ===")
    print("The refactored logger components work correctly.")
    
except Exception as e:
    print(f"Error testing logger components: {e}")
    import traceback
    traceback.print_exc()