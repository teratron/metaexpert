from enum import Enum
from typing import Self


class PositionMode(Enum):
    """Position mode enumeration for futures trading.

    Supported position modes:
    - HEDGE: Hedge mode (two-way positions)
    - ONEWAY: One-way mode (single position)
    """

    HEDGE = {
        "name": "hedge",
        "description": "Hedge mode (two-way positions)"
    }
    ONEWAY = {
        "name": "oneway",
        "description": "One-way mode (single position)"
    }

    @classmethod
    def get_position_mode_from(cls, name: str) -> Self | None:
        """Get the position mode from a string."""
        # Normalize the name for comparison
        normalized_name = name.lower()

        for item in cls:
            if item.value.get("name") == normalized_name:
                return item

        return None
