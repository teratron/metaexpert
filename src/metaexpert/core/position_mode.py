from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_POSITION_MODE


class PositionMode(Enum):
    """Position mode enumeration for futures trading.

    Supported position modes:
    - HEDGE: Hedge mode (two-way positions)
    - ONEWAY: One-way mode (single position)
    """

    HEDGE = {
        "name": "hedge",
        "description": "Hedge mode (two-way positions)",
    }
    ONEWAY = {
        "name": "oneway",
        "description": "One-way mode (single position)",
    }

    def get_name(self) -> str:
        """Return the name of the position mode."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(
            f"Position mode name must be a string, got {type(name).__name__}"
        )

    def get_description(self) -> str:
        """Return the description of the position mode."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(
            f"Position mode description must be a string, got {type(description).__name__}"
        )

    @classmethod
    def get_position_mode_from(cls, name: str) -> Self:
        """Get the position mode from a string."""
        normalized_name = name.lower().strip()
        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_position_mode_from(DEFAULT_POSITION_MODE)
