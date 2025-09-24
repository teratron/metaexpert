from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
from typing import Any


@dataclass
class Exchange(ABC):
    """Abstract base class for stock exchanges."""

    def __init__(
            self,
            exchange_name: str | None = None,
            api_key: str | None = None,
            api_secret: str | None = None,
            api_passphrase: str | None = None,
            subaccount: str | None = None,
            base_url: str | None = None,
            market_type: str | None = None,
            contract_type: str | None = None,
            testnet: bool = False,
            proxy: dict[str, str] | None = None,
            margin_mode: str | None = None,
            position_mode: str | None = None,
            **kwargs: Any
    ):
        self.exchange_name = exchange_name.lower().strip() if isinstance(exchange_name, str) else None
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.subaccount = subaccount
        self.base_url = base_url
        self.market_type = market_type.lower().strip() if isinstance(market_type, str) else None
        self.contract_type = contract_type.lower().strip() if isinstance(contract_type, str) else None
        self.testnet = testnet
        self.proxy = proxy
        self.margin_mode = margin_mode.lower().strip() if isinstance(margin_mode, str) else None
        self.position_mode = position_mode.lower().strip() if isinstance(position_mode, str) else None
        self.client: Any | None = None

    @staticmethod
    def create(exchange_name: str, **kwargs: Any) -> "Exchange":
        """Factory method to create an exchange instance."""
        if not exchange_name:
            raise ValueError("Stock exchange name must be specified.")
        try:
            module = import_module(f"metaexpert.exchanges.{exchange_name}")
            exchange_class: type[Exchange] = module.Adapter
            return exchange_class(exchange_name=exchange_name, **kwargs)
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Unsupported exchange: {exchange_name}") from e

    @abstractmethod
    def get_balance(self) -> dict | float:
        """Get account balance."""
        pass

    @abstractmethod
    def get_account(self) -> dict:
        """Get account details."""
        pass

    @abstractmethod
    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        """Get WebSocket URL for a given symbol and timeframe."""
        pass
