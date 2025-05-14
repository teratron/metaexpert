import asyncio
from typing import Any, Callable

from metaexpert._timeframe import Timeframe
from metaexpert.logger import Logger, get_logger


class Service:
    """Expert trading system service.

    This class handles the initialization and management of the trading system's events.
    It provides decorators for various events such as initialization, deinitialization,
    trading, transactions, ticks, bars, timers, and book events.
    """
    symbol: str | set[str] | None
    timeframe: str | set[str] | None
    shift: int
    magic: int
    name: str | None

    def __init__(self, name: str) -> None:
        self.logger: Logger = get_logger(name)

    def on_init(
            self,
            symbol: str | set[str] | None = None,
            timeframe: Timeframe | set[Timeframe] | str | set[str] | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | None): Symbol of the trading pair.
            timeframe (str | None): Time frame for the trading data.
            shift (int): A shift relative to the current bar on which the expert is traded. Defaults to 0.
            magic (int): Magic number. Used to identify the expert. Defaults to 0.
            name (str | None): The name of the expert.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
        """
        self.symbol = symbol
        self.timeframe: Timeframe | set[Timeframe] = timeframe
        self.shift = shift
        self.magic = magic
        self.name = name

        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], Callable]) -> Callable:  # InitStatus:
            def inner(*args, **kwargs) -> None:
                # self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)
                self.logger.debug("Initializing...")
                func(*args, **kwargs)

            return inner  # InitStatus.INIT_SUCCEEDED

        return outer

    def on_deinit(self, func: Callable[[str], None]) -> Callable:
        def inner(*, reason: str = "+++") -> None:
            self.logger.debug("Deinitializing...")
            func(reason)

        return inner

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_transaction(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    def on_tick(self, func: Callable) -> Callable:
        def inner(*args, **kwargs) -> None:
            # task = asyncio.create_task(func())
            # task
            func(*args, **kwargs)
            # await self.__tick()
            # task = asyncio.create_task(self.__tick())
            # await task
            # i = 3
            # while i > 0:
            #     func()
            #     print(self, " ", i)
            #     i -= 1
            # return func()

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    def on_bar(self, timeframe: str = "1h") -> Callable:
        def outer(
                func: Callable[[tuple[Any, ...], dict[str, Any]], None],
        ) -> Callable[[tuple[Any, ...], dict[str, Any]], None]:
            def inner(rate, *args, **kwargs) -> None:
                # rate: list = kwargs.get("rate")
                func(rate, *args, **kwargs)
                print(timeframe)

            return inner

            # async def async_inner(*args, **kwargs) -> None:
            #     await func(*args, **kwargs)
            #     print(time_frame)
            #
            # return async_inner

        return outer

    @staticmethod
    def on_timer(interval: int = 1000) -> Callable:
        """Decorator for timer-based event handling.

        Args:
            interval (int, optional): Time interval in milliseconds. Defaults to 1000.

        Returns:
            Callable: Decorated function that executes at specified intervals.
        """

        def outer(func: Callable) -> Callable:
            async def inner() -> None:
                await asyncio.sleep(interval / 1000.0)
                func()

            return inner

        return outer

    def on_book(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    # @property
    # def magic(self) -> int:
    #     return self._magic
    #
    # @magic.setter
    # def magic(self, value: int) -> None:
    #     self._magic = value
    #
    # @property
    # def comment(self) -> str:
    #     return self.__comment
    #
    # @comment.setter
    # def comment(self, value: str) -> None:
    #     self.__comment = value + f"Magic number: {self._magic}"
