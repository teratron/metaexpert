# import logging
import time

# from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient


# config_logging(logging, logging.DEBUG)


def on_close(_):
    print("Do custom stuff when connection is closed")


def message_handler(_, message):
    print(message)


if __name__ == "__main__":
    my_client = SpotWebsocketAPIClient(on_message=message_handler, on_close=on_close)

    my_client.ticker(symbol="BNBBUSD", type="FULL")

    time.sleep(2)

    my_client.ticker(symbols=["BNBBUSD", "BTCUSDT"], type="MINI", windowSize="2h")

    time.sleep(2)

    print("closing ws connection")
    my_client.stop()
