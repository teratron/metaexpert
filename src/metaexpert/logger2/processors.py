"""Custom structlog processors for MetaExpert."""

import logging
from typing import Any

import structlog


def add_app_context(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add application-specific context to log entries."""
    event_dict["app"] = "metaexpert"
    return event_dict


def filter_by_log_level(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Filter events based on logger's effective level."""
    log_level = event_dict.get("level")
    if log_level is None:
        return event_dict

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    if numeric_level < logger.getEffectiveLevel():
        raise structlog.DropEvent

    return event_dict


def add_process_info(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add process and thread information."""
    import os
    import threading

    event_dict["process_id"] = os.getpid()
    event_dict["thread_id"] = threading.get_ident()
    event_dict["thread_name"] = threading.current_thread().name

    return event_dict


def rename_event_key(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Rename 'event' to 'message' for better readability."""
    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")
    return event_dict


class TradeEventFilter:
    """Filter to route trade events to specialized logger."""

    def __call__(
        self, logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Mark trade-related events."""
        # Check if this is a trade event
        if event_dict.get("event_type") == "trade":
            event_dict["_trade_event"] = True
        return event_dict


class ErrorEventEnricher:
    """Enrich error events with additional context."""

    def __call__(
        self, logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Add extra context to error events."""
        if event_dict.get("level") in ("error", "critical"):
            # Add error-specific metadata
            if "exception" in event_dict:
                exc = event_dict["exception"]
                event_dict["error_type"] = type(exc).__name__
                event_dict["error_module"] = type(exc).__module__

        return event_dict
