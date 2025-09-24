"""Structured log formatter for JSON-based logging."""

import json
from logging import Formatter, LogRecord
from typing import Any


class LogFormatter(Formatter):
    """Formatter for structured logging with JSON output."""

    def format(self, record: LogRecord) -> str:
        """Format a log record as structured JSON.

        Args:
            record: The log record to format

        Returns:
            Formatted log record as JSON string
        """
        # Create a dictionary with log record attributes
        log_entry: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Convert to JSON string
        return json.dumps(log_entry, ensure_ascii=False, default=str)
