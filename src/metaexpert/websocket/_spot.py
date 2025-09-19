import json
import time
import traceback
from threading import Thread

from websocket import WebSocket, WebSocketApp


class WebSocketClient(WebSocketApp):
    def __init__(self, url, *args, **kwargs) -> None:  #
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            **kwargs
        )
        self.params = args[0] if args else None
        self.run_forever(ping_interval=15, ping_timeout=10, reconnect=5)

    def start(self) -> None:
        """Start the WebSocket client."""
        print(f"Starting WebSocket client for {self.url}")
        self.run_forever()

    def on_open(self, ws: WebSocket) -> None:
        print(ws, "Websocket connection opened")
        if self.params and isinstance(self.params, list):
            ws.send(json.dumps({"op": "subscribe", "args": self.params}))

    def on_close(self, ws: WebSocket, status, message: str, *args, **kwargs) -> None:
        print(f"{ws} Websocket connection closed: {status} {message}")

    def on_error(self, ws: WebSocket, error: Exception) -> None:
        print(f"{ws} Websocket connection error: {error}")
        print(traceback.format_exc())

    def on_message(self, ws: WebSocket, message: str) -> None:
        print(f"{ws} Received message: {message}")


if __name__ == "__main__":
    # Thread(target=WebSocketClient, args=("wss://stream.binance.com:9443/ws/btcusdt@aggTrade",)).start()
    # Thread(
    #     target=WebSocketClient,
    #     args=("wss://stream.binance.com:9443/stream?streams=ethusdt@trade/ethusdt@kline_1m",)
    # ).start()
    # Thread(target=WebSocketClient, args=("wss://stream.binance.com:9443/ws/ethusdt@depth",)).start()

    Thread(
        target=WebSocketClient,
        args=("wss://stream.bybit.com/v5/public/spot", ["tickers.ADAUSDT", "orderbook.50.ADAUSDT"]),
        daemon=True
    ).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
