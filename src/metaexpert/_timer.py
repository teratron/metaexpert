import asyncio
import time

from metaexpert import APP_NAME
from metaexpert.logger import Logger, get_logger


class Timer:
    def __init__(self, interval: int = 1000) -> None:
        self._interval: float = interval / 1000.0  # Convert milliseconds to seconds
        self.__start_time: float = 0.0
        self.__elapsed_time: float = 0.0
        self.__is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self.__is_running = True
        self.__start_time = time.time()
        self.logger.debug("Timer with interval %.1f seconds started.", self._interval)

        while self.__is_running:
            await asyncio.sleep(self._interval)
            self.__elapsed_time += self._interval
            self.logger.debug(
                "Timer with interval %.1f seconds: elapsed time %.1f seconds.",
                self._interval,
                self.__elapsed_time,
            )

    def stop(self) -> None:
        if self.__is_running:
            self.__is_running = False
            self.logger.debug(
                "Timer with interval %.1f seconds stopped. Total time: %.1f seconds.",
                self._interval,
                self.__elapsed_time,
            )

    # async def run(self, *a) -> None:
    #     """Основная функция для запуска таймеров."""
    #     await asyncio.gather(*a)
    #     #asyncio.run(async )
