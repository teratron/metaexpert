"""Config for Bybit exchange APIs."""

import os

from dotenv import load_dotenv  # type: ignore

_ = load_dotenv()

# Bybit
BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET", "")
BYBIT_BASE_URL: str = os.getenv("BYBIT_BASE_URL", "")

# WebSocket public stream:

# Mainnet:

# Spot:
BYBIT_SPOT_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/spot"

# USDT, USDC perpetual & USDT Futures:
BYBIT_LINEAR_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/linear"

# Inverse contract:
BYBIT_INVERSE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/inverse"

# Spread trading:
BYBIT_SPREAD_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/spread"

# USDT/USDC Options:
BYBIT_OPTION_WS_BASE_URL: str = "wss://stream.bybit.com/v5/public/option"

# Testnet:

# Spot:
BYBIT_SPOT_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/spot"

# USDT,USDC perpetual & USDT Futures:
BYBIT_LINEAR_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/linear"

# Inverse contract:
BYBIT_INVERSE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/inverse"

# Spread trading:
BYBIT_SPREAD_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/spread"

# USDT/USDC Options:
BYBIT_OPTION_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/public/option"

# WebSocket private stream:

# Mainnet:
BYBIT_PRIVATE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/private"

# Testnet:
BYBIT_PRIVATE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/private"

# WebSocket Order Entry:

# Mainnet:
BYBIT_TRADE_WS_BASE_URL: str = "wss://stream.bybit.com/v5/trade"  # Spread trading is not supported

# Testnet:
BYBIT_TRADE_WS_TESTNET_URL: str = "wss://stream-testnet.bybit.com/v5/trade"  # Spread trading is not supported
