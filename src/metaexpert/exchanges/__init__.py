from abc import ABC, abstractmethod
from importlib import import_module
from typing import Self


class Exchange(ABC):
    """Abstract base class for stock exchanges."""
    _client: Self | None = None
    stock: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    base_url: str | None = None
    instrument: str | None = None
    contract: str | None = None

    @classmethod
    def init(
            cls,
            stock: str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            base_url: str | None = None,
            instrument: str | None = None,
            contract: str | None = None
    ) -> Self:
        cls.stock = stock.lower() if isinstance(stock, str) else None
        cls.api_key = api_key
        cls.api_secret = api_secret
        cls.base_url = base_url
        cls.instrument = instrument.lower() if isinstance(stock, str) else None
        cls.contract = contract.lower() if isinstance(stock, str) else None

        match cls.stock:
            case "binance":
                return import_module("metaexpert.exchanges.binance").BinanceStock()
            case "bybit":
                return import_module("metaexpert.exchanges.bybit").BybitStock()
            case _:
                raise ValueError(f"Unsupported stock: {cls.stock}")

    @abstractmethod
    def get_balance(self) -> dict | float:
        pass

    @abstractmethod
    def get_account(self) -> dict:
        pass
