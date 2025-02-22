import os

from _binance import SpotAPI  # , get_candlestick_data, query_status, query_testnet, query_quote_asset_list

if __name__ == "__main__":
    from dotenv_vault import load_dotenv
    from _logger import getLogger

    _logger = getLogger()
    _ = load_dotenv()
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")

    spot = SpotAPI(BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL)
    account = spot.query_account()
    print(account)

    spot.query_testnet()

    candlesticks = spot.get_candlestick_data("BTCUSDT", "1h", 3)
    print(candlesticks)

    dataframe = spot.query_quote_asset_list("BTC")
    print(dataframe)
