from typing import Any, Callable, Coroutine

from metaexpert import Process
from metaexpert._bar import Bar
from metaexpert._expert import Expert
from metaexpert._timeframe import Timeframe
from metaexpert._timer import Timer
from metaexpert.config import APP_NAME
from metaexpert.logger import Logger, get_logger

logger: Logger = get_logger(APP_NAME)


class Service(Expert):
    """Expert trading system service.

    This class handles the initialization and management of the trading system's events.
    It provides decorators for various events such as initialization, deinitialization,
    trading, transactions, ticks, bars, timers, and book events.
    """

    def on_init(
            self,
            symbol: str | set[str] | None = None,
            timeframe: str | set[str] | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None,
            lots: float = 0.01,
            stop_loss: float = 0.0,
            take_profit: float = 0.0,
            trailing_stop: float = 0.0,
            slippage: float = 0.0,
            positions: int = 5
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
        self.lots = lots
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.trailing_stop = trailing_stop
        self.slippage = slippage
        self.positions = positions

        # super().__init__()

        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], Callable]) -> Callable:  # InitStatus:
            def inner(*args, **kwargs) -> None:
                # self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)
                logger.debug("Initializing...")
                func(*args, **kwargs)

            return inner  # InitStatus.INIT_SUCCEEDED

        return outer

    @staticmethod
    def on_deinit(func: Callable[[str], None]) -> Callable:
        def inner(reason: str = "+++", *args, **kwargs) -> None:
            logger.debug("Deinitializing...")
            func(reason)

            while Process.ON_TIMER:
                timer = Process.ON_TIMER.pop_instance()
                if timer is not None:
                    logger.debug("Stopping timer...")
                    timer.stop()

            while Process.ON_BAR:
                bar = Process.ON_BAR.pop_instance()
                if bar is not None:
                    logger.debug("Stopping bar...")
                    bar.stop()

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    @staticmethod
    def on_tick(func: Callable) -> Callable:
        def inner(rates: str = "tic-tac-toe") -> None:
            func(rates)

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]
    @staticmethod
    def on_bar(timeframe: str = "1h") -> Callable:
        if not isinstance(timeframe, str):
            raise TypeError("Timeframe must be a string")

        def outer(func: Callable[[str], Coroutine[Any, Any, None]]) -> Callable[[str], Coroutine[Any, Any, None]]:
            async def inner(rates: str = "tram-pam-pam") -> None:
                bar = Bar(timeframe=timeframe, callback=func, args=(rates,))
                Process.ON_BAR.push_instance(bar)
                await bar.start()

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

        def outer(func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
            async def inner() -> None:
                timer = Timer(interval=interval, callback=func)
                Process.ON_TIMER.push_instance(timer)
                await timer.start()

            return inner

        return outer

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_transaction(self, func: Callable) -> Callable:
        def inner(request: str = "", result: str = "") -> None:
            func(request, result)

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
    def on_tester(func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_tester_pass(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner
