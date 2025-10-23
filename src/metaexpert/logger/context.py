"""Context managers and utilities for MetaExpert logger."""

from collections.abc import Iterator
from contextvars import ContextVar
from typing import Any

import structlog

# Context variables for request-scoped data
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
trade_session_var: ContextVar[str | None] = ContextVar("trade_session", default=None)
strategy_id_var: ContextVar[int | None] = ContextVar("strategy_id", default=None)


def bind_contextvars(**kwargs: Any) -> None:
    """Bind context variables for current execution context.

    Example:
        bind_contextvars(request_id="abc123", strategy_id=1001)
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_contextvars(*keys: str) -> None:
    """Unbind specific context variables.

    Example:
        unbind_contextvars("request_id", "strategy_id")
    """
    structlog.contextvars.unbind_contextvars(*keys)


def clear_contextvars() -> None:
    """Clear all context variables."""
    structlog.contextvars.clear_contextvars()


class LogContext:
    """Context manager for temporary log context.

    Example:
        with LogContext(symbol="BTCUSDT", exchange="binance"):
            logger.info("processing trade")
            # Logs will include symbol and exchange
    """

    def __init__(self, **kwargs: Any):
        self.context = kwargs
        self.bound_keys: list[str] = []

    def __enter__(self) -> None:
        """Bind context variables on enter."""
        bind_contextvars(**self.context)
        self.bound_keys = list(self.context.keys())

    def __exit__(self, *args: Any) -> None:
        """Unbind context variables on exit."""
        unbind_contextvars(*self.bound_keys)


class TradeContext:
    """Context manager for trade execution logging.

    Example:
        with TradeContext(symbol="BTCUSDT", side="BUY", quantity=0.01):
            logger.info("executing trade", price=50000)
            # Automatic trade event logging
    """

    def __init__(self, symbol: str, side: str, quantity: float, **extra: Any):
        self.context = {
            "event_type": "trade",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            **extra,
        }

    def __enter__(self) -> None:
        """Bind trade context."""
        bind_contextvars(**self.context)

    def __exit__(self, *args: Any) -> None:
        """Clear trade context."""
        unbind_contextvars(*self.context.keys())


def get_logger(
    name: str | None = None, **initial_values: Any
) -> structlog.stdlib.BoundLogger:
    """Get a logger instance with optional initial context.

    Args:
        name: Logger name (typically module name)
        **initial_values: Initial context to bind

    Returns:
        Configured BoundLogger instance

    Example:
        logger = get_logger(__name__, exchange="binance")
        logger.info("connected to exchange")
    """
    logger = structlog.get_logger(name)

    if initial_values:
        logger = logger.bind(**initial_values)

    return logger


def get_trade_logger(**initial_values: Any) -> structlog.stdlib.BoundLogger:
    """Get logger specialized for trade events.

    Args:
        **initial_values: Initial context (e.g., symbol, strategy_id)

    Returns:
        BoundLogger configured for trades

    Example:
        trade_logger = get_trade_logger(symbol="BTCUSDT", strategy_id=1001)
        trade_logger.info("trade executed", side="BUY", price=50000)
    """
    return get_logger("trade", event_type="trade", **initial_values)


def iterate_with_context(items: list[Any], **context: Any) -> Iterator[Any]:
    """Iterate with context binding for each item.

    Example:
        for symbol in iterate_with_context(symbols, strategy_id=1001):
            logger.info("processing", symbol=symbol)
    """
    for item in items:
        with LogContext(**context):
            yield item
