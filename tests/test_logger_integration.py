"""Test script for MetaExpert logging system integration.

This script tests the enhanced logging functionality to ensure
proper integration with the MetaExpert trading system.
"""

import sys
import tempfile
from pathlib import Path

from metaexpert.logger import (
    configure_expert_logging,
    get_error_logger,
    get_logger,
    get_main_logger,
    get_trade_logger,
    log_expert_error,
    log_expert_shutdown,
    log_expert_startup,
    log_trade_execution,
    shutdown_logging,
)


def test_basic_logging() -> bool:
    """Test basic logging functionality."""
    print("Testing basic logging functionality...")

    try:
        # Get basic logger
        logger = get_logger()
        logger.info("Basic logging test message")

        # Get specialized loggers
        main_logger = get_main_logger()
        trade_logger = get_trade_logger()
        error_logger = get_error_logger()

        main_logger.info("Main logger test")
        trade_logger.info("Trade logger test")
        error_logger.error("Error logger test")

        print("✓ Basic logging test passed")
        return True

    except Exception as e:
        print(f"✗ Basic logging test failed: {e}")
        return False


def test_expert_configuration() -> bool:
    """Test expert-specific configuration."""
    print("Testing expert configuration...")

    try:
        # Create temporary directory for test logs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Configure with expert parameters
            result = configure_expert_logging(
                log_level="DEBUG",
                log_file="test_expert.log",
                trade_log_file="test_trades.log",
                error_log_file="test_errors.log",
                log_to_console=True,
                structured_logging=False,
                async_logging=False,
                log_directory=str(temp_path),
            )

            if result["status"] != "success":
                print(f"✗ Configuration failed: {result['message']}")
                return False

            # Test logging after configuration
            main_logger = get_main_logger()
            main_logger.debug("Debug message test")
            main_logger.info("Info message test")

            # Check if log files were created
            log_files = ["test_expert.log", "test_trades.log", "test_errors.log"]
            for log_file in log_files:
                log_path = temp_path / log_file
                if not log_path.exists():
                    print(f"✗ Log file not created: {log_file}")
                    return False

            print("✓ Expert configuration test passed")
            return True

    except Exception as e:
        print(f"✗ Expert configuration test failed: {e}")
        return False


def test_structured_logging() -> bool:
    """Test structured JSON logging."""
    print("Testing structured logging...")

    try:
        # Create temporary directory for test logs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Configure with structured logging
            result = configure_expert_logging(
                log_level="INFO",
                log_file="structured_test.log",
                structured_logging=True,
                log_directory=str(temp_path),
            )

            if result["status"] != "success":
                print(f"✗ Structured logging configuration failed: {result['message']}")
                return False

            # Test structured logging
            logger = get_main_logger()
            logger.info("Structured logging test message")

            # Check if log file contains JSON
            log_path = temp_path / "structured_test.log"
            if log_path.exists():
                content = log_path.read_text()
                if '{"timestamp"' in content and '"level"' in content:
                    print("✓ Structured logging test passed")
                    return True
                else:
                    print("✗ Log content is not structured JSON")
                    return False
            else:
                print("✗ Structured log file not created")
                return False

    except Exception as e:
        print(f"✗ Structured logging test failed: {e}")
        return False


def test_convenience_functions() -> bool:
    """Test convenience logging functions."""
    print("Testing convenience functions...")

    try:
        # Test expert lifecycle logging
        log_expert_startup("TestExpert", "binance", "BTCUSDT", "1h")
        log_expert_shutdown("TestExpert", "test_complete")

        # Test trade logging
        log_trade_execution(
            symbol="BTCUSDT",
            side="BUY",
            quantity=0.001,
            price=50000.0,
            order_id="test_order_123",
            strategy_id=1001,
        )

        # Test error logging
        try:
            raise ValueError("Test exception for logging")
        except ValueError as e:
            log_expert_error(
                "Test error occurred",
                exception=e,
                component="test_module",
                operation="test_operation",
            )

        print("✓ Convenience functions test passed")
        return True

    except Exception as e:
        print(f"✗ Convenience functions test failed: {e}")
        return False


def test_async_logging() -> bool:
    """Test asynchronous logging."""
    print("Testing asynchronous logging...")

    try:
        # Create temporary directory for test logs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Configure with async logging
            result = configure_expert_logging(
                log_level="INFO",
                log_file="async_test.log",
                async_logging=True,
                log_directory=str(temp_path),
            )

            if result["status"] != "success":
                print(f"✗ Async logging configuration failed: {result['message']}")
                return False

            # Test async logging with multiple messages
            logger = get_main_logger()
            for i in range(10):
                logger.info(f"Async test message {i}")

            # Give async handlers time to process
            import time
            time.sleep(0.5)

            # Check if log file was created and contains messages
            log_path = temp_path / "async_test.log"
            if log_path.exists():
                content = log_path.read_text()
                if "Async test message" in content:
                    print("✓ Async logging test passed")
                    return True
                else:
                    print("✗ Async log messages not found")
                    return False
            else:
                print("✗ Async log file not created")
                return False

    except Exception as e:
        print(f"✗ Async logging test failed: {e}")
        return False


def run_all_tests() -> bool:
    """Run all logging tests."""
    print("=" * 50)
    print("MetaExpert Logging System Integration Tests")
    print("=" * 50)

    tests = [
        test_basic_logging,
        test_expert_configuration,
        test_structured_logging,
        test_convenience_functions,
        test_async_logging,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            print()

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 50)

    # Clean up
    try:
        shutdown_logging()
    except Exception:
        pass

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
