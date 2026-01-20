import unittest
from unittest.mock import MagicMock, patch

from metaexpert.exchanges.kraken import Adapter
from metaexpert.core.market_type import MarketType


class TestKrakenAdapter(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"

    @patch("metaexpert.exchanges.kraken.install_package")
    @patch("metaexpert.exchanges.kraken.import_module")
    def test_spot_client_creation(self, mock_import_module, mock_install_package):
        mock_spot_client = MagicMock()
        mock_import_module.return_value.SpotClient = mock_spot_client

        adapter = Adapter()
        adapter.testnet = False
        adapter.market_type = MarketType.SPOT
        adapter.api_key = self.api_key
        adapter.api_secret = self.api_secret


        client = adapter._create_client()

        mock_install_package.assert_called_with("python-kraken-sdk")
        mock_import_module.assert_called_with("kraken.spot")
        mock_spot_client.assert_called_with(key=self.api_key, secret=self.api_secret)
        self.assertIsInstance(client, MagicMock)

    @patch("metaexpert.exchanges.kraken.install_package")
    @patch("metaexpert.exchanges.kraken.import_module")
    def test_futures_client_creation(self, mock_import_module, mock_install_package):
        mock_futures_user = MagicMock()
        mock_import_module.return_value.User = mock_futures_user

        adapter = Adapter()
        adapter.testnet = True
        adapter.market_type = MarketType.FUTURES
        adapter.api_key = self.api_key
        adapter.api_secret = self.api_secret

        client = adapter._create_client()

        mock_install_package.assert_called_with("python-kraken-sdk")
        mock_import_module.assert_called_with("kraken.futures")
        mock_futures_user.assert_called_with(
            key=self.api_key, secret=self.api_secret, sandbox=True
        )
        self.assertIsInstance(client, MagicMock)

    def test_unsupported_market_type(self):
        adapter = Adapter()
        adapter.testnet = False
        adapter.market_type = "unsupported"
        adapter.api_key = self.api_key
        adapter.api_secret = self.api_secret

        with self.assertRaises(ValueError):
            adapter._create_client()


if __name__ == "__main__":
    unittest.main()
