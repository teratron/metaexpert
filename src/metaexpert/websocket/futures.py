from threading import Thread

from metaexpert.websocket.spot import WebSocketClient

if __name__ == "__main__":
    # Thread(target=WebSocketClient, args=("wss://fstream.binance.com/ws/btcusdt@aggTrade",)).start()
    Thread(target=WebSocketClient, args=("wss://fstream.binance.com/ws/btcusdt@kline_1m",)).start()
    # Thread(
    #     target=WebSocketClient,
    #     args=("wss://fstream.binance.com/stream?streams=ethusdt@trade/ethusdt@kline_1m",)
    # ).start()
    # Thread(target=WebSocketClient, args=("wss://fstream.binance.com/ws/ethusdt@depth",)).start()
