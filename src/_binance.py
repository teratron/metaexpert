"""Binance API
"""
from binance.spot import Spot
from logger import getLogger

logger = getLogger(__name__)


def query_status() -> bool:
    try:
        if Spot().system_status()["status"] == 0:
            logger.info("System status normal")
            return True
    except (ConnectionError, Exception) as e:
        logger.error(e)
    return False


def query_account(api_key, api_secret, base_url="https://testnet.binance.vision") -> dict:
    return Spot(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url,
    ).account()


def query_testnet(base_url="https://testnet.binance.vision") -> None:
    client = Spot(base_url=base_url)
    logger.info(f"Check server time test {client.time()}")
