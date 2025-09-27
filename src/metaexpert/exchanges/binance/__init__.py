from importlib import import_module
from typing import Any, Self

from metaexpert.exchanges import Exchange
from metaexpert.exchanges.binance.config import (
    BINANCE_FUTURES_MODULE_COIN_M,
    BINANCE_FUTURES_MODULE_USDT_M,
    BINANCE_FUTURES_PACKAGE,
    BINANCE_FUTURES_WS_BASE_URL,
    BINANCE_SPOT_MODULE,
    BINANCE_SPOT_PACKAGE,
    BINANCE_SPOT_WS_BASE_URL,
)
from metaexpert.utils.package import install_package


class Adapter(Exchange):
    """Implementation for the Binance exchange."""

    def __init__(self):
        """Initializes the Binance class."""
        self.client: Self | None = self._create_client()

    def _create_client(self) -> Self | None:
        """Initializes and returns the Binance client based on market type."""
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required for Binance operations.")

        if self.market_type == "spot":
            return self._spot_client()
        elif self.market_type == "futures":
            return self._futures_client()
        else:
            raise ValueError(f"Unsupported market type for Binance: {self.market_type}")

    def _spot_client(self) -> Self:
        """Returns the Binance Spot client."""
        install_package(BINANCE_SPOT_PACKAGE)
        try:
            pkg = import_module(BINANCE_SPOT_MODULE)
            return pkg.Spot(
                api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url
            )
        except ImportError as e:
            raise ImportError(f"Please install {BINANCE_SPOT_PACKAGE}: pip install {BINANCE_SPOT_PACKAGE}") from e

    def _futures_client(self) -> Self:
        """Returns the Binance Futures client."""
        install_package(BINANCE_FUTURES_PACKAGE)
        try:
            if self.contract_type == "linear":
                pkg = import_module(BINANCE_FUTURES_MODULE_USDT_M)
                return pkg.UMFutures(
                    key=self.api_key, secret=self.api_secret, base_url=self.base_url
                )
            elif self.contract_type == "inverse":
                pkg = import_module(BINANCE_FUTURES_MODULE_COIN_M)
                return pkg.CMFutures(
                    key=self.api_key, secret=self.api_secret, base_url=self.base_url
                )
            else:
                raise ValueError(f"Unsupported contract type: {self.contract_type}")
        except ImportError as e:
            raise ImportError(f"Please install {BINANCE_FUTURES_PACKAGE}: pip install {BINANCE_FUTURES_PACKAGE}") from e

    # def get_account(self) -> dict:
    #     """Retrieves account information from Binance."""
    #     if not self.client:
    #         raise ConnectionError("Client is not initialized.")
    #     try:
    #         return self.client.account()
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to get Binance account info: {e}") from e
    #
    # def get_balance(self) -> dict | float:
    #     """Retrieves the account balance from Binance."""
    #     account_info = self.get_account()
    #     balance = {
    #         item['asset']: item['free']
    #         for item in account_info.get('balances', [])
    #         if float(item['free']) > 0
    #     }
    #     return balance

    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        """Constructs the WebSocket URL for a given symbol and timeframe."""
        if self.market_type == "spot":
            base_url = BINANCE_SPOT_WS_BASE_URL
        elif self.market_type == "futures":
            base_url = BINANCE_FUTURES_WS_BASE_URL
        else:
            raise ValueError(f"Unsupported market type for WebSocket: {self.market_type}")

        return f"{base_url}/ws/{symbol.lower()}@kline_{timeframe}"
