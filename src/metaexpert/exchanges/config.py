"""Configuration for exchange APIs."""

from dotenv_vault import load_dotenv  # type: ignore

_ = load_dotenv()

# Contract types for futures trading
CONTRACT_TYPE_USDT_M = "usdt_m"  # USDT-M Futures (USDT/BUSD margined contracts)
CONTRACT_TYPE_COIN_M = "coin_m"  # COIN-M Futures (Coin margined contracts)

# Default contract type
DEFAULT_CONTRACT_TYPE = CONTRACT_TYPE_USDT_M
