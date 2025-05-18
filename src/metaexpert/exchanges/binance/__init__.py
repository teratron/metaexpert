from importlib import import_module
from typing import Self

from metaexpert.exchanges import Exchange
from metaexpert.exchanges.binance.config import (
    BINANCE_SPOT_PACKAGE,
    BINANCE_SPOT_MODULE,
    BINANCE_FUTURES_PACKAGE,
    BINANCE_FUTURES_MODULE_USDT_M,
    BINANCE_FUTURES_MODULE_COIN_M
)
from metaexpert.utils.package import install_package


class BinanceStock(Exchange):
    """Implementation for the Binance exchange."""

    def __init__(self):
        """Initializes the BinanceStock class."""
        super().__init__()
        self._client: Self | None = self.__get_client()

    def __get_client(self) -> Self | None:
        """Lazy initializes and returns the Binance Spot client."""
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required for Binance operations.")

        if self._client is None:
            match self.instrument if isinstance(self.instrument, str) else None:
                case "spot":
                    install_package(BINANCE_SPOT_PACKAGE)
                    try:
                        pkg = import_module(BINANCE_SPOT_MODULE)
                    except ImportError:
                        raise ImportError(f"Please install {BINANCE_SPOT_PACKAGE}: pip install {BINANCE_SPOT_PACKAGE}")

                    self._client: Self = pkg.Spot(
                        api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url
                    )
                case "futures":
                    install_package(BINANCE_FUTURES_PACKAGE)
                    try:
                        match self.contract if isinstance(self.contract, str) else None:
                            case "usdt_m":
                                pkg = import_module(BINANCE_FUTURES_MODULE_USDT_M)
                                self._client: Self = pkg.UMFutures(
                                    key=self.api_key, secret=self.api_secret, base_url=self.base_url
                                )
                            case "coin_m":
                                pkg = import_module(BINANCE_FUTURES_MODULE_COIN_M)
                                self._client: Self = pkg.CMFutures(
                                    key=self.api_key, secret=self.api_secret, base_url=self.base_url
                                )
                            case _:
                                raise ValueError(f"Unsupported contract type: {self.contract}")
                    except ImportError:
                        raise ImportError(
                            f"Please install {BINANCE_FUTURES_PACKAGE}: pip install {BINANCE_FUTURES_PACKAGE}"
                        )
                case _:
                    raise ValueError(f"Unsupported instrument: {self.instrument}")

        return self._client

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
        #     account_info = self._client.account()
        #     # Process account_info to extract relevant balance data
        #     # This is a placeholder; the actual structure depends on the API response
        #     balances = {item['asset']: item['free'] for item in account_info.get('balances', []) if float(item['free']) > 0}
        #     return balances
        # except Exception as e:
        #     # Catch specific exceptions from the library if possible
        #     raise RuntimeError(f"Failed to get Binance balance: {e}")

    def get_account(self):
        """Retrieves account information from Binance.

        Returns:
            dict: A dictionary representing the account information.

        Raises:
            RuntimeError: If the API call fails.
            ValueError: If API key/secret are missing.
            ImportError: If binance-connector is not installed.
        """
        print("Binance get_account")
        # print(self.client.account())
        # print(self.client.time())
        # try:
        #     account_info = self._client.account()
        #     return account_info
        # except Exception as e:
        #     raise RuntimeError(f"Failed to get Binance account information: {e}")


def balance(self=None):
    self.client.get_balance()
