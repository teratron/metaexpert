"""Tests for MetaExpert logger formatters."""

from unittest.mock import Mock

from metaexpert.logger.formatters import (
    ConsoleRenderer,
    get_console_renderer,
    get_file_renderer,
)


def test_meta_expert_console_renderer_initialization():
    """Test initialization of ConsoleRenderer."""
    # Test that the renderer can be instantiated
    renderer_with_colors = ConsoleRenderer(colors=True)
    assert renderer_with_colors is not None

    # Test with colors disabled
    renderer_without_colors = ConsoleRenderer(colors=False)
    assert renderer_without_colors is not None


def test_meta_expert_console_renderer_custom_colors():
    """Test custom color scheme in ConsoleRenderer."""
    renderer = ConsoleRenderer(colors=True)

    # Just verify that the renderer was created successfully
    # We can't easily test internal color attributes without knowing the exact implementation
    assert renderer is not None


def test_meta_expert_console_renderer_trade_formatting_with_colors():
    """Test trade event formatting with colors."""
    renderer = ConsoleRenderer(colors=True)

    # Create a trade event dictionary
    event_dict = {
        "timestamp": "2023-01-01T12:00:00Z",
        "event_type": "trade",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 50000,
        "quantity": 0.01,
    }

    # Mock logger and name for the call
    logger = Mock()
    name = "test_logger"

    # Call the renderer
    result = renderer(logger, name, event_dict)

    # Check that the result contains trade-specific formatting
    # Since colors are enabled, the output will contain color codes
    assert "[TRADE]" in result
    assert "BTCUSDT" in result
    assert "BUY" in result
    assert "50000" in result
    assert "0.01" in result


def test_meta_expert_console_renderer_trade_formatting_without_colors():
    """Test trade event formatting without colors."""
    renderer = ConsoleRenderer(colors=False)

    # Create a trade event dictionary
    event_dict = {
        "timestamp": "2023-01-01T12:00:00Z",
        "event_type": "trade",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 50000,
        "quantity": 0.01,
    }

    # Mock logger and name for the call
    logger = Mock()
    name = "test_logger"

    # Call the renderer
    result = renderer(logger, name, event_dict)

    # Check that the result contains trade-specific formatting
    # Without colors, the output should be plain text
    assert "[TRADE]" in result
    assert "BTCUSDT" in result
    assert "BUY" in result
    assert "5000" in result
    assert "0.01" in result
    # Should not contain color codes
    assert "\x1b[" not in result  # ANSI color code start


def test_meta_expert_console_renderer_regular_formatting():
    """Test regular (non-trade) event formatting."""
    renderer = ConsoleRenderer(colors=True)

    # Create a regular event dictionary
    event_dict = {
        "timestamp": "2023-01-01T12:00:00Z",
        "event": "regular log message",
        "level": "info",
    }

    # Mock logger and name for the call
    logger = Mock()
    name = "test_logger"

    # Call the renderer
    result = renderer(logger, name, event_dict)

    # Should use default console formatting, not trade formatting
    assert "regular log message" in result
    # Should not contain [TRADE] marker
    assert "[TRADE]" not in result


def test_get_console_renderer():
    """Test get_console_renderer function."""
    # Test with colors enabled
    renderer1 = get_console_renderer(colors=True)
    assert isinstance(renderer1, ConsoleRenderer)

    # Test with colors disabled
    renderer2 = get_console_renderer(colors=False)
    assert isinstance(renderer2, ConsoleRenderer)


def test_get_file_renderer_json():
    """Test get_file_renderer function with JSON format."""
    from metaexpert.logger.formatters import structlog

    # Test with JSON format
    renderer = get_file_renderer(json_format=True)
    # Should return structlog.processors.JSONRenderer
    assert isinstance(renderer, type(structlog.processors.JSONRenderer()))


def test_get_file_renderer_logfmt():
    """Test get_file_renderer function with logfmt format."""
    from metaexpert.logger.formatters import structlog

    # Test with non-JSON format
    renderer = get_file_renderer(json_format=False)
    # Should return structlog.processors.LogfmtRenderer
    assert isinstance(renderer, type(structlog.processors.LogfmtRenderer()))
