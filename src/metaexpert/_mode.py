from enum import Enum
from typing import Self


class TradingMode(Enum):
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

    @classmethod
    def get_mode_from(cls, name: str) -> "TradingMode | None":
        """Get the mode type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None

    def __str__(self) -> str:
        """Return the name of the trading mode."""
        return self.value["name"]
