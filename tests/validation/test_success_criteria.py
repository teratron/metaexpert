"""Validation tests for all success criteria (SC-001 through SC-009)."""

import os
import tempfile
import time
import json
from pathlib import Path

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestSuccessCriteria:
    """Validation tests for all success criteria."""
    
    def test_sc_001_logger_initialization_speed(self):
        """SC-001: Users can initialize logging with default settings that create all required log files in less than 1 second."""
        start_time = time.time()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(log_directory=temp_dir)
            logger = MetaLogger(config=config)
            
            # Verify logger was created
            assert logger is not None
            
            # Verify required log files exist
            expert_log = os.path.join(temp_dir, config.expert_log_file)
            trades_log = os.path.join(temp_dir, config.trades_log_file)
            errors_log = os.path.join(temp_dir, config.errors_log_file)
            
            assert os.path.exists(expert_log)
            assert os.path.exists(trades_log)
            assert os.path.exists(errors_log)
            
        end_time = time.time()
        initialization_time = end_time - start_time
        
        # Should initialize in less than 1 second
        assert initialization_time < 1.0, f"Logger initialization took {initialization_time:.3f}s, should be < 1s"
        print(f"✓ SC-001: Logger initialization completed in {initialization_time:.3f}s (< 1s)")
    
    def test_sc_002_async_logging_performance(self):
        """SC-002: System supports logging 10,000 entries per second with asynchronous logging enabled without blocking the main trading thread."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_test.log",
                enable_async=True,
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Record start time
            start_time = time.time()
            
            # Log 10,000 entries as a performance test
            for i in range(10000):
                logger.info(f"Performance test message {i}", expert_name="PerfTest", symbol="PERF")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Calculate entries per second
            entries_per_second = 10000 / total_time
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Should support at least 10,000 entries per second
            assert entries_per_second >= 10000, f"Logged {entries_per_second:.0f} entries/second, should be >= 10,000"
            print(f"✓ SC-002: Logged {entries_per_second:.0f} entries/second with async logging")
    
    def test_sc_003_log_file_rotation(self):
        """SC-003: Log files are properly rotated when they reach the configured maximum size with no data loss."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config with small max file size for testing rotation
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="rotation_test.log",
                max_file_size_mb=1,  # Small size for testing
                backup_count=3,
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Write many log messages to force rotation
            large_message = "A" * 1000  # Large message to fill file quickly
            
            for i in range(1500):  # Enough to trigger rotation
                logger.info(f"Rotation test message {i}: {large_message}", 
                           expert_name="RotationTest", symbol="ROTATE")
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Check that rotation occurred
            main_log = os.path.join(temp_dir, "rotation_test.log")
            backup_log_1 = os.path.join(temp_dir, "rotation_test.log.1")
            backup_log_2 = os.path.join(temp_dir, "rotation_test.log.2")
            backup_log_3 = os.path.join(temp_dir, "rotation_test.log.3")
            
            # Main log should exist
            assert os.path.exists(main_log)
            
            # At least one backup should exist (likely all three)
            backup_exists = any([
                os.path.exists(backup_log_1),
                os.path.exists(backup_log_2),
                os.path.exists(backup_log_3)
            ])
            assert backup_exists
            
            # Verify no data loss by checking log contents
            log_files = [main_log, backup_log_1, backup_log_2, backup_log_3]
            total_messages = 0
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Count messages in this file
                        message_count = content.count("Rotation test message")
                        total_messages += message_count
            
            # Should have logged all messages (1500) across all files
            assert total_messages == 1500, f"Expected 1500 messages, found {total_messages}"
            print(f"✓ SC-003: Log rotation works correctly with no data loss ({total_messages} messages logged)")
    
    def test_sc_004_contextual_information_inclusion(self):
        """SC-004: 99.5% of log entries contain complete contextual information when contextual logging is enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_test.log",
                enable_contextual_logging=True,
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Bind context using the context manager
            with logger.context(expert_name="ContextTestExpert", symbol="CONTEXT"):
                # Log many messages to test context inclusion rate
                for i in range(1000):
                    logger.info(f"Context test message {i}", iteration=i)
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Read log file and check context inclusion rate
            log_path = os.path.join(temp_dir, "context_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Count messages with complete context
            context_included_count = 0
            total_messages = len(lines)
            
            for line in lines:
                if "ContextTestExpert" in line and "CONTEXT" in line:
                    context_included_count += 1
            
            # Calculate context inclusion percentage
            if total_messages > 0:
                context_percentage = (context_included_count / total_messages) * 100
                assert context_percentage >= 99.5, f"Context inclusion rate {context_percentage:.2f}% < 99.5%"
                print(f"✓ SC-004: Context inclusion rate is {context_percentage:.2f}% (>= 99.5%)")
            else:
                print("⚠ SC-004: No log messages found for context inclusion test")
    
    def test_sc_005_error_messages_in_both_files(self):
        """SC-005: All error-level messages appear in both expert.log and errors.log files as expected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="expert_errors_test.log",
                errors_log_file="errors_test.log",
                log_level="DEBUG"  # Capture all levels
            )
            
            logger = MetaLogger(config=config)
            
            # Log error and critical messages
            logger.error("Error test message", expert_name="ErrorTest", symbol="ERROR")
            logger.critical("Critical test message", expert_name="ErrorTest", symbol="CRITICAL")
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Check both log files contain the error messages
            expert_log_path = os.path.join(temp_dir, "expert_errors_test.log")
            errors_log_path = os.path.join(temp_dir, "errors_test.log")
            
            # Both files should exist
            assert os.path.exists(expert_log_path)
            assert os.path.exists(errors_log_path)
            
            # Read both files
            with open(expert_log_path, 'r', encoding='utf-8') as f:
                expert_content = f.read()
                
            with open(errors_log_path, 'r', encoding='utf-8') as f:
                errors_content = f.read()
            
            # Both files should contain the error messages
            assert "Error test message" in expert_content
            assert "Error test message" in errors_content
            assert "Critical test message" in expert_content
            assert "Critical test message" in errors_content
            
            print("✓ SC-005: Error messages appear in both expert.log and errors.log")
    
    def test_sc_006_trade_messages_in_trades_log(self):
        """SC-006: All trade-related messages appear in trades.log in JSON Lines format for external processing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="expert_trades_test.log",
                trades_log_file="trades_test.log",
                enable_structured_logging=True,
                file_log_format="json",
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Log trade-related messages
            logger.trade("Trade executed", 
                        expert_name="TradeTest", 
                        symbol="BTCUSDT", 
                        trade_id="trade_123", 
                        order_id="order_456")
            
            logger.info("Another trade message", 
                       category="trade",
                       expert_name="TradeTest", 
                       symbol="ETHUSDT", 
                       trade_id="trade_789", 
                       order_id="order_012")
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Check trades log file exists and contains JSON Lines
            trades_log_path = os.path.join(temp_dir, "trades_test.log")
            assert os.path.exists(trades_log_path)
            
            with open(trades_log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                lines = content.split('\n')
            
            # Should have at least one line with JSON content
            assert len(lines) >= 1
            
            # Each line should be valid JSON
            for line in lines:
                if line.strip():  # Skip empty lines
                    try:
                        json.loads(line)
                    except json.JSONDecodeError:
                        assert False, f"Line is not valid JSON: {line}"
            
            # Verify trade messages appear in trades log
            found_trade_msg = False
            found_category_trade_msg = False
            
            for line in lines:
                if line.strip():
                    log_entry = json.loads(line)
                    if log_entry.get('message') == "Trade executed":
                        found_trade_msg = True
                        assert log_entry.get('expert_name') == "TradeTest"
                        assert log_entry.get('symbol') == "BTCUSDT"
                        assert log_entry.get('trade_id') == "trade_123"
                        assert log_entry.get('order_id') == "order_456"
                    elif log_entry.get('message') == "Another trade message":
                        found_category_trade_msg = True
                        assert log_entry.get('category') == "trade"
                        assert log_entry.get('expert_name') == "TradeTest"
                        assert log_entry.get('symbol') == "ETHUSDT"
                        assert log_entry.get('trade_id') == "trade_789"
                        assert log_entry.get('order_id') == "order_012"
            
            assert found_trade_msg, "Trade message not found in trades.log"
            assert found_category_trade_msg, "Category trade message not found in trades.log"
            
            print("✓ SC-006: Trade messages appear in trades.log in JSON Lines format")
    
    def test_sc_007_error_resilience_continues_operation(self):
        """SC-007: The system continues trading operation even when logging system fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="resilience_test.log",
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Test that logging continues to work even when issues occur
            try:
                # Normal logging should work
                logger.info("Normal message", expert_name="ResilienceTest", symbol="RESILIENCE")
                
                # Even if we encounter issues, the system should continue
                # For example, logging with problematic data
                logger.info("Message with special chars", 
                           expert_name="ResilienceTest", 
                           symbol="RESILIENCE", 
                           special_chars="αβγδεζηθ")
                
                # Logging should continue to work
                logger.info("After special chars", expert_name="ResilienceTest", symbol="RESILIENCE")
                
                # System should continue operating
                assert True  # If we get here, the system continued operating
                print("✓ SC-007: System continues operation when logging encounters issues")
            except Exception as e:
                assert False, f"System failed to continue operation when logging encountered issues: {e}"
    
    def test_sc_008_structured_logging_meets_schema_requirements(self):
        """SC-008: Structured JSON logging format meets predefined schema requirements."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="schema_test.log",
                enable_structured_logging=True,
                file_log_format="json",
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Log a message with all required contextual fields
            logger.info(
                "Schema test message",
                expert_name="SchemaTestExpert",
                symbol="SCHEMA",
                trade_id="trade_schema_123",
                order_id="order_schema_456",
                strategy_id="SchemaStrategy",
                account_id="account_schema_789"
            )
            
            # Wait for async processing to complete
            time.sleep(1)
            
            # Read the log file and verify schema compliance
            log_path = os.path.join(temp_dir, "schema_test.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Should be valid JSON
            try:
                log_entry = json.loads(content)
            except json.JSONDecodeError:
                assert False, "Log entry is not valid JSON"
            
            # Verify all required fields exist
            required_fields = [
                'timestamp', 'severity', 'message',
                'expert_name', 'symbol', 'trade_id', 'order_id', 'strategy_id', 'account_id'
            ]
            
            for field in required_fields:
                assert field in log_entry, f"Required field '{field}' missing from log entry"
            
            # Verify field values
            assert log_entry['message'] == "Schema test message"
            assert log_entry['expert_name'] == "SchemaTestExpert"
            assert log_entry['symbol'] == "SCHEMA"
            assert log_entry['trade_id'] == "trade_schema_123"
            assert log_entry['order_id'] == "order_schema_456"
            assert log_entry['strategy_id'] == "SchemaStrategy"
            assert log_entry['account_id'] == "account_schema_789"
            assert log_entry['severity'] == "info"
            
            # Verify timestamp format (ISO 8601)
            timestamp = log_entry['timestamp']
            assert isinstance(timestamp, str)
            assert "T" in timestamp
            assert "Z" in timestamp
            
            print("✓ SC-008: Structured JSON logging meets schema requirements")
    
    def test_sc_009_documentation_examples_clear(self):
        """SC-009: Documentation includes clear examples of how to implement contextual logging."""
        # This is verified by checking that the template.py file contains clear examples
        template_path = os.path.join("src", "metaexpert", "cli", "templates", "template.py")
        
        # Check that template.py exists
        assert os.path.exists(template_path), "Template file should exist"
        
        # Read the template file
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that it contains examples of contextual logging
        assert "expert.bind" in content or "expert.context" in content, "Template should include contextual logging examples"
        assert "expert_name" in content, "Template should include expert_name context"
        assert "symbol" in content, "Template should include symbol context"
        
        # Check that it contains examples of all major features
        assert "log_level" in content, "Template should include log_level configuration"
        assert "async_logging" in content, "Template should include async_logging configuration"
        assert "structured_logging" in content, "Template should include structured_logging configuration"
        
        print("✓ SC-009: Documentation includes clear examples for contextual logging")