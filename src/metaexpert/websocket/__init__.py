import json
import traceback
from abc import ABC, abstractmethod

from websocket import WebSocketApp

from metaexpert.logger import get_logger

# Get the logger instance
logger = get_logger("metaexpert.websocket")


class WebSocketClient(WebSocketApp, ABC):
    def __init__(self, url: str, **kwargs) -> None:
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            **kwargs
        )
        self.run_forever(ping_interval=15, ping_timeout=10, reconnect=5)

    @abstractmethod
    def on_open(self, ws: WebSocketApp) -> None:
        logger.debug(f"{ws} Websocket connection opened")

    @abstractmethod
    def on_close(self, ws: WebSocketApp, status: int, message: str) -> None:
        logger.debug(f"{ws} Websocket connection closed: {status} {message}")

    @abstractmethod
    def on_error(self, ws: WebSocketApp, error: Exception) -> None:
        logger.error(f"{ws} Websocket connection error: {error}")
        logger.error(traceback.format_exc())

    @abstractmethod
    def on_message(self, ws: WebSocketApp, message: str) -> None:
        logger.debug(f"{ws} Received message: {message}")
        data = json.loads(message)
        logger.debug(f"Parsed message: {data}")
