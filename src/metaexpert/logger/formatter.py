"""Enhanced structured log formatter for JSON-based logging with structlog compatibility."""

import json
import logging
import traceback
from datetime import datetime
from typing import Any


class MainFormatter(logging.Formatter):
    """Enhanced formatter for structured logging with JSON output that integrates with structlog."""

    def __init__(self, include_extra: bool = True, timestamp_format: str = "iso"):
        """Initialize the structured formatter.

        Args:
            include_extra: Whether to include extra fields from log record
            timestamp_format: Format for timestamps ('iso', 'epoch', 'custom')
        """
        super().__init__()
        self.include_extra = include_extra
        self.timestamp_format = timestamp_format

        # Standard log record attributes to exclude from extra fields
        self.reserved_attrs = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "getMessage",
            "message",
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as structured JSON.

        Args:
            record: The log record to format

        Returns:
            Formatted log record as JSON string
        """
        # Check if the record has structlog-specific fields
        if hasattr(record, '__dict__') and '_record' in record.__dict__:
            # This is a structlog record wrapped by stdlib logger
            return self._format_structlog_record(record)
        else:
            # This is a regular stdlib logging record
            log_entry = self._get_log_entry(record)
            return json.dumps(log_entry, ensure_ascii=False, default=self._json_serializer)

    def _format_structlog_record(self, record: logging.LogRecord) -> str:
        """Format a structlog record that was passed to a stdlib handler.

        Args:
            record: The structlog record to format

        Returns:
            Formatted log record as JSON string
        """
        # Extract the original structlog event dict from the formatted message
        # This is a simplified approach - in practice, the integration between
        # structlog and stdlib logging handlers is more complex
        log_entry: dict[str, Any] = {
            "timestamp": self._format_timestamp(record.created),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),  # Use the message as the event
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add any extra fields
        for key, value in record.__dict__.items():
            if key not in self.reserved_attrs:
                log_entry[key] = value

        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self._format_exception(record.exc_info),
            }

        return json.dumps(log_entry, ensure_ascii=False, default=self._json_serializer)

    def _get_log_entry(self, record: logging.LogRecord) -> dict[str, Any]:
        """Create base log entry dictionary.

        Args:
            record: The log record to format

        Returns:
            Log entry dictionary
        """
        # Create base log entry
        log_entry: dict[str, Any] = {
            "timestamp": self._format_timestamp(record.created),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add thread information if available
        if hasattr(record, "thread") and record.thread:
            log_entry["thread"] = {
                "id": record.thread,
                "name": getattr(record, "threadName", "Unknown"),
            }

        # Add process information if available
        if hasattr(record, "process") and record.process:
            log_entry["process"] = {
                "id": record.process,
                "name": getattr(record, "processName", "Unknown"),
            }

        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self._format_exception(record.exc_info),
            }

        # Add stack info if present
        if record.stack_info:
            log_entry["stack_info"] = record.stack_info

        # Add extra fields if enabled
        if self.include_extra:
            extra_fields = self._extract_extra_fields(record)
            if extra_fields:
                log_entry.update(extra_fields)  # For structlog compatibility, add fields at top level

        return log_entry

    def _format_timestamp(self, created: float) -> str:
        """Format timestamp according to configuration.

        Args:
            created: Timestamp from log record

        Returns:
            Formatted timestamp string
        """
        if self.timestamp_format == "epoch":
            return str(created)
        elif self.timestamp_format == "iso":
            return datetime.fromtimestamp(created).isoformat()
        else:
            # Custom format using standard formatTime
            dt = datetime.fromtimestamp(created)
            return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _format_exception(exc_info) -> str:
        """Format exception information.

        Args:
            exc_info: Exception info tuple (exc_type, exc_value, exc_traceback)

        Returns:
            Formatted exception traceback
        """
        try:
            if exc_info and len(exc_info) >= 3:
                return "".join(
                    traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])
                ).strip()
            else:
                return "Invalid exception info"
        except (TypeError, ValueError):
            return "Failed to format exception"

    def _extract_extra_fields(self, record: logging.LogRecord) -> dict[str, Any]:
        """Extract extra fields from log record.

        Args:
            record: Log record to extract from

        Returns:
            Dictionary of extra fields
        """
        extra = {}
        for key, value in record.__dict__.items():
            if key not in self.reserved_attrs:
                extra[key] = value
        return extra

    @staticmethod
    def _json_serializer(obj: Any) -> str:
        """Custom JSON serializer for non-standard types.

        Args:
            obj: Object to serialize

        Returns:
            String representation of object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__dict__"):
            return str(obj)
        else:
            return repr(obj)


class TradeFormatter(MainFormatter):
    """Specialized formatter for trade-related logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format trade log record with additional trade-specific fields."""
        # Get base log entry
        base_entry = self._get_log_entry(record)

        # Add trade-specific metadata
        base_entry["log_type"] = "trade"

        # Extract trade-specific fields if present
        trade_fields = {}
        for field in ["symbol", "side", "quantity", "price", "order_id", "strategy_id"]:
            if hasattr(record, field):
                trade_fields[field] = getattr(record, field)

        if trade_fields:
            base_entry.update(trade_fields)  # Add trade fields at the top level for structlog compatibility

        return json.dumps(base_entry, ensure_ascii=False, default=self._json_serializer)


class ErrorFormatter(MainFormatter):
    """Specialized formatter for error logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format error log record with additional error-specific fields."""
        # Get base log entry
        base_entry = self._get_log_entry(record)

        # Add error-specific metadata
        base_entry["log_type"] = "error"
        base_entry["severity"] = self._get_error_severity(record.levelno)

        # Add error context if available
        error_context = {}
        for field in ["error_code", "component", "operation", "user_id", "session_id"]:
            if hasattr(record, field):
                error_context[field] = getattr(record, field)

        if error_context:
            base_entry.update(error_context)  # Add error context at the top level for structlog compatibility

        return json.dumps(base_entry, ensure_ascii=False, default=self._json_serializer)

    @staticmethod
    def _get_error_severity(levelno: int) -> str:
        """Get error severity based on log level.

        Args:
            levelno: Numeric log level

        Returns:
            Error severity string
        """
        if levelno >= logging.CRITICAL:
            return "critical"
        elif levelno >= logging.ERROR:
            return "high"
        elif levelno >= logging.WARNING:
            return "medium"
        else:
            return "low"
