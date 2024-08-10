import os
import sys
import json
from dotenv_vault import load_dotenv
from logger import getLogger
from _binance import query_status, query_account, query_testnet

logger = getLogger()

if __name__ == "__main__":
    if not query_status():
        logger.error("Binance is not available")
        sys.exit(1)

    load_dotenv()
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")

    account = query_account(BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL)
    print(account)

    query_testnet(BINANCE_BASE_URL)
