from importlib import import_module
from types import ModuleType
from typing import Self

from metaexpert.exchanges import Exchange
from metaexpert.utils.install import install_package


class BinanceStock(Exchange):
    """Implementation for the Binance exchange."""

    def __init__(self):
        """Initializes the BinanceStock class."""
        super().__init__()
        self._client: Self | None = self.__get_client()

    def __get_client(self) -> Self | None:
        """Lazy initializes and returns the Binance Spot client."""
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required for Binance operations like get_balance.")

        if self._client is None:
            pkg: ModuleType
            match self.instrument:
                case "spot":
                    install_package("binance-connector")

                    try:
                        pkg = import_module("binance.spot")
                    except ImportError:
                        raise ImportError("Please install binance-connector: pip install binance-connector")

                    self._client: Self = pkg.Spot(api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url)
                case "futures":
                    # self._client = self.__get_client()
                    #from binance.cm_futures import CMFutures
                    install_package("binance-futures-connector")

                    try:
                        pkg = import_module("binance.cm_futures")
                    except ImportError:
                        raise ImportError("Please install binance-connector: pip install binance-connector")

                    self._client: Self = pkg.CMFutures(key=self.api_key, secret=self.api_secret, base_url=self.base_url)
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


def balance(self = None):
    self.client.get_balance()