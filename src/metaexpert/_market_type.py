from enum import Enum
from typing import Self, TypedDict

from metaexpert._contract_type import ContractType


class MarketTypeDict(TypedDict):
    name: str
    description: str
    contract: list[ContractType]


class MarketType(Enum):
    """Market type enumeration for supported instruments."""

    SPOT = {
        "name": "spot",
        "description": "Spot trading",
        "contract": [ContractType.COIN_M, ContractType.USD_M]
    }
    FUTURES = {
        "name": "futures",
        "description": "Futures trading",
        "contract": [ContractType.COIN_M, ContractType.USD_M]
    }
    OPTIONS = {
        "name": "options",
        "description": "Options trading",
        "contract": [ContractType.COIN_M, ContractType.USD_M]
    }

    @classmethod
    def get_market_type_from(cls, name: str) -> Self | None:
        """Get the market type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
