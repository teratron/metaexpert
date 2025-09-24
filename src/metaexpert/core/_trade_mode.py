from enum import Enum
from typing import Self


class TradeMode(Enum):
    """Enum for different trading modes."""

    LIVE = {
        "name": "live",
        "description": "Live trading mode"
    }
    PAPER = {
        "name": "paper",
        "description": "Paper trading mode"
    }
    BACKTEST = {
        "name": "backtest",
        "description": "Backtesting mode"
    }

    def get_name(self) -> str:
        """Return the name of the trading mode."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Trade mode name must be a string, got {type(name).__name__}")

    @classmethod
    def get_mode_from(cls, name: str) -> Self | None:
        """Get the mode type from a string."""
        for item in cls:
            if item.get_name() == name.lower():
                return item
        return None
