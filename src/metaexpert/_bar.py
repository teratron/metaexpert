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
        self.__start_time: float = 0.0
        self.__elapsed_time: float = 0.0
        self.__is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self.__is_running = True
        self.__start_time = time.time()
        self.logger.debug("Bar with timeframe %s started.", self.timeframe)

        while self.__is_running:
            await asyncio.sleep(7)
            self.__elapsed_time += 7
            self.func(*self.args)

    def stop(self) -> None:
        if self.__is_running:
            self.__is_running = False
            self.logger.debug(
                "Bar with timeframe %s stopped. Total time: %.1f seconds.",
                self.timeframe,
                self.__elapsed_time,
            )
