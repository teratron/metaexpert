from abc import ABC, abstractmethod
from importlib import import_module
from typing import Self


class Exchange(ABC):
    """Abstract base class for stock exchanges."""
    client: Self | None = None
    api_key: str | None = None
    api_secret: str | None = None
    base_url: str | None = None
    market_type: str | None = None
    contract_type: str | None = None

    @classmethod
    def init(
            cls,
            exchange: str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            base_url: str | None = None,
            market_type: str | None = None,
            contract_type: str | None = None
    ) -> Self:
        cls.api_key = api_key
        cls.api_secret = api_secret
        cls.base_url = base_url
        cls.market_type = market_type.lower() if isinstance(market_type, str) else None
        cls.contract_type = contract_type.lower() if isinstance(contract_type, str) else None

        if exchange is None:
            raise ValueError("Stock exchange must be specified.")

        return import_module("metaexpert.exchanges." + exchange.lower()).Stock()

    @abstractmethod
    def get_balance(self) -> dict | float:
        pass

    @abstractmethod
    def get_account(self) -> dict:
        pass

    @abstractmethod
    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        pass
