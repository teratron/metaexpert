"""Custom formatters for MetaExpert logger."""

import logging
from collections.abc import MutableMapping
from typing import Any

import structlog


class ConsoleRenderer(structlog.dev.ConsoleRenderer):
    """Enhanced console renderer with custom styling."""

    def __init__(self, colors: bool, **kwargs: Any) -> None:
        """Initialize console renderer."""
        super().__init__(colors=colors, **kwargs)

    def __call__(
        self,
        logger: logging.Logger,
        method_name: str,
        event_dict: MutableMapping[str, Any],
    ) -> str:
        """Render log entry with custom formatting."""
        # Extract trade-specific fields for special formatting
        if event_dict.get("event_type") == "trade":
            return self._format_trade_event(event_dict)

        return super().__call__(logger, method_name, event_dict)

    @staticmethod
    def _format_trade_event(event_dict: MutableMapping[str, Any]) -> str:
        """Format trade events specially."""
        symbol = event_dict.get("symbol", "???")
        side = event_dict.get("side", "???")
        price = event_dict.get("price", "???")
        quantity = event_dict.get("quantity", "???")
        timestamp = event_dict.get("timestamp", "")

        # Simple format without trying to access internal color attributes
        # that may not exist in the parent class
        return f"{timestamp} [TRADE] {side.upper()} {quantity} {symbol} @ {price}"


def get_console_renderer(colors: bool = True) -> ConsoleRenderer:
    """Get console renderer based on configuration."""
    return ConsoleRenderer(colors=colors)


def get_file_renderer(
    json_format: bool = False,
) -> structlog.processors.LogfmtRenderer | structlog.processors.JSONRenderer:
    """Get file renderer based on configuration."""
    if json_format:
        # Return the JSON renderer as a processor (for use with ProcessorFormatter)
        # This will be used by ProcessorFormatter to render the final output
        return structlog.processors.JSONRenderer()

    # Human-readable format for files
    return structlog.processors.LogfmtRenderer()
