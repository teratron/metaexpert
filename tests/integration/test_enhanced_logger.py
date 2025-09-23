"""Quick test to verify the enhanced logger functionality."""

import logging
from metaexpert.logger import setup_logger, get_logger
from metaexpert.logger.structured_log_formatter import StructuredLogFormatter
from metaexpert.logger.async_log_handler import AsyncLogHandler
from metaexpert.logger.performance_monitor import PerformanceMonitor


def test_enhanced_logger_imports():
    """Test that all enhanced logger components can be imported."""
    # Test basic logger setup
    logger = setup_logger("test_enhanced_logger")
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    
    # Test getting logger
    logger2 = get_logger("test_enhanced_logger")
    assert logger2 is logger  # Should return the same instance
    
    # Test structured formatter
    formatter = StructuredLogFormatter()
    assert formatter is not None
    
    # Test async handler
    handler = AsyncLogHandler()
    assert handler is not None
    
    # Test performance monitor
    monitor = PerformanceMonitor()
    assert monitor is not None
    
    print("All enhanced logger components imported successfully!")


def test_enhanced_logger_functionality():
    """Test basic functionality of enhanced logger components."""
    # Test logger with structured formatting
    logger = setup_logger("test_functionality", structured=True)
    logger.info("This is a test message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test performance monitoring
    monitor = PerformanceMonitor()
    op_id = monitor.start_operation("test_operation")
    # Simulate some work
    import time
    time.sleep(0.001)  # 1ms
    monitor.end_operation(op_id, success=True)
    
    # Get performance report
    report = monitor.get_performance_report()
    assert "total_operations" in report
    
    print("Enhanced logger functionality test passed!")


if __name__ == "__main__":
    test_enhanced_logger_imports()
    test_enhanced_logger_functionality()
    print("All enhanced logger tests passed!")