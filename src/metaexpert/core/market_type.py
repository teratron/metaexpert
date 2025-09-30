from enum import Enum
from typing import Self

from ..config import DEFAULT_MARKET_TYPE
from .contract_type import ContractType


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

    def get_name(self) -> str:
        """Return the name of the market type."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(f"Market type name must be a string, got {type(name).__name__}")

    def get_description(self) -> str:
        """Return the description of the market type."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(f"Market type description must be a string, got {type(description).__name__}")

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

    @classmethod
    def get_market_type_from(cls, name: str) -> Self:
        """Get the market type from a string."""
        normalized_name = name.lower().strip()
        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_market_type_from(DEFAULT_MARKET_TYPE)
