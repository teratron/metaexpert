from enum import Enum
from typing import Self


class Contract(Enum):
    """Enum for contract types."""

    COIN_M = {
        "name": "coin_m"
    }
    USD_M = {
        "name": "usd_m"
    }

    @classmethod
    def get_contract_from(cls, name: str | Self) -> Self | None:
        """Get the contract type from a string."""
        if isinstance(name, Contract):
            return name

        for item in cls:
            if item.value["name"] == name.lower():
                return item

        return None
        