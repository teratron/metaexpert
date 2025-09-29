"""Config for Bybit exchange APIs."""


# Spot trading
SPOT_PACKAGE: str = "binance-connector"
SPOT_PACKAGE_VERSION: str = "3.12.0"
SPOT_MODULE: str = "binance.spot"
SPOT_WS_PORT: set[int] = {9443, 443}

# Futures trading
FUTURES_PACKAGE: str = "bybit-connector"
FUTURES_PACKAGE_VERSION: str = ""
FUTURES_MODULE_LINEAR: str = "binance.um_futures"  # USDT-M Futures /fapi/*
FUTURES_MODULE_INVERSE: str = "binance.cm_futures"  # COIN-M Delivery /dapi/*
FUTURES_WS_PORT: set[int] = {9443, 443}

# -----------------------------------------------------------------------------
# WEBSOCKET PUBLIC STREAM
# -----------------------------------------------------------------------------

# Mainnet:

# Spot:
SPOT_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/spot"

# USDT, USDC perpetual & USDT Futures:
LINEAR_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/linear"

# Inverse contract:
INVERSE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/inverse"

# Spread trading:
SPREAD_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/spread"

# USDT/USDC Options:
OPTION_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/option"

# Testnet:

# Spot:
SPOT_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/spot"

# USDT,USDC perpetual & USDT Futures:
LINEAR_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/linear"

# Inverse contract:
INVERSE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/inverse"

# Spread trading:
SPREAD_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/spread"

# USDT/USDC Options:
OPTION_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/option"

# -----------------------------------------------------------------------------
# WEBSOCKET PRIVATE STREAM
# -----------------------------------------------------------------------------

# Mainnet:
PRIVATE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/private"

# Testnet:
PRIVATE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/private"

# -----------------------------------------------------------------------------
# WEBSOCKET ORDER ENTRY
# -----------------------------------------------------------------------------

# Mainnet:
TRADE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/trade"  # Spread trading is not supported

# Testnet:
TRADE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/trade"  # Spread trading is not supported
