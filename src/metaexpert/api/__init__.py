from abc import ABC, abstractmethod
from importlib import import_module
from typing import Self


class Exchange(ABC):
    stock: str | None
    api_key: str | None
    api_secret: str | None
    base_url: str | None
    instrument: str | None
    contract: str | None

    # def __new__(
    #         cls,
    #         stock: str | None = None,
    #         api_key: str | None = None,
    #         api_secret: str | None = None,
    #         base_url: str | None = None,
    #         instrument: str | None = None,
    #         contract: str | None = None
    # ) -> Self:
    #     """Create a new instance of the Exchange class."""
    #     # instance = super().__new__(cls)
    #     return cls.init_exchange(
    #         stock,
    #         api_key,
    #         api_secret,
    #         base_url,
    #         instrument,
    #         contract
    #     )

    # def __init__(
    #         self,
    #         stock: str | None = None,
    #         api_key: str | None = None,
    #         api_secret: str | None = None,
    #         base_url: str | None = None,
    #         instrument: str | None = None,
    #         contract: str | None = None
    # ) -> None:
    #     self.stock: str | None = stock
    #     self.api_key: str | None = api_key
    #     self.api_secret: str | None = api_secret
    #     self.base_url: str | None = base_url
    #     self.instrument: str | None = instrument
    #     self.contract: str | None = contract

    @classmethod
    def init(cls,
             stock: str | None = None,
             api_key: str | None = None,
             api_secret: str | None = None,
             base_url: str | None = None,
             instrument: str | None = None,
             contract: str | None = None
             ) -> Self:
        cls.stock: str | None = stock
        cls.api_key: str | None = api_key
        cls.api_secret: str | None = api_secret
        cls.base_url: str | None = base_url
        cls.instrument: str | None = instrument
        cls.contract: str | None = contract

        match cls.stock.lower():
            case "binance":
                pkg = import_module("metaexpert.api.binance")
                return pkg.BinanceStock()
                #return pkg.BinanceStock().get_client()
            case "bybit":
                pkg = import_module("metaexpert.api.bybit")
                return pkg.BybitStock()
            case _:
                raise ValueError(f"Unsupported stock: {cls.stock}")

    @abstractmethod
    def get_client(self) -> Self:
        """Lazy initializes and returns the exchange client."""
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def get_account(self):
        pass
