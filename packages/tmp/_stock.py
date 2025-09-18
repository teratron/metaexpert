from enum import Enum
from importlib import import_module
from types import ModuleType
from typing import Self


class Stocks(Enum):
    """Stock enumeration for supported exchanges."""

    BINANCE = {
        "name": "binance",
        "title": "Binance",
        "description": "Binance exchange",
        "strategy_id": 1,
        "module": "metaexpert.exchanges.binance",
    }
    BYBIT = {
        "name": "bybit",
        "title": "Bybit",
        "description": "Bybit exchange",
        "strategy_id": 2,
        "module": "metaexpert.exchanges.bybit"
    }
    OKX = {
        "name": "okx",
        "title": "OKX",
        "description": "OKX exchange",
        "strategy_id": 3,
        "module": "metaexpert.exchanges.okx"
    }

    def get_module(self) -> ModuleType:
        """Get the module for the exchange."""
        return import_module(self.value.get("module"))

    @classmethod
    def get_exchange_from(cls, name: str) -> Self | None:
        """Get the exchange name from the enumeration."""
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None
