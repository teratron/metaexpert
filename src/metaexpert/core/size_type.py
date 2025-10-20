from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_SIZE_TYPE


class SizeType(Enum):
    """Position sizing method enumeration for trade size calculation.

    Supported position sizing methods:
    - FIXED_BASE: Fixed amount in base currency
    - FIXED_QUOTE: Fixed amount in quote currency
    - PERCENT_EQUITY: Percentage of account equity
    - RISK_BASED: Risk-based position sizing (default)
    """

    FIXED_BASE = {
        "name": "fixed_base",
        "description": "Fixed amount in base currency",
    }
    FIXED_QUOTE = {
        "name": "fixed_quote",
        "description": "Fixed amount in quote currency",
    }
    PERCENT_EQUITY = {
        "name": "percent_equity",
        "description": "Percentage of account equity",
    }
    RISK_BASED = {
        "name": "risk_based",
        "description": "Risk-based position sizing",
    }

    def get_name(self) -> str:
        """Return the name of the size type."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Size type name must be a string, got {type(name).__name__}")

    def get_description(self) -> str:
        """Return the description of the size type."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(
            f"Size type description must be a string, got {type(description).__name__}"
        )

    @classmethod
    def get_size_type_from(cls, name: str) -> Self:
        """Get the size type from a string."""
        normalized_name = name.lower().strip()
        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_size_type_from(DEFAULT_SIZE_TYPE)
