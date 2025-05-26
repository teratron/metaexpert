from typing import Any, Callable

from metaexpert._timeframe import Timeframe
from metaexpert._timer import Timer
from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger

logger: Logger = get_logger(APP_NAME)


class Service:
    """Expert trading system service.

    This class handles the initialization and management of the trading system's events.
    It provides decorators for various events such as initialization, deinitialization,
    trading, transactions, ticks, bars, timers, and book events.
    """
    symbol: str | set[str] | None
    timeframe: str | set[Timeframe] | None
    shift: int
    magic: int
    name: str | None

    # def __init__(self, name: str) -> None:
    #     self.logger: Logger = get_logger(name)

    def on_init(
            self,
            symbol: str | set[str] | None = None,
            timeframe: str | set[str] | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | set[str] | None): Symbol of the trading pair.
            timeframe (str | set[str] | None): Time frame for the trading data.
            shift (int): A shift relative to the current bar on which the expert is traded. Defaults to 0.
            magic (int): Magic number. Used to identify the expert. Defaults to 0.
            name (str | None): The name of the expert.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
        """
        self.symbol = symbol
        self.timeframe = Timeframe.get_period_from(timeframe)
        self.shift = shift
        self.magic = magic
        self.name = name

        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], Callable]) -> Callable:  # InitStatus:
            def inner(*args, **kwargs) -> None:
                # self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)
                logger.debug("Initializing...")
                func(*args, **kwargs)

            return inner  # InitStatus.INIT_SUCCEEDED

        return outer

    def on_deinit(self, func: Callable[[str], None]) -> Callable:
        def inner(*, reason: str = "+++") -> None:
            logger.debug("Deinitializing...")
            func(reason)

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    def on_tick(self, func: Callable) -> Callable:
        def inner(*args, **kwargs) -> None:
            func(*args, **kwargs)

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    @staticmethod
    def on_bar(timeframe: str = "1h") -> Callable:
        def outer(
                # func: Callable[[tuple[Any, ...], dict[str, Any]], None],
                func: Callable,
                # ) -> Callable[[Any, str], None]:
        ) -> Callable:
            async def inner(rates: str = "tram-pam-pam") -> None:
                func(rates)
                print(timeframe, rates)

            return inner

        return outer

    @staticmethod
    def on_timer(interval: int = 1000) -> Callable:
        """Decorator for timer-based event handling.

        Args:
            interval (int): Interval in milliseconds for the timer. Defaults to 1000 ms.

        Returns:
            Callable: Decorated function that executes at specified intervals.
        """

        if interval <= 0:
            raise ValueError("Interval must be greater than 0")

        def outer(func: Callable) -> Callable:
            timer = Timer(interval=interval, callback=func)

            async def inner() -> None:
                await timer.start()

            return inner

        return outer

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_transaction(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_book(symbol: str | set[str] | None = None) -> Callable:
        """Decorator for book event handling.
        Args:
            symbol (str | None): Symbol of the trading pair. Defaults to None.
        Returns:
            Callable: Decorated function that handles book events.
        """
        if symbol is None:
            raise ValueError("Symbol must be provided")
        if isinstance(symbol, str):
            symbol = {symbol}
        if not isinstance(symbol, set):
            raise TypeError("Symbol must be a string or a set of strings")

        def outer(func: Callable) -> Callable:
            def inner() -> None:
                func()

            return inner

        return outer

    @staticmethod
    def on_tester(func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_tester_init(func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_tester_deinit(func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_tester_pass(self, func: Callable) -> Callable:
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
