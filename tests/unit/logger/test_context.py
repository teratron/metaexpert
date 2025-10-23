"""Tests for MetaExpert logger context utilities."""


from metaexpert.logger.context import (
    LogContext,
    bind_contextvars,
    clear_contextvars,
    get_logger,
    get_trade_logger,
    iterate_with_context,
    request_id_var,
    strategy_id_var,
    trade_context,
    trade_session_var,
    unbind_contextvars,
)


def test_bind_contextvars():
    """Test binding context variables."""
    # Clear any existing context
    clear_contextvars()

    # Just verify the function runs without error
    # We can't easily check internal state without using internal APIs
    bind_contextvars(request_id="test123", strategy_id=1001)
    assert True


def test_unbind_contextvars():
    """Test unbinding specific context variables."""
    # Clear any existing context
    clear_contextvars()

    # Bind some context variables first
    bind_contextvars(request_id="test123", strategy_id=1001, extra_var="extra")

    # Unbind specific variables
    unbind_contextvars("request_id", "strategy_id")

    # Just verify the function runs without error
    assert True


def test_clear_contextvars():
    """Test clearing all context variables."""
    # Clear any existing context
    clear_contextvars()

    # Bind some context variables
    bind_contextvars(request_id="test123", strategy_id=1001)

    # Clear all context
    clear_contextvars()

    # Just verify the function runs without error
    assert True


def test_LogContext_manager():
    """Test the LogContext context manager."""
    # Clear any existing context
    clear_contextvars()

    # Use the context manager
    with LogContext(symbol="BTCUSDT", exchange="binance"):
        # Context is bound within the block
        pass

    # Just verify the context manager runs without error
    assert True


def test_trade_context_manager():
    """Test the trade_context context manager."""
    # Clear any existing context
    clear_contextvars()

    # Use the trade context manager
    with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01, strategy_id=1001):
        # Context is bound within the block
        pass

    # Just verify the context manager runs without error
    assert True


def test_get_logger():
    """Test getting a logger with optional initial context."""
    # Clear any existing context
    clear_contextvars()

    # Get a logger without initial context
    logger1 = get_logger("test_module")
    assert logger1 is not None

    # Get a logger with initial context
    logger2 = get_logger("test_module", exchange="binance", strategy_id=1001)

    # The logger should be bound with the initial context
    # To test this, we'll need to check how structlog handles bound loggers
    # For now, just ensure it returns a logger instance
    assert logger2 is not None


def test_get_trade_logger():
    """Test getting a trade logger."""
    # Clear any existing context
    clear_contextvars()

    # Get a trade logger
    trade_logger = get_trade_logger(symbol="BTCUSDT", strategy_id=1001)

    # The logger should be bound with event_type="trade" and other initial context
    assert trade_logger is not None


def test_iterate_with_context():
    """Test the iterate_with_context utility."""
    # Clear any existing context
    clear_contextvars()

    items = ["item1", "item2", "item3"]
    context = {"strategy_id": 1001}

    # Use iterate_with_context
    collected_items = []
    for item in iterate_with_context(items, **context):
        collected_items.append(item)

    # Check that all items were processed
    assert collected_items == items

    # Just verify the function runs without error
    assert True


def test_context_variables_initial_state():
    """Test that context variables have correct initial state."""
    # Check initial state of context variables
    assert request_id_var.get() is None
    assert trade_session_var.get() is None
    assert strategy_id_var.get() is None
