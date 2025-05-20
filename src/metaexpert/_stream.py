import traceback
from abc import ABC, abstractmethod

from websocket import WebSocketApp, WebSocket

from metaexpert import logger


class WebSocketClient(WebSocketApp, ABC):
    def __init__(self, *args, **kwargs) -> None:  #
        super().__init__(
            url=args[0],
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            **kwargs
        )
        self.run_forever(ping_interval=15, ping_timeout=10, reconnect=5)

    def on_open(self, ws: WebSocket) -> None:
        logger.debug("Websocket connection opened")

    def on_close(self, ws: WebSocket, status: int, message: str) -> None:
        logger.debug("Websocket connection closed: %d %s", status, message)

    def on_error(self, ws: WebSocket, error: Exception) -> None:
        logger.error("Websocket connection error: %s", error)
        logger.error(traceback.format_exc())

    @abstractmethod
    def on_message(self, ws: WebSocket, message: str) -> None:
        print(f"Received message: {message}")
