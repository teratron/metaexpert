from enum import Enum
from typing import Self


class MarginMode(Enum):
    """Margin mode enumeration for futures trading.

    Supported margin modes:
    - ISOLATED: Isolated margin mode
    - CROSS: Cross margin mode
    """

    ISOLATED = {
        "name": "isolated",
        "description": "Isolated margin mode"
    }
    CROSS = {
        "name": "cross",
        "description": "Cross margin mode"
    }

    @classmethod
    def get_margin_mode_from(cls, name: str) -> Self | None:
        """Get the margin mode from a string."""
        # Normalize the name for comparison
        normalized_name = name.lower()

        for item in cls:
            if item.value.get("name") == normalized_name:
                return item

        return None
