from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
from typing import Self

from metaexpert.core import Market, Trade


@dataclass
class MetaExchange(Trade, Market, ABC):
    """Abstract base class for stock exchanges."""

    exchange: str
    api_key: str | None
    api_secret: str | None
    api_passphrase: str | None
    subaccount: str | None
    base_url: str | None
    testnet: bool
    proxy: dict[str, str] | None
    market_type: str
    contract_type: str
    margin_mode: str
    position_mode: str

    # def __init__(
    #         self,
    #         exchange: str,
    #         api_key: str | None,
    #         api_secret: str | None,
    #         api_passphrase: str | None,
    #         subaccount: str | None,
    #         base_url: str | None,
    #         testnet: bool,
    #         proxy: dict[str, str] | None,
    #         market_type: str,
    #         contract_type: str,
    #         margin_mode: str,
    #         position_mode: str
    #     ) -> None:
    #     """Initialize the exchange."""
    #     self.exchange = exchange.lower().strip()
    #     self.api_key = api_key
    #     self.api_secret = api_secret
    #     self.api_passphrase = api_passphrase
    #     self.subaccount = subaccount
    #     self.base_url = base_url
    #     self.testnet = testnet
    #     self.proxy = proxy
    #     self.market_type = market_type.lower().strip()
    #     self.contract_type = contract_type.lower().strip()
    #     self.margin_mode = margin_mode.lower().strip()
    #     self.position_mode = position_mode.lower().strip()

    @classmethod
    def create(
        cls,
        exchange: str,
        api_key: str | None,
        api_secret: str | None,
        api_passphrase: str | None,
        subaccount: str | None,
        base_url: str | None,
        testnet: bool,
        proxy: dict[str, str] | None,
        market_type: str,
        contract_type: str,
        margin_mode: str,
        position_mode: str
    ) -> Self:
        """Factory method to create an exchange instance."""
        cls.exchange = exchange.lower().strip()
        cls.api_key = api_key
        cls.api_secret = api_secret
        cls.api_passphrase = api_passphrase
        cls.subaccount = subaccount
        cls.base_url = base_url
        cls.testnet = testnet
        cls.proxy = proxy
        cls.market_type = market_type.lower().strip()
        cls.contract_type = contract_type.lower().strip()
        cls.margin_mode = margin_mode.lower().strip()
        cls.position_mode = position_mode.lower().strip()

        try:
            module = import_module(f"metaexpert.exchanges.{cls.exchange}")
            return module.Adapter()
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Unsupported exchange: {cls.exchange}") from e

    @abstractmethod
    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        """Get WebSocket URL for a given symbol and timeframe."""
        pass
