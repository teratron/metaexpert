from enum import Enum
from typing import Self


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
        "description": "Fixed amount in base currency"
    }
    FIXED_QUOTE = {
        "name": "fixed_quote",
        "description": "Fixed amount in quote currency"
    }
    PERCENT_EQUITY = {
        "name": "percent_equity",
        "description": "Percentage of account equity"
    }
    RISK_BASED = {
        "name": "risk_based",
        "description": "Risk-based position sizing"
    }

    @classmethod
    def get_size_type_from(cls, name: str) -> Self | None:
        """Get the size type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None

    @classmethod
    def get_default(cls) -> "SizeType":
        """Get the default size type."""
        return cls.RISK_BASED
