import json
import logging
import sys

import pytest

from metaexpert.logger.structured_log_formatter import StructuredLogFormatter


@pytest.fixture
def formatter() -> StructuredLogFormatter:
    return StructuredLogFormatter()


@pytest.fixture
def log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="/test/path.py",
        lineno=42,
        msg="This is a test message",
        args=(),
        exc_info=None,
        func="test_func",
    )


def test_format_is_valid_json(formatter: StructuredLogFormatter, log_record: logging.LogRecord):
    """Test that the formatted output is a valid JSON string."""
    formatted_log = formatter.format(log_record)
    try:
        json.loads(formatted_log)
    except json.JSONDecodeError:
        pytest.fail("Formatter did not produce valid JSON.")


def test_formatted_json_contains_required_fields(formatter: StructuredLogFormatter, log_record: logging.LogRecord):
    """Test that the formatted JSON contains all the required fields."""
    formatted_log = formatter.format(log_record)
    log_json = json.loads(formatted_log)

    expected_keys = ["timestamp", "level", "logger", "function", "line", "message"]
    for key in expected_keys:
        assert key in log_json

    assert log_json["level"] == "INFO"
    assert log_json["message"] == "This is a test message"
    assert log_json["logger"] == "test_logger"


def test_format_with_exception(formatter: StructuredLogFormatter):
    """Test that exception information is included in the formatted log."""
    try:
        raise ValueError("Test exception")
    except ValueError:
        exc_info = sys.exc_info()
        record = logging.LogRecord(
            name="test_exc_logger",
            level=logging.ERROR,
            pathname="/exc/path.py",
            lineno=99,
            msg="An error occurred",
            args=(),
            exc_info=exc_info,
        )
        formatted_log = formatter.format(record)
        log_json = json.loads(formatted_log)

        assert "exception" in log_json
        assert "ValueError: Test exception" in log_json["exception"]