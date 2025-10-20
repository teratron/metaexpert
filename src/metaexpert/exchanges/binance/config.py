"""Config for Binance exchange APIs."""

# Spot trading
SPOT_PACKAGE: str = "binance-connector"
SPOT_PACKAGE_VERSION: str = "3.12.0"
SPOT_MODULE: str = "binance.spot"
SPOT_WS_BASE_URL: str = "wss://stream.binance.com"
SPOT_WS_PORT: set[int] = {9443, 443}

# Futures trading
FUTURES_PACKAGE: str = "binance-futures-connector"
FUTURES_PACKAGE_VERSION: str = "4.1.0"
FUTURES_MODULE_LINEAR: str = "binance.um_futures"  # USDT-M Futures /fapi/*
FUTURES_MODULE_INVERSE: str = "binance.cm_futures"  # COIN-M Delivery /dapi/*
FUTURES_WS_BASE_URL: str = "wss://fstream.binance.com"
FUTURES_WS_PORT: set[int] = {9443, 443}
