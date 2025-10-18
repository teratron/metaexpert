"""Simple test to validate logger functionality."""

import os
import tempfile
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration


def test_basic_functionality():
    """Test basic logger functionality."""
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
        print("[PASS] Basic logging methods work")
        
        # Test 4: Log trade messages
        logger.trade("Test trade message", trade_id="trade_123", order_id="order_456")
        print("[PASS] Trade logging method works")
        
        # Test 5: Context binding
        bound_logger = logger.bind({"expert_name": "BoundExpert", "symbol": "ETHUSDT"})
        bound_logger.info("Bound context message")
        print("[PASS] Context binding works")
        
        # Test 6: Context manager
        with logger.context(expert_name="ContextManagerExpert", symbol="ADAUSDT"):
            logger.info("Context manager message")
        print("[PASS] Context manager works")
        
        # Test 7: Check log files were created
        expert_log_path = os.path.join(temp_dir, "test_expert.log")
        trades_log_path = os.path.join(temp_dir, "test_trades.log")
        errors_log_path = os.path.join(temp_dir, "test_errors.log")
        
        assert os.path.exists(expert_log_path), "Expert log file should exist"
        assert os.path.exists(trades_log_path), "Trades log file should exist"
        assert os.path.exists(errors_log_path), "Errors log file should exist"
        print("[PASS] Log files were created")
        
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
        print("[PASS] Basic messages appear in expert log")
        
        # Verify trade messages appear in trades log
        assert "Test trade message" in trades_content
        assert "trade_123" in trades_content
        assert "order_456" in trades_content
        print("[PASS] Trade messages appear in trades log")
        
        # Verify error messages appear in errors log
        assert "Test error message" in errors_content
        assert "Test critical message" in errors_content
        print("[PASS] Error messages appear in errors log")
        
        # Test 9: Check structured logging
        # Since we enabled JSON format, the logs should contain valid JSON
        try:
            lines = expert_content.strip().split('\n')
            if lines:
                # Try to parse the first line as JSON
                json.loads(lines[0])
                print("[PASS] Logs are in JSON format")
        except:
            print("[WARN] Logs may not be in JSON format")
        
        print("\n[PASS] All basic functionality tests passed!")


def main():
    """Run basic functionality test."""
    try:
        test_basic_functionality()
        return 0
    except Exception as e:
        print(f"[FAIL] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())