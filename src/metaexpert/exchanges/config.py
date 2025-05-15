"""Configuration for exchange APIs."""

import os

from dotenv_vault import load_dotenv  # type: ignore

_ = load_dotenv()

# Binance
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")

BINANCE_SPOT_PACKAGE = "binance-connector"
BINANCE_SPOT_MODULE = "binance.spot"

BINANCE_FUTURES_PACKAGE = "binance-futures-connector"
BINANCE_FUTURES_MODULE_USDT_M = "binance.um_futures"
BINANCE_FUTURES_MODULE_COIN_M = "binance.cm_futures"

# Contract types for futures trading
BINANCE_CONTRACT_USDT_M = "usdt-m"  # USDT-M Futures /fapi/*
BINANCE_CONTRACT_COIN_M = "coin-m"  # COIN-M Delivery /dapi/*

CONTRACT_TYPE_USDT_M = "usdt_m"  # USDT-M Futures (USDT/BUSD margined contracts)
CONTRACT_TYPE_COIN_M = "coin_m"  # COIN-M Futures (Coin margined contracts)

# Default contract type
DEFAULT_CONTRACT_TYPE = CONTRACT_TYPE_USDT_M

# Bybit
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
BYBIT_BASE_URL = os.getenv("BYBIT_BASE_URL")
