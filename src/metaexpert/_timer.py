import asyncio
import time
from typing import Callable

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger


class Timer:
    def __init__(self, interval: float, callback: Callable | None = None) -> None:
        self.interval: float = interval
        self.func: Callable = callback if callback is not None else lambda: None
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        self.logger.debug("Timer with interval %.1f seconds started.", self.interval)

        while self._is_running:
            await asyncio.sleep(self.interval)
            self._elapsed_time += self.interval
            self.func()

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            self.logger.debug(
                "Timer with interval %.1f seconds stopped. Total time: %.1f seconds.",
                self.interval,
                self._elapsed_time,
            )
