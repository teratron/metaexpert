"""Tests for MetaExpert logger processors."""

import logging
from unittest.mock import Mock

import pytest
from structlog import DropEvent

from metaexpert.logger2.processors import (
    add_app_context,
    add_process_info,
    filter_by_log_level,
    rename_event_key,
    TradeEventFilter,
    ErrorEventEnricher
)


def test_add_app_context():
    """Test the add_app_context processor."""
    logger = Mock(spec=logging.Logger)
    method_name = "info"
    event_dict = {"message": "test message"}
    
    # Call the processor
    result = add_app_context(logger, method_name, event_dict)
    
    # Check that app context is added
    assert result["app"] == "metaexpert"
    assert result["message"] == "test message"


def test_filter_by_log_level_below_threshold():
    """Test filter_by_log_level when event level is below logger level."""
    from structlog import DropEvent
    
    # Create a mock logger with WARNING level
    logger = Mock(spec=logging.Logger)
    logger.getEffectiveLevel.return_value = logging.WARNING
    method_name = "info"
    event_dict = {"level": "info", "message": "test message"}
    
    # Test that the processor raises DropEvent when level is too low
    with pytest.raises(DropEvent):
        filter_by_log_level(logger, method_name, event_dict)


def test_filter_by_log_level_above_threshold():
    """Test filter_by_log_level when event level is above or equal to logger level."""
    logger = Mock(spec=logging.Logger)
    logger.getEffectiveLevel.return_value = logging.WARNING
    method_name = "error"
    event_dict = {"level": "error", "message": "test message"}
    
    # Call the processor
    result = filter_by_log_level(logger, method_name, event_dict)
    
    # Since ERROR >= WARNING, the event should pass through
    assert result["level"] == "error"
    assert result["message"] == "test message"


def test_add_process_info():
    """Test the add_process_info processor."""
    logger = Mock(spec=logging.Logger)
    method_name = "info"
    event_dict = {"message": "test message"}
    
    # Call the processor
    result = add_process_info(logger, method_name, event_dict)
    
    # Check that process information is added
    assert "process_id" in result
    assert "thread_id" in result
    assert "thread_name" in result
    assert result["message"] == "test message"


def test_rename_event_key():
    """Test the rename_event_key processor."""
    logger = Mock(spec=logging.Logger)
    method_name = "info"
    event_dict = {"event": "test message", "level": "info"}
    
    # Call the processor
    result = rename_event_key(logger, method_name, event_dict)
    
    # Check that 'event' is renamed to 'message'
    assert "message" in result
    assert "event" not in result
    assert result["message"] == "test message"
    assert result["level"] == "info"
    
    # Test with no 'event' key
    event_dict_no_event = {"level": "info", "other": "value"}
    result_no_event = rename_event_key(logger, method_name, event_dict_no_event)
    assert result_no_event == event_dict_no_event


def test_trade_event_filter():
    """Test the TradeEventFilter processor."""
    filter_processor = TradeEventFilter()
    
    logger = Mock(spec=logging.Logger)
    method_name = "info"
    
    # Test with a trade event
    trade_event_dict = {"event_type": "trade", "symbol": "BTCUSDT", "side": "BUY"}
    result_trade = filter_processor(logger, method_name, trade_event_dict)
    
    # Check that _trade_event flag is added
    assert result_trade["_trade_event"] is True
    assert result_trade["event_type"] == "trade"
    assert result_trade["symbol"] == "BTCUSDT"
    assert result_trade["side"] == "BUY"
    
    # Test with a non-trade event
    non_trade_event_dict = {"event_type": "info", "message": "regular message"}
    result_non_trade = filter_processor(logger, method_name, non_trade_event_dict)
    
    # Check that _trade_event flag is not added
    assert "_trade_event" not in result_non_trade
    assert result_non_trade["event_type"] == "info"
    assert result_non_trade["message"] == "regular message"


def test_error_event_enricher_with_error():
    """Test the ErrorEventEnricher processor with an error event."""
    enricher = ErrorEventEnricher()
    
    logger = Mock(spec=logging.Logger)
    method_name = "error"
    
    # Create an exception instance
    test_exception = ValueError("Test error message")
    
    # Test with an error event containing an exception
    error_event_dict = {
        "level": "error",
        "message": "An error occurred",
        "exception": test_exception
    }
    result = enricher(logger, method_name, error_event_dict)
    
    # Check that error-specific metadata is added
    assert result["error_type"] == "ValueError"
    assert result["error_module"] == "builtins"
    assert result["level"] == "error"
    assert result["message"] == "An error occurred"
    assert result["exception"] is test_exception


def test_error_event_enricher_with_non_error():
    """Test the ErrorEventEnricher processor with a non-error event."""
    enricher = ErrorEventEnricher()
    
    logger = Mock(spec=logging.Logger)
    method_name = "info"
    
    # Test with a non-error event
    info_event_dict = {
        "level": "info",
        "message": "Regular info message"
    }
    result = enricher(logger, method_name, info_event_dict)
    
    # Check that no error-specific metadata is added
    assert "error_type" not in result
    assert "error_module" not in result
    assert result["level"] == "info"
    assert result["message"] == "Regular info message"


def test_error_event_enricher_with_critical():
    """Test the ErrorEventEnricher processor with a critical event."""
    enricher = ErrorEventEnricher()
    
    logger = Mock(spec=logging.Logger)
    method_name = "critical"
    
    # Create an exception instance
    test_exception = RuntimeError("Critical error")
    
    # Test with a critical event containing an exception
    critical_event_dict = {
        "level": "critical",
        "message": "A critical error occurred",
        "exception": test_exception
    }
    result = enricher(logger, method_name, critical_event_dict)
    
    # Check that error-specific metadata is added
    assert result["error_type"] == "RuntimeError"
    assert result["error_module"] == "builtins"
    assert result["level"] == "critical"
    assert result["message"] == "A critical error occurred"
    assert result["exception"] is test_exception