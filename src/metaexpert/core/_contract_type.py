from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_CONTRACT_TYPE


class ContractType(Enum):
    """Contract type enumeration for futures trading.

    Supported contract types:
    - INVERSE: Inverse contracts (COIN-M)
    - LINEAR: Linear contracts (USD-M)
    """

    INVERSE = {
        "name": "inverse",
        "alias": "coin_m",
        "description": "Inverse contracts (COIN-M)"
    }
    LINEAR = {
        "name": "linear",
        "alias": "usd_m",
        "description": "Linear contracts (USD-M)"
    }

    @classmethod
    def get_contract_type_from(cls, name: str) -> Self:
        """Get the contract type from a string."""
        # Normalize the name for comparison
        normalized_name: str = name.lower().strip()

        # Handle aliases for backward compatibility
        if normalized_name == "coin_m":
            normalized_name = "inverse"
        elif normalized_name == "usd_m":
            normalized_name = "linear"

        for item in cls:
            if item.value.get("name") == normalized_name:
                return item

        return cls.get_contract_type_from(DEFAULT_CONTRACT_TYPE)
