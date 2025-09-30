from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_MARGIN_MODE


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
    def get_name(self) -> str:
        """Return the name of the margin mode."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Margin mode name must be a string, got {type(name).__name__}")

    def get_description(self) -> str:
        """Return the description of the margin mode."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(f"Margin mode description must be a string, got {type(description).__name__}")

    @classmethod
    def get_margin_mode_from(cls, name: str) -> Self:
        """Get the margin mode from a string."""
        normalized_name = name.lower().strip()
        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_margin_mode_from(DEFAULT_MARGIN_MODE)
