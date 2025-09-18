from enum import Enum
from typing import ClassVar, Self, TypedDict

from metaexpert._contract_type import Contract


class InstrumentDict(TypedDict):
    name: str
    description: str
    contract: list[Contract]

class Instrument(Enum):
    """Market type enumeration for supported instruments."""

    SPOT: ClassVar[dict] = {
        "name": "spot",
        "description": "Spot trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    FUTURES: ClassVar[dict] = {
        "name": "futures",
        "description": "Futures trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    OPTIONS: ClassVar[dict] = {
        "name": "options",
        "description": "Options trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }

    @classmethod
    def get_market_type_from(cls, name: str) -> Self | None:
        """Get the market type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
