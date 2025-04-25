from enum import Enum


class Mode(Enum):
    """Enum for different trading modes."""

    LIVE = {
        "name": "live"
    }
    PAPER = {
        "name": "paper"
    }
    BACKTEST = {
        "name": "backtest"
    }

    def __str__(self) -> str:
        return self.value["name"]

    def __repr__(self) -> str:
        return f"<Mode {self.name!r}>"
