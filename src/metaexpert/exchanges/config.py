import os

from dotenv_vault import load_dotenv  # type: ignore

_ = load_dotenv()

# Binance
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")

BINANCE_PACKAGE_SPOT = "binance-connector"
BINANCE_PACKAGE_FUTURES = "binance-futures-connector"

BINANCE_MODULE_SPOT = "binance.spot"
BINANCE_MODULE_FUTURES = "binance.cm_futures"

# Bybit
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
BYBIT_BASE_URL = os.getenv("BYBIT_BASE_URL")
