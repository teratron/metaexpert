# -*- coding: utf-8 -*-

from enum import Enum


class Stock(Enum):
    """Stock enumeration for supported exchanges."""
    BINANCE = {
        "name": "Binance",
        "description": "Binance exchange",
    }
    BYBIT = {
        "name": "Bybit",
        "description": "Bybit exchange",
    }


class Exchange:
    def __init__(self):
        self.logger = None

    def init_exchange(self, stock: Stock) -> None:
        match stock:
            case Stock.BINANCE:
                self.logger.debug("Binance exchange selected")
            case Stock.BYBIT:
                self.logger.debug("Bybit exchange selected")
            case _:
                self.logger.warning("Unknown exchange selected")

        # if self.trade_mode == MODE_LIVE and (not self.api_key or not self.api_secret):
        #     self.logger.error("API key and secret are required for live trading")
        #     raise ValueError("API key and secret are required for live trading")
        #
        # # Initialize client with or without authentication based on mode
        # if self.trade_mode == MODE_BACKTEST or (not self.api_key or not self.api_secret):
        #     # self.client = Spot()
        #     self.logger.info("Initialized Binance client in public mode")
        # else:
        #     # self.client = Spot(api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url)
        #     self.logger.info("Initialized Binance client with API key authentication")
