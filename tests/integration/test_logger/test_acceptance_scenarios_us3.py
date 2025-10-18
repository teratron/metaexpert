"""Acceptance tests for contextual and structured logging in the MetaExpert logging system."""

import json
import tempfile
import os

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestContextualStructuredAcceptance:
    """Acceptance tests for user story 3: Contextual and Structured Logging."""
    
    def test_contextual_information_included_in_log_entries(self):
        """Verify contextual information is included in log entries (acceptance scenario 1)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="context_acceptance.log",
                log_level="INFO",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log with all required contextual fields using context manager
            with logger.context(
                expert_name="AcceptanceTestExpert",
                symbol="BTCUSDT",
                trade_id="trade_acceptance_123",
                order_id="order_acceptance_456",
                strategy_id="AcceptanceTestStrategy",
                account_id="account_acceptance_789"
            ):
                logger.info("Acceptance test message with full context", 
                           additional_param="acceptance_value")
            
            # Verify that all context information appears in the log entry
            log_path = os.path.join(temp_dir, "context_acceptance.log")
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            parsed = json.loads(content)
            
            # Verify all required contextual fields are present
            assert parsed['expert_name'] == "AcceptanceTestExpert"
            assert parsed['symbol'] == "BTCUSDT"
            assert parsed['trade_id'] == "trade_acceptance_123"
            assert parsed['order_id'] == "order_acceptance_456"
            assert parsed['strategy_id'] == "AcceptanceTestStrategy"
            assert parsed['account_id'] == "account_acceptance_789"
            
            # Verify the log message is present
            assert parsed['message'] == "Acceptance test message with full context"
            
            # Verify the additional parameter is preserved
            assert parsed['additional_param'] == "acceptance_value"
            
            # Verify standard fields are present
            assert 'timestamp' in parsed
            assert parsed['severity'] == "info"
    
    def test_logs_formatted_as_json_objects(self):
        """Verify logs are formatted as JSON objects (acceptance scenario 2)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="json_acceptance.log",
                trades_log_file="json_trades_acceptance.log",
                errors_log_file="json_errors_acceptance.log",
                log_level="DEBUG",
                enable_structured_logging=True,
                file_log_format="json"
            )
            
            logger = MetaLogger(config=config)
            
            # Log various types of messages
            logger.info("Info message", expert_name="TestExpert", symbol="BTCUSDT")
            logger.trade("Trade executed", trade_id="trade_json_123", order_id="order_json_456")
            logger.error("Error occurred", error_code="JSON-ERR-001")
            
            # Check all log files to ensure they contain valid JSON
            log_files = [
                os.path.join(temp_dir, "json_acceptance.log"),
                os.path.join(temp_dir, "json_trades_acceptance.log"),
                os.path.join(temp_dir, "json_errors_acceptance.log")
            ]
            
            json_entries_count = 0
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if line:  # Skip empty lines
                            # Each line should be a valid JSON object
                            try:
                                parsed = json.loads(line)
                                # Verify it has the expected structure for our RFC 5424 compliance
                                assert 'timestamp' in parsed
                                assert 'severity' in parsed
                                assert 'message' in parsed
                                json_entries_count += 1
                            except json.JSONDecodeError:
                                assert False, f"Entry is not valid JSON: {line}"
            
            # We expect at least 3 entries (one for each log type)
            assert json_entries_count >= 3, f"Expected at least 3 JSON entries, found {json_entries_count}"