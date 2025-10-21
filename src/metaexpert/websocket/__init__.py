"""WebSocket client with MetaLogger integration."""

import asyncio
import json

import websockets

from metaexpert.logger import BoundLogger, get_logger


class WebSocketClient:
    def __init__(
        self,
        url: str,
        name: str = "ws",
        reconnect_delay: int = 5,
    ):
        self.url = url
        self.name = name
        self.reconnect_delay = reconnect_delay
        self.ws = None
        self.running = False
        self.logger: BoundLogger = get_logger("WebSocketClient")

    async def connect(self):
        while True:
            try:
                async with websockets.connect(
                    self.url, ping_interval=20, ping_timeout=10
                ) as ws:
                    self.ws = ws
                    self.logger.info("Connected to {url}", url=self.url, name=self.name)
                    await self.on_open()
                    async for message in ws:
                        await self.on_message(message)
            except Exception as e:
                self.logger.error("Connection error", error=str(e), name=self.name)
                await self.on_close()
                await asyncio.sleep(self.reconnect_delay)

    async def send(self, message: dict):
        if self.ws:
            await self.ws.send(json.dumps(message))

    async def on_open(self):
        """Override in subclass."""
        pass

    async def on_message(self, message: str | bytes):
        """Override in subclass."""
        pass

    async def on_close(self):
        """Override in subclass."""
        pass
