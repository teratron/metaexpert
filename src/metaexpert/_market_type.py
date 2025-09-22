from enum import Enum
from typing import Self

from metaexpert._contract_type import ContractType


class MarketType(Enum):
    """Market type enumeration for supported instruments.

    Supported market types:
    - SPOT: Spot trading (no contracts)
    - FUTURES: Futures trading with contract types (linear/usd_m or inverse/coin_m)
    - OPTIONS: Options trading with contract types (linear/usd_m or inverse/coin_m)
    """

    SPOT = {
        "name": "spot",
        "description": "Spot trading",
        "contract": []  # Spot trading has no contracts
    }
    FUTURES = {
        "name": "futures",
        "description": "Futures trading",
        "contract": [ContractType.INVERSE, ContractType.LINEAR]  # inverse/coin_m or linear/usd_m
    }
    OPTIONS = {
        "name": "options",
        "description": "Options trading",
        "contract": [ContractType.INVERSE, ContractType.LINEAR]  # inverse/coin_m or linear/usd_m
    }

    @classmethod
    def get_market_type_from(cls, name: str) -> Self | None:
        """Get the market type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None

    def has_contracts(self) -> bool:
        """Check if this market type has contracts."""
        return len(self.value.get("contract", [])) > 0

    def get_contract_types(self) -> list[ContractType]:
        """Get the contract types for this market type."""
        return self.value.get("contract", [])
