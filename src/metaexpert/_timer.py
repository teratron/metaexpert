import asyncio
import time

from metaexpert.logger import Logger, get_logger


class Timer:
    def __init__(self, interval: int = 1000) -> None:
        self._interval: float = interval / 1000.0  # Convert milliseconds to seconds
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._is_running: bool = False
        self.logger: Logger = get_logger(__name__)

    async def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()
        # print(f"Таймер с интервалом {self._interval:.1f} секунд запущен.")
        self.logger.debug("Timer with interval %.1f seconds started.", self._interval)

        while self._is_running:
            await asyncio.sleep(self._interval)
            self._elapsed_time += self._interval
            # print(f"Таймер с интервалом {self._interval:.1f} секунд: прошло {self._elapsed_time:.1f} секунд")
            self.logger.debug(
                "Timer with interval %.1f seconds: elapsed time %.1f seconds.",
                self._interval,
                self._elapsed_time,
            )

    def stop(self) -> None:
        if self._is_running:
            self._is_running = False
            # print(
            #     f"Таймер с интервалом {self._interval:.1f} секунд остановлен. Общее время: {self._elapsed_time:.1f} секунд"
            # )
            self.logger.debug(
                "Timer with interval %.1f seconds stopped. Total time: %.1f seconds.",
                self._interval,
                self._elapsed_time,
            )
