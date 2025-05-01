from metaexpert.api import Exchange


class BinanceStock(Exchange):
    """Implementation for the Binance exchange."""
    def __init__(self, api_key: str = None, api_secret: str = None):
        """Initializes the BinanceStock class.

        Args:
            api_key (str, optional): The API key for Binance. Defaults to None.
            api_secret (str, optional): The API secret for Binance. Defaults to None.
        """
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self._client = None

    def _get_client(self):
        """Lazy initializes and returns the Binance Spot client."""
        if self._client is None:
            try:
                # Import happens only when the client is needed
                from binance.spot import Spot as Client
            except ImportError:
                raise ImportError("Please install binance-connector: pip install binance-connector")

            if not self.api_key or not self.api_secret:
                # Initialize without authentication for public data access if needed
                # Or raise an error if keys are strictly required for intended operations
                # For get_balance, keys are usually required.
                raise ValueError("API key and secret are required for Binance operations like get_balance.")
            self._client = Client(key=self.api_key, secret=self.api_secret)
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
        client = self._get_client()
        try:
            # Example: Fetch account information which includes balances
            # Adjust the specific API call based on binance-connector documentation
            # if account() is not the correct method or requires different parameters.
            account_info = client.account()
            # Process account_info to extract relevant balance data
            # This is a placeholder; the actual structure depends on the API response
            balances = {item['asset']: item['free'] for item in account_info.get('balances', []) if float(item['free']) > 0}
            return balances
        except Exception as e:
            # Catch specific exceptions from the library if possible
            raise RuntimeError(f"Failed to get Binance balance: {e}")
