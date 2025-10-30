"""MetaExpert structured logging system.

This module provides a production-ready logging system built on structlog,
offering structured logging, context management, and specialized handlers.

Quick Start:
    >>> from metaexpert.logger import setup_logging, get_logger, LoggerConfig
    >>>
    >>> # Initialize logging system
    >>> config = LoggerConfig(log_level="INFO")
    >>> result = setup_logging(config)
    >>> print(result.to_string())
    >>>
    >>> # Get logger
    >>> logger = get_logger(__name__)
    >>> logger.info("application started")
    >>>
    >>> # With context
    >>> logger = logger.bind(symbol="BTCUSDT", exchange="binance")
    >>> logger.info("processing trade", price=50000)

Context Management:
    >>> from metaexpert.logger import LogContext, get_logger
    >>>
    >>> logger = get_logger(__name__)
    >>> with LogContext(strategy_id=1001, symbol="ETHUSDT"):
    >>>     logger.info("executing strategy")
    >>>     # All logs in this block will include strategy_id and symbol

Trade Logging:
    >>> from metaexpert.logger import get_trade_logger, TradeContext
    >>>
    >>> trade_logger = get_trade_logger(strategy_id=1001)
    >>> with TradeContext(symbol="BTCUSDT", side="BUY", quantity=0.01):
    >>>     trade_logger.info("trade executed", price=50000)

Metrics and Monitoring:
    >>> from metaexpert.logger import get_metrics, validate_log_event
    >>>
    >>> # Get logging metrics
    >>> metrics = get_metrics()
    >>> print(metrics.get_summary())
    >>>
    >>> # Validate log events
    >>> event = {"event_type": "trade", "symbol": "BTCUSDT", "side": "BUY", "quantity": 0.01}
    >>> is_valid, errors = validate_log_event(event)
"""

import structlog

from metaexpert.config import LOG_LEVEL_TYPE
from metaexpert.logger.config import LoggerConfig
from metaexpert.logger.context import (
    LogContext,
    TradeContext,
    bind_contextvars,
    clear_contextvars,
    get_logger,
    get_trade_logger,
    iterate_with_context,
    unbind_contextvars,
)
from metaexpert.logger.metrics import get_metrics, reset_metrics
from metaexpert.logger.results import LoggingSetupResult
from metaexpert.logger.setup import setup_logging
from metaexpert.logger.validators import sanitize_log_event, validate_log_event

# Type alias for convenience
BoundLogger = structlog.stdlib.BoundLogger

__all__ = [
    "BoundLogger",
    "LogContext",
    "LoggerConfig",
    "LoggingSetupResult",
    "MetaLogger",
    "TradeContext",
    "bind_contextvars",
    "clear_contextvars",
    "get_logger",
    "get_metrics",
    "get_trade_logger",
    "iterate_with_context",
    "reset_metrics",
    "sanitize_log_event",
    "setup_logging",
    "unbind_contextvars",
    "validate_log_event",
]

# Module-level logger for initialization
_logger = structlog.get_logger(__name__)


def _initialize_logging() -> None:
    """Initialize logging with defaults if not already configured."""
    if not structlog.is_configured():
        _logger.warning(
            "Logging not configured, using defaults. "
            "Call setup_logging() explicitly for production use."
        )
        setup_logging(LoggerConfig())


# Auto-initialize with defaults if imported
_initialize_logging()


class MetaLogger:
    @classmethod
    def create(
        cls,
        log_name: str,
        log_level: LOG_LEVEL_TYPE,
        log_file: str,
        log_trade_file: str,
        log_error_file: str,
        log_to_file: bool,
        log_to_console: bool,
        json_logging: bool,
    ) -> BoundLogger:
        """Create a new MetaLogger instance."""
        config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            log_trade_file=log_trade_file,
            log_error_file=log_error_file,
            log_to_file=log_to_file,
            log_to_console=log_to_console,
            json_logging=json_logging,
        )
        # Setup logging with the new config. This affects global state.
        setup_logging(config)

        return get_logger(log_name)
