import asyncio
import time
from typing import Callable

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger


class Bar:
    def __init__(self, timeframe: str = "1h", callback: Callable | None = None, args: tuple[str] = ()) -> None:
        self.timeframe: str = timeframe
        self.func: Callable = callback if callback is not None else lambda: None
        self.args: tuple[str] = args
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        self.logger.debug("Bar with timeframe %s started.", self.timeframe)

        # client = WebSocketClient("wss://fstream.binance.com/ws/btcusdt@kline_1m")
        # await client.start()

        while self._is_running:
            await asyncio.sleep(7)
            self._elapsed_time += 7
            self.func(*self.args)

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            self.logger.debug(
                "Bar with timeframe %s stopped. Total time: %.1f seconds.",
                self.timeframe,
                self._elapsed_time,
            )
