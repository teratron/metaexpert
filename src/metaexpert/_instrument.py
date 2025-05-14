from enum import Enum
from typing import TypedDict, Self

from metaexpert._contract import Contract


class InstrumentDict(TypedDict):
    name: str
    description: str
    contract: list[Contract]


class Instrument(Enum):
    """Instrument enumeration for supported instruments."""

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
    MARGIN = {
        "name": "margin",
        "description": "Margin trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    SWAP = {
        "name": "swap",
        "description": "Swap trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    FORWARD = {
        "name": "forward",
        "description": "Forward trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }
    OPTIONS = {
        "name": "options",
        "description": "Options trading",
        "contract": [Contract.COIN_M, Contract.USD_M]
    }

    @classmethod
    def get_instrument_from(cls, name: str | Self) -> Self | None:
        """Get the instrument type from a string."""
        if isinstance(name, Instrument):
            return name

        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
