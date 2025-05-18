from threading import Thread

from websocket import WebSocketApp, WebSocket


class WebSocketClient(WebSocketApp):
    def __init__(self, url, *args, **kwargs) -> None:  #
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            *args,
            **kwargs
        )
        self.keep_running = True
        # _run_forever_thread = Thread(target=self.run_forever)
        self.run_forever()

    # def run_forever(self):
    #     while self.keep_running:
    #         self.run_forever()

    def on_open(self, ws: WebSocket) -> None:
        print("Websocket connection opened")
        # self.run_forever()

    def on_close(self, ws: WebSocket, *args, **kwargs) -> None:
        print("Websocket connection closed")
        self.keep_running = False

        if self.on_close:
            self.on_close(ws, *args, **kwargs)

    def on_error(self, ws: WebSocket, error: Exception) -> None:
        print(f"Websocket connection error: {error}")
        # if self.on_error:
        #     self.on_error(ws, error)

    def on_message(self, ws: WebSocket, message: str) -> None:
        print(f"Received message: {message}")
        # if self.on_message:
        #     self.on_message(ws, message)


if __name__ == "__main__":
    # Thread(target=WebSocketClient, args=("wss://stream.binance.com:9443/ws/btcusdt@aggTrade",)).start()
    # Thread(
    #     target=WebSocketClient,
    #     args=("wss://stream.binance.com:9443/stream?streams=ethusdt@trade/ethusdt@kline_1m",)
    # ).start()
    Thread(target=WebSocketClient, args=("wss://stream.binance.com:9443/ws/ethusdt@depth",)).start()
