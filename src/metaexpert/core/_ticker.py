import asyncio
import time
from collections.abc import Callable

from metaexpert.logger import MetaLogger as Logger, get_logger


class Ticker:
    def __init__(self, callback: Callable | None = None) -> None:
        self._func: Callable = callback if callback is not None else lambda: None
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger("Ticker")

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        self.logger.debug("Ticker started.")

        while self._is_running:
            await asyncio.sleep(7)
            self._elapsed_time += 7
            self._func()

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            self.logger.debug(
                "Total time: %.1f seconds.",
                self._elapsed_time,
            )
