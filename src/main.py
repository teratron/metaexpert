import os
import sys
import json
from dotenv_vault import load_dotenv
from _logger import getLogger
from _binance import new_spot, query_status, query_testnet, query_quote_asset_list, get_candlestick_data

logger = getLogger()

if __name__ == "__main__":
    if not query_status():
        logger.error("Binance is not available")
        sys.exit(1)

    load_dotenv()
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")

    spot = new_spot(BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL)
    account = spot.account()
    print(account)

    query_testnet(BINANCE_BASE_URL)

    candlesticks = get_candlestick_data("BTCUSDT", "1h", 3)
    print(candlesticks)

    dataframe = query_quote_asset_list("BTC")
    print(dataframe)
