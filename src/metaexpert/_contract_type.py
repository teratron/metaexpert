from enum import Enum
from typing import Self, TypedDict


class ContractTypeDict(TypedDict):
    name: str

class ContractType(Enum):
    """Enum for contract types."""

    COIN_M = {
        "name": "coin_m"
    }
    USD_M = {
        "name": "usd_m"
    }

    @classmethod
    def get_contract_type_from(cls, name: str) -> Self | None:
        """Get the contract_type type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
