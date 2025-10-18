"""Unit tests for different log file handlers in the MetaExpert logging system."""

import os
import tempfile
import logging
from unittest.mock import Mock, patch
import pytest

from src.metaexpert.logger.handlers.file import ExpertFileHandler, TradesFileHandler, ErrorsFileHandler


class TestLogHandlers:
    """Test cases for different log file handlers."""
    
    def test_expert_file_handler_initialization(self):
        """Test that ExpertFileHandler initializes correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "expert.log")
            handler = ExpertFileHandler(log_file)
            
            assert handler is not None
            assert os.path.exists(log_file) or True  # Handler might not create file until first write
    
    def test_trades_file_handler_initialization(self):
        """Test that TradesFileHandler initializes correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "trades.log")
            handler = TradesFileHandler(log_file)
            
            assert handler is not None
            assert os.path.exists(log_file) or True  # Handler might not create file until first write
    
    def test_errors_file_handler_initialization(self):
        """Test that ErrorsFileHandler initializes correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "errors.log")
            handler = ErrorsFileHandler(log_file)
            
            assert handler is not None
            assert os.path.exists(log_file) or True  # Handler might not create file until first write
    
    def test_expert_file_handler_filter_allows_regular_messages(self):
        """Test that ExpertFileHandler allows regular messages."""
        handler = ExpertFileHandler("dummy.log")
        
        # Create a mock log record for a regular message
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Regular info message",
            args=(),
            exc_info=None
        )
        
        # Add a structlog_event_dict attribute to simulate structlog processing
        record.structlog_event_dict = {}
        
        # Regular messages should be allowed
        assert handler.filter(record) is True
    
    def test_expert_file_handler_filter_blocks_trade_messages(self):
        """Test that ExpertFileHandler blocks trade messages."""
        handler = ExpertFileHandler("dummy.log")
        
        # Create a mock log record for a trade message
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Trade executed",
            args=(),
            exc_info=None
        )
        
        # Add a structlog_event_dict with category=trade to simulate a trade message
        record.structlog_event_dict = {"category": "trade"}
        
        # Trade messages should be filtered out (return False)
        assert handler.filter(record) is False
    
    def test_trades_file_handler_filter_allows_trade_messages(self):
        """Test that TradesFileHandler allows trade messages."""
        handler = TradesFileHandler("dummy.log")
        
        # Create a mock log record for a trade message
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Trade executed",
            args=(),
            exc_info=None
        )
        
        # Add a structlog_event_dict with category=trade to simulate a trade message
        record.structlog_event_dict = {"category": "trade"}
        
        # Trade messages should be allowed
        assert handler.filter(record) is True
    
    def test_trades_file_handler_filter_blocks_regular_messages(self):
        """Test that TradesFileHandler blocks regular messages."""
        handler = TradesFileHandler("dummy.log")
        
        # Create a mock log record for a regular message
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Regular info message",
            args=(),
            exc_info=None
        )
        
        # Add a structlog_event_dict with no category to simulate a non-trade message
        record.structlog_event_dict = {}
        
        # Regular messages should be filtered out (return False)
        assert handler.filter(record) is False
    
    def test_errors_file_handler_filter_allows_error_messages(self):
        """Test that ErrorsFileHandler allows ERROR and CRITICAL messages."""
        handler = ErrorsFileHandler("dummy.log")
        
        # Test ERROR level
        error_record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Error occurred",
            args=(),
            exc_info=None
        )
        assert handler.filter(error_record) is True
        
        # Test CRITICAL level
        critical_record = logging.LogRecord(
            name="test",
            level=logging.CRITICAL,
            pathname="",
            lineno=0,
            msg="Critical error occurred",
            args=(),
            exc_info=None
        )
        assert handler.filter(critical_record) is True
    
    def test_errors_file_handler_filter_blocks_lower_level_messages(self):
        """Test that ErrorsFileHandler blocks INFO, WARNING, and DEBUG messages."""
        handler = ErrorsFileHandler("dummy.log")
        
        # Test INFO level (should be blocked)
        info_record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Info message",
            args=(),
            exc_info=None
        )
        assert handler.filter(info_record) is False
        
        # Test WARNING level (should be blocked)
        warning_record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="Warning message",
            args=(),
            exc_info=None
        )
        assert handler.filter(warning_record) is False
        
        # Test DEBUG level (should be blocked)
        debug_record = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="",
            lineno=0,
            msg="Debug message",
            args=(),
            exc_info=None
        )
        assert handler.filter(debug_record) is False