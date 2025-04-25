from enum import Enum


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

    def __str__(self) -> str:
        return self.value["name"]

    def __repr__(self) -> str:
        return f"<Mode {self.name!r}>"
