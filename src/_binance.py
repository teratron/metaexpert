"""Binance API
"""
#from typing import override

import pandas
from binance.spot import Spot
from _logger import getLogger

logger = getLogger("binance")


def new_spot(api_key, api_secret, base_url="https://testnet.binance.vision") -> Spot:
    return Spot(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url,
    )


def query_status() -> bool:
    try:
        status = Spot().system_status()
        if status["status"] == 0:
            logger.info(f"System status {status['msg']}")
            return True
    except ConnectionError as error:
        logger.error(error)
    return False


def query_account(spot: Spot) -> dict:
    return spot.account()


# @override
# def query_account(api_key, api_secret, base_url="https://testnet.binance.vision") -> dict:
#     return Spot(
#         api_key=api_key,
#         api_secret=api_secret,
#         base_url=base_url,
#     ).account()


def query_testnet(base_url="https://testnet.binance.vision") -> None:
    logger.info(f"Check server time test {Spot(base_url=base_url).time()['serverTime']}")


def query_quote_asset_list(quote_asset_symbol):
    symbol_dataframe = pandas.DataFrame(Spot().exchange_info()["symbols"])
    # print(symbol_dataframe)
    quote_symbol_dataframe = symbol_dataframe.loc[symbol_dataframe["quoteAsset"] == quote_asset_symbol]
    quote_symbol_dataframe = quote_symbol_dataframe.loc[quote_symbol_dataframe["status"] == "TRADING"]
    return quote_symbol_dataframe


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
