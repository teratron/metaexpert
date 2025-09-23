"""Structured log formatter for JSON-based logging."""

import json
import logging
import traceback
from typing import Any, Dict


class StructuredLogFormatter(logging.Formatter):
    """Formatter for structured logging with JSON output."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as structured JSON.

        Args:
            record: The log record to format

        Returns:
            Formatted log record as JSON string
        """
        try:
            # Create a dictionary with log record attributes
            log_entry = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "message": record.getMessage(),
            }

            # Add context data if present
            if hasattr(record, "context"):
                try:
                    log_entry["context"] = record.context
                except Exception as e:
                    log_entry["context_error"] = f"Failed to serialize context: {str(e)}"

            # Add exception information if present
            if record.exc_info:
                try:
                    log_entry["exception"] = self.formatException(record.exc_info)
                except Exception as e:
                    log_entry["exception_format_error"] = f"Failed to format exception: {str(e)}"

            # Add extra fields if present
            if hasattr(record, "__dict__"):
                try:
                    for key, value in record.__dict__.items():
                        # Skip internal attributes and the message (already added)
                        if not key.startswith("_") and key not in ["msg", "args", "levelname", "levelno", 
                                                                "pathname", "filename", "module", 
                                                                "lineno", "funcName", "created", 
                                                                "msecs", "relativeCreated", "thread", 
                                                                "threadName", "processName", "process", 
                                                                "getMessage", "exc_info", "exc_text", 
                                                                "stack_info", "context"]:
                            try:
                                # Try to serialize the value
                                json.dumps(value)  # This will raise if not serializable
                                log_entry[key] = value
                            except (TypeError, ValueError):
                                # If not JSON serializable, convert to string
                                log_entry[key] = str(value)
                except Exception as e:
                    log_entry["extra_fields_error"] = f"Failed to process extra fields: {str(e)}"

            # Convert to JSON string
            try:
                return json.dumps(log_entry, ensure_ascii=False, default=str)
            except (TypeError, ValueError) as json_error:
                # Fallback to simple string if JSON conversion fails
                fallback_message = f"[JSON_FORMAT_ERROR] {super().format(record)} - JSON Error: {str(json_error)}"
                return fallback_message
        except Exception as e:
            # Handle any other unexpected errors
            error_message = f"[UNEXPECTED_ERROR] Failed to format log record - Error: {str(e)}"
            try:
                # Try to provide some basic information
                basic_info = {
                    "timestamp": getattr(record, "asctime", "unknown"),
                    "level": getattr(record, "levelname", "UNKNOWN"),
                    "message": "Failed to format log record",
                    "error": str(e)
                }
                return json.dumps(basic_info, ensure_ascii=False)
            except:
                # Ultimate fallback
                return error_message


class KeyValueLogFormatter(logging.Formatter):
    """Formatter for key-value pair logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as key-value pairs.

        Args:
            record: The log record to format

        Returns:
            Formatted log record as key-value string
        """
        try:
            # Create a dictionary with log record attributes
            log_entry = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }

            # Add context data if present
            if hasattr(record, "context"):
                try:
                    log_entry.update(record.context)
                except Exception as e:
                    log_entry["context_error"] = f"Failed to add context: {str(e)}"

            # Add extra fields if present
            if hasattr(record, "__dict__"):
                try:
                    for key, value in record.__dict__.items():
                        # Skip internal attributes and the message (already added)
                        if not key.startswith("_") and key not in ["msg", "args", "levelname", "levelno", 
                                                                "pathname", "filename", "module", 
                                                                "lineno", "funcName", "created", 
                                                                "msecs", "relativeCreated", "thread", 
                                                                "threadName", "processName", "process", 
                                                                "getMessage", "exc_info", "exc_text", 
                                                                "stack_info", "context"]:
                            try:
                                log_entry[key] = value
                            except Exception as e:
                                log_entry[f"{key}_error"] = f"Failed to add field {key}: {str(e)}"
                except Exception as e:
                    log_entry["extra_fields_error"] = f"Failed to process extra fields: {str(e)}"

            # Format as key-value pairs
            try:
                formatted_entries = []
                for key, value in log_entry.items():
                    # Escape quotes in values
                    if isinstance(value, str):
                        escaped_value = value.replace('"', '\\"')
                        formatted_entries.append(f'{key}="{escaped_value}"')
                    else:
                        formatted_entries.append(f'{key}={value}')

                return " ".join(formatted_entries)
            except Exception as format_error:
                # Fallback if formatting fails
                return f"[KV_FORMAT_ERROR] {super().format(record)} - KV Error: {str(format_error)}"
                
        except Exception as e:
            # Handle any other unexpected errors
            error_message = f"[UNEXPECTED_ERROR] Failed to format log record - Error: {str(e)}"
            try:
                return f'timestamp="{getattr(record, "asctime", "unknown")}" level="{getattr(record, "levelname", "UNKNOWN")}" message="Failed to format log record" error="{str(e)}"'
            except:
                # Ultimate fallback
                return error_message