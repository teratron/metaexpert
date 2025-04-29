from enum import Enum
from typing import Self


class Mode(Enum):
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
    def get_mode_from(cls, name: str | Self) -> Self | None:
        """Get the mode type from a string."""
        if isinstance(name, Mode):
            return name

        for item in cls:
            if item.value["name"] == name.lower():
                return item

        return None
