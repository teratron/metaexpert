"""Config for Bybit exchange APIs."""

import os

from dotenv_vault import load_dotenv  # type: ignore

_ = load_dotenv()

# Bybit
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
BYBIT_BASE_URL = os.getenv("BYBIT_BASE_URL")
