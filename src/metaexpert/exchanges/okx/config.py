"""Config for OKX exchange APIs."""

# Spot trading
SPOT_PACKAGE: str = "okx-connector"
SPOT_PACKAGE_VERSION: str = "1.0.0"
SPOT_MODULE: str = "okx.spot"
SPOT_WS_BASE_URL: str = "wss://ws.okx.com:843/ws/v5/public"

# Futures trading
FUTURES_PACKAGE: str = "okx-connector"
FUTURES_PACKAGE_VERSION: str = "1.0.0"
FUTURES_MODULE_LINEAR: str = "okx.futures.linear"
FUTURES_MODULE_INVERSE: str = "okx.futures.inverse"
FUTURES_WS_BASE_URL: str = "wss://ws.okx.com:8443/ws/v5/public"

# Swap trading
SWAP_PACKAGE: str = "okx-connector"
SWAP_PACKAGE_VERSION: str = "1.0.0"
SWAP_MODULE: str = "okx.swap"
SWAP_WS_BASE_URL: str = "wss://ws.okx.com:8443/ws/v5/public"

# Options trading
OPTION_PACKAGE: str = "okx-connector"
OPTION_PACKAGE_VERSION: str = "1.0.0"
OPTION_MODULE: str = "okx.option"
OPTION_WS_BASE_URL: str = "wss://ws.okx.com:8443/ws/v5/public"

# Testnet URLs
SPOT_WS_TESTNET_URL: str = "wss://wspap.okx.com:8443/ws/v5/public"
FUTURES_WS_TESTNET_URL: str = "wss://wspap.okx.com:8443/ws/v5/public"
SWAP_WS_TESTNET_URL: str = "wss://wspap.okx.com:8443/ws/v5/public"
OPTION_WS_TESTNET_URL: str = "wss://wspap.okx.com:8443/ws/v5/public"
