import asyncio
import time
from typing import Callable

from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger


class Timer:
    def __init__(self, interval: int = 1000, callback: Callable | None = None) -> None:
        self.interval: float = interval / 1000.0  # Convert milliseconds to seconds
        self.func: Callable = callback if callback is not None else lambda: None
        self.__start_time: float = 0.0
        self.__elapsed_time: float = 0.0
        self.__is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self.__is_running = True
        self.__start_time = time.time()
        self.logger.debug("Timer with interval %.1f seconds started.", self.interval)

        while self.__is_running:
            await asyncio.sleep(self.interval)
            self.__elapsed_time += self.interval
            self.func()

    def stop(self) -> None:
        if self.__is_running:
            self.__is_running = False
            self.logger.debug(
                "Timer with interval %.1f seconds stopped. Total time: %.1f seconds.",
                self.interval,
                self.__elapsed_time,
            )
