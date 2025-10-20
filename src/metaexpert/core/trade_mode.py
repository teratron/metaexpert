from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_TRADE_MODE


class TradeMode(Enum):
    """Enum for different trading modes."""

    LIVE = {
        "name": "live",
        "description": "Live trading mode",
    }
    PAPER = {
        "name": "paper",
        "description": "Paper trading mode",
    }
    BACKTEST = {
        "name": "backtest",
        "description": "Backtesting mode",
    }

    def get_name(self) -> str:
        """Return the name of the trading mode."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Trade mode name must be a string, got {type(name).__name__}")

    def get_description(self) -> str:
        """Return the description of the trading mode."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(
            f"Trade mode description must be a string, got {type(description).__name__}"
        )

    @classmethod
    def get_trade_mode_from(cls, name: str) -> Self:
        """Get the mode type from a string."""
        normalized_name = name.lower().strip()
        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_trade_mode_from(DEFAULT_TRADE_MODE)
