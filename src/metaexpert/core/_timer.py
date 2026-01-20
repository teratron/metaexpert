import asyncio
import time
from collections.abc import Callable

from metaexpert.logger import MetaLogger as Logger, get_logger


class Timer:
    def __init__(self, interval: float, callback: Callable | None = None) -> None:
        self._interval: float = interval
        self._func: Callable = callback if callback is not None else lambda: None
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger(__name__).bind(
            component="Timer", interval=interval
        )

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        self.logger.debug("Timer with interval %.1f seconds started.", self._interval)

        while self._is_running:
            await asyncio.sleep(self._interval)
            self._elapsed_time += self._interval
            self._func()

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            self.logger.debug(
                "Timer with interval %.1f seconds stopped. Total time: %.1f seconds.",
                self._interval,
                self._elapsed_time,
            )

    @property
    def interval(self) -> float:
        return self._interval

    @interval.setter
    def interval(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            self.logger.error("Interval must be a number, got %s", type(value).__name__)
            raise TypeError("Interval must be a number")
        if value <= 0:
            self.logger.error("Interval must be greater than 0, got %d", value)
            raise ValueError("Interval must be greater than 0")
        self._interval = value
