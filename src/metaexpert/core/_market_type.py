from enum import Enum
from typing import Self

from ..config import DEFAULT_MARKET_TYPE
from ._contract_type import ContractType


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
        "contract": [ContractType.LINEAR, ContractType.INVERSE]
    }
    OPTIONS = {
        "name": "options",
        "description": "Options trading",
        "contract": [ContractType.LINEAR, ContractType.INVERSE]
    }

    @classmethod
    def get_market_type_from(cls, name: str) -> Self:
        """Get the market type from a string."""
        for item in cls:
            if item.value.get("name") == name.lower().strip():
                return item

        return cls.get_market_type_from(DEFAULT_MARKET_TYPE)

    def has_contracts(self) -> bool:
        """Check if this market type has contracts."""
        return len(self.value.get("contract", [])) > 0

    def get_contract_types(self) -> list[ContractType] |  None:
        """Get the contract types for this market type."""
        if not self.has_contracts():
            raise ValueError("This market type does not have contracts.")

        contract: str | list[ContractType] = self.value["contract"]
        if isinstance(contract, list):
            return contract

        return None
