# -*- coding: utf-8 -*-

from enum import Enum
from typing import Self, TypedDict


class ProcessDict(TypedDict):
    name: str
    title: str
    description: str


class Stock(Enum):
    """Stock enumeration for supported exchanges."""

    BINANCE = {
        "name": "binance",
        "title": "Binance",
        "description": "Binance exchange",
    }
    BYBIT = {
        "name": "bybit",
        "title": "Bybit",
        "description": "Bybit exchange",
    }

    def init_exchange(self) -> None:
        print("Initializing exchange:", self.value["name"])

    @classmethod
    def get_exchange_name(cls, name: str) -> Self | None:
        """Get the exchange name from the enumeration."""
        for item in cls:
            if item.value["name"] == name.lower():
                return item

        return None


class Exchange:
    def __init__(self) -> None:
        self.logger = None

    def init_exchange(self, stock: Stock) -> None:
        match stock:
            case Stock.BINANCE:
                self.logger.debug("%s exchange selected", stock.value["title"])
            case Stock.BYBIT:
                self.logger.debug("%s exchange selected", stock.value["title"])
            case _:
                self.logger.warning("Unknown exchange selected")

        # if self.mode == MODE_LIVE and (not self.api_key or not self.api_secret):
        #     self.logger.error("API key and secret are required for live trading")
        #     raise ValueError("API key and secret are required for live trading")
        #
        # # Initialize client with or without authentication based on mode
        # if self.mode == MODE_BACKTEST or (not self.api_key or not self.api_secret):
        #     # self.client = Spot()
        #     self.logger.info("Initialized Binance client in public mode")
        # else:
        #     # self.client = Spot(api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url)
        #     self.logger.info("Initialized Binance client with API key authentication")
