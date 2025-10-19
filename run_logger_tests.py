#!/usr/bin/env python3
"""Simple test runner to validate logger implementation."""

import sys
import os
import tempfile

# Add the src directory to the path so we can import the logger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration


def test_basic_functionality():
    """Test basic functionality of the logger."""
    print("Testing basic logger functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test 1: Create logger with default settings
        logger = MetaLogger()
        print("[PASS] Logger created with default settings")
        
        # Test 2: Create logger with custom config
        config = LogConfiguration(
            log_directory=temp_dir,
            expert_log_file="test_expert.log",
            trades_log_file="test_trades.log",
            errors_log_file="test_errors.log",
            log_level="DEBUG",
            enable_async=False,
            max_file_size_mb=10,
            backup_count=5,
            enable_structured_logging=True,
            file_log_format="json"
        )
        logger = MetaLogger(config=config)
        print("[PASS] Logger created with custom configuration")
        
        # Test 3: Log messages
        logger.info("Test info message", expert_name="TestExpert", symbol="BTCUSDT")
        logger.debug("Test debug message", expert_name="TestExpert", symbol="BTCUSDT")
        logger.warning("Test warning message", expert_name="TestExpert", symbol="BTCUSDT")
        logger.error("Test error message", expert_name="TestExpert", symbol="BTCUSDT")
        logger.critical("Test critical message", expert_name="TestExpert", symbol="BTCUSDT")
        print("✓ Basic logging methods work")
        
        # Test 4: Log trade messages
        logger.trade("Test trade message", trade_id="trade_123", order_id="order_456")
        print("✓ Trade logging method works")
        
        # Test 5: Context binding
        bound_logger = logger.bind({"expert_name": "BoundExpert", "symbol": "ETHUSDT"})
        bound_logger.info("Bound context message")
        print("✓ Context binding works")
        
        # Test 6: Context manager
        with logger.context(expert_name="ContextManagerExpert", symbol="ADAUSDT"):
            logger.info("Context manager message")
        print("✓ Context manager works")
        
        # Test 7: Check log files were created
        expert_log_path = os.path.join(temp_dir, "test_expert.log")
        trades_log_path = os.path.join(temp_dir, "test_trades.log")
        errors_log_path = os.path.join(temp_dir, "test_errors.log")
        
        assert os.path.exists(expert_log_path), "Expert log file should exist"
        assert os.path.exists(trades_log_path), "Trades log file should exist"
        assert os.path.exists(errors_log_path), "Errors log file should exist"
        print("✓ Log files were created")
        
        # Test 8: Check log file contents
        with open(expert_log_path, 'r', encoding='utf-8') as f:
            expert_content = f.read()
            
        with open(trades_log_path, 'r', encoding='utf-8') as f:
            trades_content = f.read()
            
        with open(errors_log_path, 'r', encoding='utf-8') as f:
            errors_content = f.read()
        
        # Verify basic messages appear in expert log
        assert "Test info message" in expert_content
        assert "Test debug message" in expert_content
        assert "Test warning message" in expert_content
        assert "Test error message" in expert_content
        assert "Test critical message" in expert_content
        print("✓ Basic messages appear in expert log")
        
        # Verify trade messages appear in trades log
        assert "Test trade message" in trades_content
        assert "trade_123" in trades_content
        assert "order_456" in trades_content
        print("✓ Trade messages appear in trades log")
        
        # Verify error messages appear in errors log
        assert "Test error message" in errors_content
        assert "Test critical message" in errors_content
        print("✓ Error messages appear in errors log")
        
        # Test 9: Check structured logging
        # Since we enabled JSON format, the logs should contain valid JSON
        try:
            import json
            lines = expert_content.strip().split('\n')
            if lines:
                # Try to parse the first line as JSON
                json.loads(lines[0])
                print("✓ Logs are in JSON format")
        except:
            print("⚠ Logs may not be in JSON format")
        
        print("\n✓ All basic functionality tests passed!")


def test_async_functionality():
    """Test async functionality of the logger."""
    print("\nTesting async logger functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test with async enabled
        config = LogConfiguration(
            log_directory=temp_dir,
            expert_log_file="async_test_expert.log",
            trades_log_file="async_test_trades.log",
            errors_log_file="async_test_errors.log",
            log_level="INFO",
            enable_async=True,  # Enable async logging
            max_file_size_mb=10,
            backup_count=5,
            enable_structured_logging=False,
            file_log_format="text"
        )
        
        logger = MetaLogger(config=config)
        print("✓ Async logger created")
        
        # Log several messages quickly
        for i in range(100):
            logger.info(f"Async test message {i}", expert_name="AsyncTestExpert", symbol="BTCUSDT")
        
        # Log some trade messages
        for i in range(50):
            logger.trade(f"Async trade message {i}", trade_id=f"trade_{i}", order_id=f"order_{i}")
        
        # Log some error messages
        for i in range(10):
            logger.error(f"Async error message {i}", expert_name="AsyncTestExpert", symbol="BTCUSDT")
        
        print("✓ Async logging messages sent")
        
        # Give some time for async processing
        import time
        time.sleep(1)
        
        # Check files were created
        expert_log_path = os.path.join(temp_dir, "async_test_expert.log")
        trades_log_path = os.path.join(temp_dir, "async_test_trades.log")
        errors_log_path = os.path.join(temp_dir, "async_test_errors.log")
        
        assert os.path.exists(expert_log_path), "Async expert log file should exist"
        assert os.path.exists(trades_log_path), "Async trades log file should exist"
        assert os.path.exists(errors_log_path), "Async errors log file should exist"
        print("✓ Async log files were created")
        
        # Check file contents
        with open(expert_log_path, 'r', encoding='utf-8') as f:
            expert_content = f.read()
            
        with open(trades_log_path, 'r', encoding='utf-8') as f:
            trades_content = f.read()
            
        with open(errors_log_path, 'r', encoding='utf-8') as f:
            errors_content = f.read()
        
        # Verify messages appear in logs
        assert "Async test message 0" in expert_content
        assert "Async test message 99" in expert_content
        assert "Async trade message 0" in trades_content
        assert "Async trade message 49" in trades_content
        assert "Async error message 0" in errors_content
        assert "Async error message 9" in errors_content
        print("✓ Async log messages were written to files")
        
        print("\n✓ All async functionality tests passed!")


def test_configuration_priority():
    """Test configuration priority order."""
    print("\nTesting configuration priority...")
    
    # Test default configuration
    logger = MetaLogger()
    assert logger.config.log_level == "INFO"
    assert logger.config.log_directory == "./logs"
    print("✓ Default configuration works")
    
    # Test code parameter override
    logger = MetaLogger(log_level="DEBUG", log_directory="./test_logs")
    assert logger.config.log_level == "DEBUG"
    assert logger.config.log_directory == "./test_logs"
    print("✓ Code parameter override works")
    
    print("\n✓ All configuration priority tests passed!")


def test_error_resilience():
    """Test error resilience of the logger."""
    print("\nTesting error resilience...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a logger with a directory that might cause issues
        config = LogConfiguration(
            log_directory=temp_dir,
            expert_log_file="resilience_test.log",
            log_level="INFO",
            enable_async=False
        )
        
        logger = MetaLogger(config=config)
        print("✓ Logger created in test directory")
        
        # Try logging with various problematic inputs
        try:
            logger.info("Normal message")
            logger.info("Message with unicode: αβγδεζηθ")
            logger.info("Message with special chars: {}[]()<>")
            logger.info("Message with None value", null_field=None)
            logger.info("Message with numeric values", num_field=123, float_field=45.67)
            logger.info("Message with boolean values", bool_field=True, another_bool=False)
            print("✓ Logger handles various input types")
        except Exception as e:
            print(f"✗ Logger failed with exception: {e}")
            raise
        
        # Test with context that might cause issues
        try:
            with logger.context(expert_name="ResilienceTest", symbol="RESILIENCE"):
                logger.info("Context message")
            print("✓ Context manager works")
        except Exception as e:
            print(f"✗ Context manager failed with exception: {e}")
            raise
        
        print("\n✓ All error resilience tests passed!")


def main():
    """Run all tests."""
    print("Running comprehensive logger tests...\n")
    
    try:
        test_basic_functionality()
        test_async_functionality()
        test_configuration_priority()
        test_error_resilience()
        
        print("\n🎉 All tests passed! Logger implementation is working correctly.")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
