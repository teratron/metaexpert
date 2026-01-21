from importlib import import_module
from typing import Self

from metaexpert.exchanges import (
    ContractType,
    # MarginMode,
    MarketType,
    MetaExchange,
    # PositionMode,
)
from metaexpert.exchanges.binance.config import (
    FUTURES_MODULE_INVERSE,
    FUTURES_MODULE_LINEAR,
    FUTURES_PACKAGE,
    FUTURES_WS_BASE_URL,
    SPOT_MODULE,
    SPOT_PACKAGE,
    SPOT_WS_BASE_URL,
)
from metaexpert.utils.package import install_package


class Adapter(MetaExchange):
    """Implementation for the Binance exchange."""

    def __init__(self) -> None:
        """Initializes the Binance class."""
        self.client = self._create_client()

    def _create_client(self) -> Self:
        """Initializes and returns the Binance client based on market type."""
        # For paper trading mode, we don't need API keys
        if not self.testnet and (not self.api_key or not self.api_secret):
            raise ValueError("API key and secret are required for Binance operations.")

        match self.market_type:
            case MarketType.SPOT:
                return self._spot_client()
            case MarketType.FUTURES:
                return self._futures_client()
            case _:
                raise ValueError(
                    f"Unsupported market type for Binance: {self.market_type}"
                )

    def _spot_client(self) -> Self:
        """Returns the Binance Spot client."""
        install_package(SPOT_PACKAGE)
        try:
            pkg = import_module(SPOT_MODULE)
            return pkg.Spot(
                api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url
            )
        except ImportError as e:
            raise ImportError(
                f"Please install {SPOT_PACKAGE}: pip install {SPOT_PACKAGE}"
            ) from e

    def _futures_client(self) -> Self:
        """Returns the Binance Futures client."""
        install_package(FUTURES_PACKAGE)
        try:
            match self.contract_type:
                case ContractType.LINEAR:
                    pkg = import_module(FUTURES_MODULE_LINEAR)
                    return pkg.UMFutures(
                        key=self.api_key, secret=self.api_secret, base_url=self.base_url
                    )
                case ContractType.INVERSE:
                    pkg = import_module(FUTURES_MODULE_INVERSE)
                    return pkg.CMFutures(
                        key=self.api_key, secret=self.api_secret, base_url=self.base_url
                    )
        except ImportError as e:
            raise ImportError(
                f"Please install {FUTURES_PACKAGE}: pip install {FUTURES_PACKAGE}"
            ) from e

    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        """Constructs the WebSocket URL for a given symbol and timeframe."""
        # MEXC uses different streams for different market types
        # Docs:
        base_url: str = ""
        match self.market_type:
            case MarketType.SPOT:
                base_url = SPOT_WS_BASE_URL
            case MarketType.FUTURES:
                base_url = FUTURES_WS_BASE_URL
            case _:
                raise ValueError(
                    f"Unsupported market type for WebSocket: {self.market_type}"
                )

        return f"{base_url}/ws/{symbol.lower()}@kline_{timeframe}"

    def get_account(self) -> dict:
        """Retrieves account information from Binance."""
        if not self.client:
            raise ConnectionError("Client is not initialized.")
        try:
            return {}  # self.client.account()
        except Exception as e:
            raise RuntimeError(f"Failed to get Binance account info: {e}") from e

    def get_balance(self) -> dict | float:
        """Retrieves the account balance from Binance."""
        account_info = self.get_account()
        balance = {
            item["asset"]: item["free"]
            for item in account_info.get("balances", [])
            if float(item["free"]) > 0
        }
        return balance

    def trade(
        self,
        *,
        lots: float = 0,
        stop_loss: float = 0,
        take_profit: float = 0,
        trailing_stop: float = 0,
        positions: int = 0,
        slippage: int = 0,
        fee: float = 0,
    ) -> None:
        """Execute a trade with specified parameters."""
        # TODO: Implement actual trading logic using the client
        pass

    # POSITION
    def open_position(self, side: str, fee: float) -> bool:
        """Open a position."""
        # TODO: Implement position opening logic
        return False

    def close_position(self, side: str) -> bool:
        """Close a position."""
        # TODO: Implement position closing logic
        return False

    def close_all_positions(self, side: str) -> bool:
        """Close all positions."""
        # TODO: Implement closing all positions logic
        return False

    def modify_position(self) -> bool:
        """Modify a position."""
        # TODO: Implement position modification logic
        return False

    def modify_all_positions(self) -> bool:
        """Modify all positions."""
        # TODO: Implement modification of all positions logic
        return False

    # ORDER
    def open_order(self, side: str) -> bool:
        """Open an order."""
        # TODO: Implement order opening logic
        return False

    def close_order(self, side: str) -> bool:
        """Close an order."""
        # TODO: Implement order closing logic
        return False

    def close_all_orders(self, side: str) -> bool:
        """Close all orders."""
        # TODO: Implement closing all orders logic
        return False


# def balance(self: Adapter):
#     self.client.get_balance()
