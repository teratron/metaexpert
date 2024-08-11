"""Binance API
"""
#from typing import override
import sys
import pandas
from binance.spot import Spot


class API:
    from _logger import getLogger

    __log = getLogger(__name__)
    __default_url = "https://testnet.binance.vision"

    def __init__(self, api_key=None, api_secret=None, base_url=__default_url) -> None:
        if not API.query_status():
            API.__log.error("Binance is not available")
            sys.exit(1)

        self.api_key = api_key
        self.api_secret = api_secret
        self.spot = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    # Проверка статуса Binance
    @staticmethod
    def query_status() -> bool:
        try:
            status = Spot().system_status()
            if status["status"] == 0:
                API.__log.info(f"System status {status['msg']}")
                return True
        except ConnectionError as error:
            API.__log.error(error)
        return False

    # Получение данных аккаунта с Binance
    def query_account(self) -> dict:
        return self.spot.account()

    # Проверка состояния соединения с Binance
    def query_testnet(self) -> None:
        self.__log.info(f"Check server time test {self.spot.time()['serverTime']}")

    # Получение списка биржевых пар
    def query_quote_asset_list(self, quote_asset_symbol: str) -> pandas.DataFrame:
        symbol_dataframe = pandas.DataFrame(self.spot.exchange_info()["symbols"])
        # print(symbol_dataframe)
        quote_symbol_dataframe = symbol_dataframe.loc[symbol_dataframe["quoteAsset"] == quote_asset_symbol]
        quote_symbol_dataframe = quote_symbol_dataframe.loc[quote_symbol_dataframe["status"] == "TRADING"]
        return quote_symbol_dataframe


# Получение данных свечей по инструменту
def get_candlestick_data(symbol, timeframe, period) -> list:
    raw_data = Spot().klines(symbol=symbol, interval=timeframe, limit=period)
    converted_data = []

    for candle in raw_data:
        converted_data.append({
            "time": int(candle[0]),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
            "close_time": candle[6],
            "quote_asset_volume": float(candle[7]),
            "number_of_trades": int(candle[8]),
            "taker_buy_base_asset_volume": float(candle[9]),
            "taker_buy_quote_asset_volume": float(candle[10])
        })

    return converted_data


def make_trade_with_params(spot: Spot, **kwargs):
    print("Making trade with params")
    try:
        response = spot.new_order(**kwargs)
        return response
    except ConnectionRefusedError as error:
        logger.error(f"New order error: {error}")
