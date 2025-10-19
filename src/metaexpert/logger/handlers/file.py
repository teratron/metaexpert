"""Specialized file handlers for the MetaExpert logging system.

This module contains specialized handlers that route log messages
to the appropriate files based on log level and content.
"""

import logging
from logging.handlers import RotatingFileHandler


class ExpertFileHandler(RotatingFileHandler):
    """File handler for expert.log - captures most log messages."""

    def __init__(self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, **kwargs):
        super().__init__(
            filename, maxBytes=max_bytes, backupCount=backup_count, **kwargs
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Expert log captures all messages except those specifically
        designated for trades or errors logs.
        """
        # Check if this is a trade-specific message (has 'category' field set to 'trade')
        if hasattr(record, "structlog_event_dict"):
            # If structlog_event_dict exists, check for trade category
            # Check for trade category in a safer way
            if (
                hasattr(record, "__dict__")
                and "category" in record.__dict__
                and record.__dict__.get("category") == "trade"
            ):
                return False  # Don't log trade messages to expert.log
        elif (
            hasattr(record, "__dict__")
            and "trade" in getattr(record, "getMessage", lambda: "")().lower()
        ):
            # Fallback: if it's a trade-related message, don't log to expert.log
            return False

        return True  # Log everything else to expert.log


class TradesFileHandler(RotatingFileHandler):
    """File handler for trades.log - captures only trade-related messages."""

    def __init__(self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, **kwargs):
        super().__init__(
            filename, maxBytes=max_bytes, backupCount=backup_count, **kwargs
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Trades log captures only messages specifically related to trades.
        """
        # Check if this is a trade-specific message (has 'category' field set to 'trade')
        # Check for trade category in the record's extra attributes
        if (
            hasattr(record, "__dict__")
            and "category" in record.__dict__
            and record.__dict__.get("category") == "trade"
        ):
            return True

        # Also check if the logger name is related to trading
        if hasattr(record, "name") and "trade" in record.name.lower():
            return True

        # Check if message contains trade-related terms
        if hasattr(record, "getMessage"):
            msg = record.getMessage().lower()
            if any(
                term in msg for term in ["trade", "order", "buy", "sell", "transaction"]
            ):
                return True

        return False


class ErrorsFileHandler(RotatingFileHandler):
    """File handler for errors.log - captures only error and critical messages."""

    def __init__(self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, **kwargs):
        super().__init__(
            filename, maxBytes=max_bytes, backupCount=backup_count, **kwargs
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Errors log captures only ERROR and CRITICAL level messages.
        """
        # Only log ERROR and CRITICAL level messages
        return record.levelno >= logging.ERROR
