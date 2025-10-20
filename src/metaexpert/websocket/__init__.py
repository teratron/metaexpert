""""""

import asyncio
import json
import logging

import websockets

logger = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(self, url: str, name: str = "ws", reconnect_delay: int = 5):
        self.url = url
        self.name = name
        self.reconnect_delay = reconnect_delay
        self.ws = None
        self.running = False

    async def connect(self):
        while True:
            try:
                async with websockets.connect(
                    self.url, ping_interval=20, ping_timeout=10
                ) as ws:
                    self.ws = ws
                    logger.info(f"[{self.name}] Connected to {self.url}")
                    await self.on_open()
                    async for message in ws:
                        await self.on_message(message)
            except Exception as e:
                logger.error(f"[{self.name}] Connection error: {e}")
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
