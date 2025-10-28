"""Custom structlog processors for MetaExpert."""

import logging
from typing import Any


def add_app_context(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add application-specific context to log entries."""
    event_dict["app"] = "metaexpert"
    return event_dict


def filter_by_log_level(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Filter events based on logger's effective level."""
    log_level = event_dict.get("level")
    if log_level is None:
        return event_dict

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    if numeric_level < logger.getEffectiveLevel():
        # Skip logging if below logger's effective level
        from structlog import DropEvent
        raise DropEvent

    return event_dict


def add_process_info(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add process and thread information."""
    import os
    import threading

    event_dict["process_id"] = os.getpid()
    event_dict["thread_id"] = threading.get_ident()
    event_dict["thread_name"] = threading.current_thread().name

    return event_dict


def rename_event_key(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Rename 'event' to 'message' for better readability."""
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")

    return event_dict


class TradeEventFilter:
    """Filter to route trade events to specialized logger."""

    def __call__(
        self, logger: Any, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Mark trade-related events.

        Processor is called BEFORE ProcessorFormatter.wrap_for_formatter,
        so we need to set a marker in event_dict that will then
        be passed to _record via wrap_for_formatter.
        """
        # Check if this is a trade event
        if event_dict.get("event_type") == "trade":
            event_dict["_trade_event"] = True

            # FIX: Also set in _record if it exists
            # This is needed for ProcessorFormatter
            _record = event_dict.get("_record")
            if _record:
                _record._trade_event = True

        return event_dict


class ErrorEventEnricher:
    """Enrich error events with additional context."""

    def __call__(
        self, logger: Any, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Add extra context to error events."""
        level = event_dict.get("level")

        if level in ("error", "critical"):
            # Add error-specific metadata
            if "exception" in event_dict:
                exc = event_dict["exception"]
                event_dict["error_type"] = type(exc).__name__
                event_dict["error_module"] = type(exc).__module__

            # контекст для отладки
            if event_dict.get("exc_info"):
                import traceback

                exc_info = event_dict["exc_info"]
                if isinstance(exc_info, tuple) and len(exc_info) == 3:
                    _exc_type, _exc_value, exc_tb = exc_info
                    if exc_tb:
                        # Добавляем место возникновения ошибки
                        tb_summary = traceback.extract_tb(exc_tb)
                        if tb_summary:
                            last_frame = tb_summary[-1]
                            event_dict["error_location"] = (
                                f"{last_frame.filename}:{last_frame.lineno}"
                            )
                            event_dict["error_function"] = last_frame.name

        return event_dict


class PerformanceMonitor:
    """Performance monitor for trade operations."""

    def __init__(self, threshold_ms: float = 100.0):
        """

        Args:
            threshold_ms: Threshold in milliseconds for warning
        """
        self.threshold_ms = threshold_ms
        self._timers: dict[str, float] = {}

    def __call__(
        self, logger: Any, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Add performance metrics for trade events."""

        # Only for trade events
        if event_dict.get("event_type") != "trade":
            return event_dict

        # If duration exists, check threshold
        duration_ms = event_dict.get("duration_ms")
        if duration_ms is not None and duration_ms > self.threshold_ms:
            event_dict["_slow_operation"] = True
            event_dict["performance_warning"] = f"Operation took {duration_ms:.2f}ms"

        return event_dict


class SensitiveDataFilter:
    """Filter for masking sensitive data."""

    SENSITIVE_KEYS = {
        "password",
        "token",
        "api_key",
        "secret",
        "private_key",
        "apikey",
        "api_secret",
        "access_token",
        "refresh_token",
    }

    def __call__(
        self, logger: Any, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Mask sensitive data in logs."""
        for key in list(event_dict.keys()):
            if any(sensitive in key.lower() for sensitive in self.SENSITIVE_KEYS):
                value = event_dict[key]
                if isinstance(value, str) and len(value) > 4:
                    # Show only last 4 characters
                    event_dict[key] = f"***{value[-4:]}"
                else:
                    event_dict[key] = "***"

        return event_dict
