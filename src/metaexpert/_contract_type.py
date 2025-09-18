from enum import Enum
from typing import ClassVar, Self


class Contract(Enum):
    """Enum for contract types."""

    COIN_M: ClassVar[dict] = {
        "name": "coin_m"
    }
    USD_M: ClassVar[dict] = {
        "name": "usd_m"
    }

    @classmethod
    def get_contract_type_from(cls, name: str) -> Self | None:
        """Get the contract_type type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
