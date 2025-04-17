import argparse

from dotenv_vault import load_dotenv

from api.src import SpotAPI  # , get_candlestick_data, query_status, query_testnet, query_quote_asset_list
from arguments import parse_arguments
from logger import get_logger
from src.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL

if __name__ == "__main__":
    logger = get_logger()
    _ = load_dotenv()

    # Parse command line arguments
    args: argparse.Namespace = parse_arguments()

    spot = SpotAPI(BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL)
    account = spot.query_account()
    print(account)

    spot.query_testnet()

    candlesticks = spot.get_candlestick_data("BTCUSDT", "1m", 3)
    print(candlesticks)

    dataframe = spot.query_quote_asset_list("BTC")
    print(dataframe)
