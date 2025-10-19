from enum import Enum
from typing import Self

from metaexpert.config import DEFAULT_CONTRACT_TYPE


class ContractType(Enum):
    """Contract type enumeration for futures trading.

    Supported contract types:
    - INVERSE: Inverse contracts (COIN-M)
    - LINEAR: Linear contracts (USD-M)
    """

    LINEAR = {
        "name": "linear",
        "alias": "usd_m",
        "description": "Linear contracts (USD-M)",
    }
    INVERSE = {
        "name": "inverse",
        "alias": "coin_m",
        "description": "Inverse contracts (COIN-M)",
    }

    def get_name(self) -> str:
        """Return the name of the contract type."""
        name = self.value["name"]
        if isinstance(name, str):
            return name
        raise TypeError(
            f"Contract type name must be a string, got {type(name).__name__}"
        )

    def get_alias(self) -> str:
        """Return the alias of the contract type."""
        alias = self.value["alias"]
        if isinstance(alias, str):
            return alias
        raise TypeError(
            f"Contract type alias must be a string, got {type(alias).__name__}"
        )

    def get_description(self) -> str:
        """Return the description of the contract type."""
        description = self.value["description"]
        if isinstance(description, str):
            return description
        raise TypeError(
            f"Contract type description must be a string, got {type(description).__name__}"
        )

    @classmethod
    def get_contract_type_from(cls, name: str) -> Self:
        """Get the contract type from a string."""
        normalized_name: str = name.lower().strip()

        # Handle aliases for backward compatibility
        if normalized_name == "coin_m":
            normalized_name = "inverse"
        elif normalized_name == "usd_m":
            normalized_name = "linear"

        for item in cls:
            if item.get_name() == normalized_name:
                return item
        return cls.get_contract_type_from(DEFAULT_CONTRACT_TYPE)
