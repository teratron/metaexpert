"""MetaExpert structured logging system.

This module provides a production-ready logging system built on structlog,
offering structured logging, context management, and specialized handlers.

Quick Start:
    >>> from metaexpert.logger import setup_logging, get_logger, LoggerConfig
    >>>
    >>> # Initialize logging system
    >>> config = LoggerConfig(log_level="INFO")
    >>> setup_logging(config)
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
    >>> from metaexpert.logger import get_trade_logger, trade_context
    >>>
    >>> trade_logger = get_trade_logger(strategy_id=1001)
    >>> with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    >>>     trade_logger.info("trade executed", price=50000)
"""

import structlog

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
from metaexpert.logger.setup import setup_logging

# Type alias for convenience
BoundLogger = structlog.stdlib.BoundLogger

__all__ = [
    "BoundLogger",
    "LogContext",
    "LoggerConfig",
    "TradeContext",
    "bind_contextvars",
    "clear_contextvars",
    "get_logger",
    "get_trade_logger",
    "iterate_with_context",
    "setup_logging",
    "unbind_contextvars",
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
