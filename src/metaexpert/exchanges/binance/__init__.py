from importlib import import_module
from typing import Self

from metaexpert.exchanges import Exchange
from metaexpert.exchanges.binance.config import (
    BINANCE_SPOT_PACKAGE,
    BINANCE_SPOT_MODULE,
    BINANCE_FUTURES_PACKAGE,
    BINANCE_FUTURES_MODULE_USDT_M,
    BINANCE_FUTURES_MODULE_COIN_M, BINANCE_SPOT_WS_BASE_URL, BINANCE_FUTURES_WS_BASE_URL
)
from metaexpert.utils.package import install_package


# class BinanceStock(Exchange):
class Stock(Exchange):
    """Implementation for the Binance exchange."""

    def __init__(self):
        """Initializes the BinanceStock class."""
        super().__init__()
        self.client = self.__get_client()

    def __get_client(self) -> Self | None:
        """Lazy initializes and returns the Binance Spot client."""
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required for Binance operations.")

        if self.client is None:
            match self.market_type if isinstance(self.market_type, str) else None:
                case "spot":
                    self.client = self.__spot_client()
                case "futures":
                    self.client = self.__futures_client()

        return self.client

    def __spot_client(self) -> Self:
        """Returns the Binance Spot client."""
        install_package(BINANCE_SPOT_PACKAGE)
        try:
            pkg = import_module(BINANCE_SPOT_MODULE)
        except ImportError:
            raise ImportError(f"Please install {BINANCE_SPOT_PACKAGE}: pip install {BINANCE_SPOT_PACKAGE}")

        return pkg.Spot(
            api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url
        )

    def __futures_client(self) -> Self:
        """Returns the Binance Futures client."""
        install_package(BINANCE_FUTURES_PACKAGE)
        try:
            match self.contract_type if isinstance(self.contract_type, str) else None:
                case "linear":
                    pkg = import_module(BINANCE_FUTURES_MODULE_USDT_M)
                    return pkg.UMFutures(
                        key=self.api_key, secret=self.api_secret, base_url=self.base_url
                    )
                case "inverse":
                    pkg = import_module(BINANCE_FUTURES_MODULE_COIN_M)
                    return pkg.CMFutures(
                        key=self.api_key, secret=self.api_secret, base_url=self.base_url
                    )
                case _:
                    raise ValueError(f"Unsupported contract type: {self.contract_type}")
        except ImportError:
            raise ImportError(f"Please install {BINANCE_FUTURES_PACKAGE}: pip install {BINANCE_FUTURES_PACKAGE}")

    def get_balance(self):
        """Retrieves the account balance from Binance.

        Returns:
            dict: A dictionary representing the account balance information.

        Raises:
            RuntimeError: If the API call fails.
            ValueError: If API key/secret are missing.
            ImportError: If binance-connector is not installed.
        """
        print("Binance get_balance")
        # try:
        #     # Example: Fetch account information which includes balances
        #     # Adjust the specific API call based on binance-connector documentation
        #     # if account() is not the correct method or requires different parameters.
        #     account_info = self.client.account()
        #     # Process account_info to extract relevant balance data
        #     # This is a placeholder; the actual structure depends on the API response
        #     balances = {item['asset']: item['free'] for item in account_info.get('balances', []) if float(item['free']) > 0}
        #     return balances
        # except Exception as e:
        #     # Catch specific exceptions from the library if possible
        #     raise RuntimeError(f"Failed to get Binance balance: {e}")

    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        """Constructs the WebSocket URL for a given symbol and timeframe."""
        base_url = ""
        if self.market_type == "spot":
            base_url = BINANCE_SPOT_WS_BASE_URL
        elif self.market_type == "futures":
            base_url = BINANCE_FUTURES_WS_BASE_URL
        else:
            raise ValueError(f"Unsupported market type for WebSocket: {self.market_type}")

        return f"{base_url}/ws/{symbol.lower()}@kline_{timeframe}"


def balance(self=None):
    self.client.get_balance()
