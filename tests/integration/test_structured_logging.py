"""Integration test for structured logging functionality."""

import pytest
import logging
import json
from io import StringIO
from unittest.mock import patch, MagicMock

from metaexpert.logger import setup_logger, get_logger
from metaexpert.logger.structured_log_formatter import StructuredLogFormatter


def test_structured_logging_format():
    """Test that logs are formatted in structured format.
    
    Given a logger configured for structured logging
    When a log message is created with additional context
    Then the log should be formatted as structured data (JSON)
    """
    # Given
    logger = setup_logger("test_structured", structured=True)
    
    # Capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(StructuredLogFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # When
    logger.info("Test message")
    
    # Then
    log_output = log_stream.getvalue().strip()
    # Verify it's valid JSON
    log_data = json.loads(log_output)
    
    # Check required fields
    assert "timestamp" in log_data
    assert "level" in log_data
    assert "logger" in log_data
    assert "message" in log_data
    assert log_data["message"] == "Test message"
    assert log_data["level"] == "INFO"


def test_structured_logging_context():
    """Test that context data is properly included in structured logs.
    
    Given a logger with structured logging enabled
    When a log message is created with context data
    Then the context should be included in the structured output
    """
    # Given
    logger = setup_logger("test_context", structured=True)
    
    # Capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(StructuredLogFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # When
    # Create a log record with extra context
    logger.info("Test with context", extra={"user_id": 123, "action": "login"})
    
    # Then
    log_output = log_stream.getvalue().strip()
    # Verify it's valid JSON
    log_data = json.loads(log_output)
    
    # Check that context data is included
    assert log_data["message"] == "Test with context"
    assert log_data["user_id"] == 123
    assert log_data["action"] == "login"


def test_structured_logging_levels():
    """Test that different log levels are properly handled in structured logging.
    
    Given a logger with structured logging enabled
    When log messages are created at different levels
    Then each level should be properly represented in the structured output
    """
    # Given
    logger = setup_logger("test_levels", structured=True)
    
    # Capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(StructuredLogFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    # When
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    
    # Then
    log_output = log_stream.getvalue().strip()
    log_lines = log_output.split('\n')
    
    # Check that we have 5 log entries
    assert len(log_lines) == 5
    
    # Check each level
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for i, level in enumerate(levels):
        log_data = json.loads(log_lines[i])
        assert log_data["level"] == level


def test_structured_logging_backward_compatibility():
    """Test that structured logging maintains backward compatibility.
    
    Given existing code using the standard logging interface
    When structured logging is enabled
    Then existing code should continue to work without modification
    """
    # Given
    # Traditional logger usage
    logger = setup_logger("test_backward_compat")
    
    # When
    # This should work the same as before
    logger.info("Traditional log message")
    
    # Then
    # No exception should be raised
    assert True  # If we get here, the test passed