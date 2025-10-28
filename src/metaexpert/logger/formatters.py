"""Custom formatters for MetaExpert logger."""

from collections.abc import MutableMapping
from typing import Any

import structlog
from structlog.dev import ConsoleRenderer


class MetaConsoleRenderer(ConsoleRenderer):
    """Enhanced console renderer with custom styling."""

    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: MutableMapping[str, Any]
    ) -> str:
        """Render log entry with custom formatting."""
        # Extract trade-specific fields for special formatting
        if event_dict.get("event_type") == "trade":
            return self._format_trade_event(event_dict)

        return super().__call__(logger, method_name, event_dict)

    def _format_trade_event(self, event_dict: MutableMapping[str, Any]) -> str:
        """Format trade events specially."""
        symbol = event_dict.get("symbol", "???")
        side = event_dict.get("side", "???")
        price = event_dict.get("price", "???")
        quantity = event_dict.get("quantity", "???")
        timestamp = event_dict.get("timestamp", "")

        # Simple format without trying to access internal color attributes
        # that may not exist in the parent class
        return f"{timestamp} [TRADE] {side.upper()} {quantity} {symbol} @ {price}"


class CompactJSONRenderer:
    """Compact JSON renderer for production logs."""

    def __call__(self, logger: Any, name: str, event_dict: dict[str, Any]) -> str:
        """Render log entry as compact JSON."""
        import json

        # Remove internal fields
        clean_dict = {k: v for k, v in event_dict.items() if not k.startswith("_")}

        return json.dumps(clean_dict, separators=(",", ":"))


def get_console_renderer(colors: bool = True) -> Any:
    """Get console renderer based on configuration."""
    return MetaConsoleRenderer(colors=colors)


def get_file_renderer(json_format: bool = False) -> Any:
    """Get file renderer based on configuration."""
    if json_format:
        # Return the JSON renderer as a processor (for use with ProcessorFormatter)
        # This will be used by ProcessorFormatter to render the final output
        return structlog.processors.JSONRenderer()

    # Human-readable format for files
    return structlog.processors.LogfmtRenderer()
