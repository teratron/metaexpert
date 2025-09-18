from enum import Enum
from typing import Self

from metaexpert._contract_type import Contract


class Instrument(Enum):
    """Market type enumeration for supported instruments."""

    SPOT = {
        "name": "spot",
        "description": "Spot trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    FUTURES = {
        "name": "futures",
        "description": "Futures trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    OPTIONS = {
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
