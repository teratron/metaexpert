"""Exchange API integration module."""

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ExchangeInfo:
    """Information about an exchange."""

    name: str
    api_base_url: str
    requires_passphrase: bool
    supported_features: list[str]

class ExchangeAPIManager:
    """Manager for exchange API integrations."""

    def __init__(self) -> None:
        """Initialize the exchange API manager."""
        self.exchanges = {
            "binance": ExchangeInfo(
                name="Binance",
                api_base_url="https://api.binance.com",
                requires_passphrase=False,
                supported_features=["spot", "futures", "options"]
            ),
            "bybit": ExchangeInfo(
                name="Bybit",
                api_base_url="https://api.bybit.com",
                requires_passphrase=False,
                supported_features=["spot", "futures"]
            ),
            "okx": ExchangeInfo(
                name="OKX",
                api_base_url="https://www.okx.com",
                requires_passphrase=True,
                supported_features=["spot", "futures", "options"]
            ),
            "bitget": ExchangeInfo(
                name="Bitget",
                api_base_url="https://api.bitget.com",
                requires_passphrase=False,
                supported_features=["spot", "futures"]
            ),
            "kucoin": ExchangeInfo(
                name="KuCoin",
                api_base_url="https://api.kucoin.com",
                requires_passphrase=True,
                supported_features=["spot", "futures"]
            )
        }

    def get_exchange_info(self, exchange_name: str) -> ExchangeInfo | None:
        """Get information about an exchange.

        Args:
            exchange_name: Name of the exchange

        Returns:
            ExchangeInfo object or None if not found
        """
        return self.exchanges.get(exchange_name.lower())

    def get_supported_exchanges(self) -> list[str]:
        """Get a list of supported exchanges.

        Returns:
            List of supported exchange names
        """
        return list(self.exchanges.keys())

    def validate_api_credentials(
        self,
        exchange_name: str,
        api_key: str,
        api_secret: str,
        api_passphrase: str | None = None
    ) -> dict[str, Any]:
        """Validate API credentials for an exchange.

        Args:
            exchange_name: Name of the exchange
            api_key: API key
            api_secret: API secret
            api_passphrase: API passphrase (required for some exchanges)

        Returns:
            Dictionary with validation results
        """
        exchange_info = self.get_exchange_info(exchange_name)
        if exchange_info is None:
            return {
                "valid": False,
                "error": f"Unsupported exchange: {exchange_name}"
            }

        # Check if passphrase is required but not provided
        if exchange_info.requires_passphrase and not api_passphrase:
            return {
                "valid": False,
                "error": f"API passphrase required for {exchange_name}"
            }

        # In a real implementation, you would make an actual API call to validate credentials
        # For now, we'll just check that the credentials are not empty
        if not api_key or not api_secret:
            return {
                "valid": False,
                "error": "API key and secret are required"
            }

        return {
            "valid": True,
            "message": "API credentials validation passed"
        }

    def get_exchange_status(self, exchange_name: str) -> dict[str, Any]:
        """Get the status of an exchange.

        Args:
            exchange_name: Name of the exchange

        Returns:
            Dictionary with exchange status information
        """
        exchange_info = self.get_exchange_info(exchange_name)
        if exchange_info is None:
            return {
                "status": "error",
                "error": f"Unsupported exchange: {exchange_name}"
            }

        try:
            # Make a simple API call to check if the exchange is accessible
            response = requests.get(f"{exchange_info.api_base_url}/api/v3/ping", timeout=5)

            if response.status_code == 200:
                return {
                    "status": "online",
                    "exchange": exchange_name,
                    "api_base_url": exchange_info.api_base_url
                }
            else:
                return {
                    "status": "offline",
                    "exchange": exchange_name,
                    "error": f"API returned status code {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "offline",
                "exchange": exchange_name,
                "error": f"Network error: {e}"
            }
        except Exception as e:
            return {
                "status": "error",
                "exchange": exchange_name,
                "error": f"Unexpected error: {e}"
            }
