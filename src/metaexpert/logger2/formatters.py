"""Custom formatters for MetaExpert logger."""

from typing import Any

import structlog
from structlog.dev import ConsoleRenderer


class MetaExpertConsoleRenderer(ConsoleRenderer):
    """Enhanced console renderer with custom styling."""

    def __init__(self, colors: bool = True, **kwargs):
        """Initialize renderer with color support."""
        super().__init__(colors=colors, **kwargs)

        # Custom color scheme
        if colors:
            self._level_to_color.update(
                {
                    "trade": self._colorama.Fore.GREEN,
                    "position": self._colorama.Fore.CYAN,
                    "order": self._colorama.Fore.YELLOW,
                }
            )

    def __call__(self, logger: Any, name: str, event_dict: dict[str, Any]) -> str:
        """Render log entry with custom formatting."""
        # Extract trade-specific fields for special formatting
        if event_dict.get("event_type") == "trade":
            return self._format_trade_event(event_dict)

        return super().__call__(logger, name, event_dict)

    def _format_trade_event(self, event_dict: dict[str, Any]) -> str:
        """Format trade events specially."""
        symbol = event_dict.get("symbol", "???")
        side = event_dict.get("side", "???")
        price = event_dict.get("price", "???")
        quantity = event_dict.get("quantity", "???")

        timestamp = event_dict.get("timestamp", "")

        if self._colors:
            color = self._colorama.Fore.GREEN
            reset = self._colorama.Style.RESET_ALL

            return (
                f"{timestamp} "
                f"{color}[TRADE]{reset} "
                f"{side.upper()} {quantity} {symbol} @ {price}"
            )

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
    return MetaExpertConsoleRenderer(colors=colors)


def get_file_renderer(json_format: bool = False) -> Any:
    """Get file renderer based on configuration."""
    if json_format:
        return structlog.processors.JSONRenderer()

    # Human-readable format for files
    return structlog.processors.LogfmtRenderer()
