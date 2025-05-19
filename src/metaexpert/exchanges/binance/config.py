"""Config for Binance exchange APIs."""

import os

from dotenv_vault import load_dotenv  # type: ignore

_ = load_dotenv()

# Binance
BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET")
BINANCE_BASE_URL: str = os.getenv("BINANCE_BASE_URL")

# Spot trading
BINANCE_SPOT_PACKAGE: str = "binance-connector"
BINANCE_SPOT_PACKAGE_VERSION: str = "3.12.0"
BINANCE_SPOT_MODULE: str = "binance.spot"
BINANCE_SPOT_WS_BASE_URL: str = "wss://stream.binance.com"
BINANCE_SPOT_WS_PORT: list[int] = [9443, 443]

# Futures trading
BINANCE_FUTURES_PACKAGE: str = "binance-futures-connector"
BINANCE_FUTURES_PACKAGE_VERSION: str = "0.0.0"
BINANCE_FUTURES_MODULE_USDT_M: str = "binance.um_futures"
BINANCE_FUTURES_MODULE_COIN_M: str = "binance.cm_futures"
BINANCE_FUTURES_WS_BASE_URL: str = "wss://fstream.binance.com"
BINANCE_FUTURES_WS_PORT: list[int] = []

# Contract types for futures trading
BINANCE_CONTRACT_USDT_M = "usdt-m"  # USDT-M Futures /fapi/*
BINANCE_CONTRACT_COIN_M = "coin-m"  # COIN-M Delivery /dapi/*
