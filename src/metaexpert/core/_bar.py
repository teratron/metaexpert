import asyncio
import time
from collections.abc import Callable
from logging import Logger

from metaexpert.config import APP_NAME
from metaexpert.logger import get_logger


class Bar:
    def __init__(
        self,
        timeframe: str = "1h",
        callback: Callable | None = None,
        args: tuple[dict, ...] = (),
    ) -> None:
        self._timeframe: str = timeframe
        self._func: Callable = callback if callback is not None else lambda: None
        self._args: tuple[dict, ...] = args
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger(APP_NAME)

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        self.logger.debug("Bar with timeframe %s started.", self._timeframe)

        while self._is_running:
            await asyncio.sleep(7)
            self._elapsed_time += 7
            self._func(*self._args)

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            self.logger.debug(
                "Bar with timeframe %s stopped. Total time: %.1f seconds.",
                self._timeframe,
                self._elapsed_time,
            )

    @property
    def timeframe(self) -> str:
        return self._timeframe

    @timeframe.setter
    def timeframe(self, value: str) -> None:
        if not isinstance(value, str):
            self.logger.error(
                "Timeframe must be a string, got %s", type(value).__name__
            )
            raise TypeError("Timeframe must be a string")
        self._timeframe = value
