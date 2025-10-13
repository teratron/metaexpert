"""Integration test to verify the refactored logger works properly."""

import tempfile

from metaexpert.logger import MetaLogger


def test_logger_integration():
    """Test that the refactored logger works with both structured and legacy logging."""
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()

    # Create log file paths
    log_file = temp_dir + "/test.log"
    trade_log_file = temp_dir + "/trade.log"
    error_log_file = temp_dir + "/error.log"

    # Initialize logger with structured logging
    logger = MetaLogger(
        log_level="INFO",
        log_file=log_file,
        trade_log_file=trade_log_file,
        error_log_file=error_log_file,
        log_to_console=False,
        structured_logging=True,
        async_logging=True,  # Enable async as per original design
    )

    # Test basic logging
    main_logger = logger.get_main_logger()
    main_logger.info("Test message", test_id=1, category="integration")

    # Test legacy logging with extra dict
    logger.log_trade("Test trade", extra={"symbol": "BTCUSDT", "amount": 1.5})

    # Test error logging
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        logger.log_error("Test error occurred", exception=e, error_code="TEST001")

    # Test context binding
    context_logger = main_logger.bind(strategy_name="test_strategy", version="1.0")
    context_logger.info("Message with context")

    # Check performance stats
    perf_stats = logger.log_performance_stats()
    print(f"Performance stats: {perf_stats}")

    # Cleanup
    logger.shutdown()

    print("Integration test completed successfully!")


if __name__ == "__main__":
    test_logger_integration()
