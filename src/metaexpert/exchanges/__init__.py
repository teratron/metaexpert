from abc import ABC, abstractmethod
from importlib import import_module
from typing import Self


# from types import ModuleType

#from metaexpert.exchanges._stock import Stocks


class Exchange(ABC):
    """Abstract base class for stock exchanges."""
    client: Self | None = None
    #stock: Stocks | None = None
    api_key: str | None = None
    api_secret: str | None = None
    base_url: str | None = None
    instrument: str | None = None
    contract: str | None = None

    # def __new__(cls, *args, **kwargs) -> Self:
    #     """Create a new instance of the Exchange class."""
    #     instance = super().__new__(cls)
    #     print(f"Creating instance of {cls.__name__}")
    #     print(f"Arguments: {args}, {kwargs}")
    #     return instance

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
        #cls.stock: Stocks = Stocks.get_exchange_from(stock.lower()) if isinstance(stock, str) else None
        cls.api_key = api_key
        cls.api_secret = api_secret
        cls.base_url = base_url
        cls.instrument = instrument.lower() if isinstance(stock, str) else None
        cls.contract = contract.lower() if isinstance(stock, str) else None

        # return cls.stock.get_module().Stock()

        if stock is None:
            raise ValueError("Stock exchange must be specified.")

        return import_module("metaexpert.exchanges." + stock.lower()).Stock()

    @abstractmethod
    def get_balance(self) -> dict | float:
        pass

    @abstractmethod
    def get_account(self) -> dict:
        pass
