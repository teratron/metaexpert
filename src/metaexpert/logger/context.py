"""Context managers and utilities for MetaExpert logger."""

import time
from collections.abc import Iterator
from contextvars import ContextVar
from typing import Any, Self

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

    # Также сохраняем в typed context vars для type-safe доступа
    if "request_id" in kwargs:
        request_id_var.set(kwargs["request_id"])
    if "trade_session" in kwargs:
        trade_session_var.set(kwargs["trade_session"])
    if "strategy_id" in kwargs:
        strategy_id_var.set(kwargs["strategy_id"])


def unbind_contextvars(*keys: str) -> None:
    """Unbind specific context variables.

    Example:
        unbind_contextvars("request_id", "strategy_id")
    """
    structlog.contextvars.unbind_contextvars(*keys)

    # Очищаем typed context vars
    for key in keys:
        if key == "request_id":
            request_id_var.set(None)
        elif key == "trade_session":
            trade_session_var.set(None)
        elif key == "strategy_id":
            strategy_id_var.set(None)


def clear_contextvars() -> None:
    """Clear all context variables."""
    structlog.contextvars.clear_contextvars()

    # Очищаем typed context vars
    request_id_var.set(None)
    trade_session_var.set(None)
    strategy_id_var.set(None)


def get_current_context() -> dict[str, Any]:
    """Получить текущий контекст логирования.

    Returns:
        Dict с текущими context variables

    Example:
        context = get_current_context()
        print(context.get("strategy_id"))
    """
    return {
        "request_id": request_id_var.get(),
        "trade_session": trade_session_var.get(),
        "strategy_id": strategy_id_var.get(),
    }


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

    def __enter__(self) -> Self:
        """Bind context variables on enter."""
        bind_contextvars(**self.context)
        self.bound_keys = list(self.context.keys())
        return self

    def __exit__(self, *args: Any) -> None:
        """Unbind context variables on exit."""
        unbind_contextvars(*self.bound_keys)


class TradeContext:
    """Context manager for trade execution logging.

    Example:
        with TradeContext(symbol="BTCUSDT", side="BUY", quantity=0.01) as ctx:
            logger.info("executing trade", price=50000)
            ctx.set_result(success=True, filled=0.01)
    """

    def __init__(self, symbol: str, side: str, quantity: float, **extra: Any):
        self.context = {
            "event_type": "trade",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            **extra,
        }
        self.start_time: float | None = None
        self.logger = get_trade_logger(**self.context)

    def __enter__(self) -> Self:
        """Bind trade context."""
        self.start_time = time.perf_counter()
        bind_contextvars(**self.context)
        self.logger.debug("trade_started")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Clear trade context."""
        duration_ms = (
            (time.perf_counter() - self.start_time) * 1000 if self.start_time else None
        )

        if exc_type is None:
            # Успешное выполнение
            self.logger.info("trade_completed", duration_ms=duration_ms, success=True)
        else:
            # Ошибка
            self.logger.error(
                "trade_failed",
                duration_ms=duration_ms,
                success=False,
                error=str(exc_val),
                exc_info=(exc_type, exc_val, exc_tb),
            )

        unbind_contextvars(*self.context.keys())

    def set_result(self, **result: Any) -> None:
        """Установить результат trade операции.

        Example:
            ctx.set_result(filled=0.01, avg_price=50123.45)
        """
        self.logger.info("trade_result", **result)

    def add_note(self, message: str, **extra: Any) -> None:
        """Добавить промежуточную заметку.

        Example:
            ctx.add_note("order submitted", order_id="12345")
        """
        self.logger.debug("trade_note", note=message, **extra)


def get_logger(name: str | None = None, **initial_values: Any) -> Any:
    """Get a logger instance with optional initial context.

    Args:
        name: Logger name (typically module name)
        **initial_values: Initial context to bind

    Returns:
        Configured logger instance

    Example:
        logger = get_logger(__name__, exchange="binance")
        logger.info("connected to exchange")
    """
    logger = structlog.stdlib.get_logger(name)

    if initial_values:
        logger = logger.bind(**initial_values)

    return logger


def get_trade_logger(**initial_values: Any) -> Any:
    """Get logger specialized for trade events.

    Args:
        **initial_values: Initial context (e.g., symbol, strategy_id)

    Returns:
        Logger configured for trades

    Example:
        trade_logger = get_trade_logger(symbol="BTCUSDT", strategy_id=101)
        trade_logger.info("trade executed", side="BUY", price=5000)
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


class TimedOperation:
    """Context manager для измерения времени операций.

    Example:
        logger = get_logger(__name__)
        with TimedOperation(logger, "fetch_data", threshold_ms=1000):
            data = fetch_expensive_data()
    """

    def __init__(
            self,
            logger: structlog.stdlib.BoundLogger,
            operation: str,
            threshold_ms: float | None = None,
            **context: Any,
    ):
        """
        Args:
            logger: Logger instance
            operation: Название операции
            threshold_ms: Порог для warning (опционально)
            **context: Дополнительный контекст
        """
        self.logger = logger
        self.operation = operation
        self.threshold_ms = threshold_ms
        self.context = context
        self.start_time: float | None = None

    def __enter__(self) -> Self:
        """Start timing."""
        self.start_time = time.perf_counter()
        self.logger.debug(f"{self.operation}_started", **self.context)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Log timing result."""
        duration_ms = (
            (time.perf_counter() - self.start_time) * 1000 if self.start_time else 0
        )

        log_data = {"duration_ms": round(duration_ms, 2), **self.context}

        if exc_type is None:
            # Определяем уровень логирования
            if self.threshold_ms and duration_ms > self.threshold_ms:
                self.logger.warning(f"{self.operation}_completed_slow", **log_data)
            else:
                self.logger.info(f"{self.operation}_completed", **log_data)
        else:
            self.logger.error(
                f"{self.operation}_failed",
                error=str(exc_val),
                exc_info=(exc_type, exc_val, exc_tb),
                **log_data,
            )
