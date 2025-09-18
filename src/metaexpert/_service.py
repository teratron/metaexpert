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

            # Core Trading Parameters
            symbol: str | set[str] | None = None,
            timeframe: str | set[str] | None = None,
            *,
            lookback_bars: int = 100,
            warmup_bars: int = 0,

            # Strategy Metadata
            strategy_id: int = 42,
            strategy_name: str | None = None,
            comment: str | None = None,

            # Risk & Position Sizing
            leverage: int = 10,
            max_drawdown_pct: float = 0.2,
            daily_loss_limit: float = 1000.0,
            size_type: str = "risk_based", # Position sizing: 'fixed_base', 'fixed_quote', 'percent_equity', 'risk_based'
            size_value: float = 1.5,
            max_position_size_quote: float = 50000.0,

            # Trade Parameters
            stop_loss_pct: float = 2.0,
            take_profit_pct: float = 4.0,
            trailing_stop_pct: float = 1.0,
            trailing_activation_pct: float = 2.0,
            breakeven_pct: float = 1.5,
            slippage_pct: float = 0.1,
            max_spread_pct: float = 0.1,

            # Portfolio Management
            max_open_positions: int = 3,
            max_positions_per_symbol: int = 1,

            # Entry Filters
            trade_hours: list[int] | None = None,
            allowed_days: list[int] | None = None,
            min_volume: int = 1000000,
            volatility_filter: bool = True,
            trend_filter: bool = True
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | set[str] | None): Symbol of the trading pair.
            timeframe (str | set[str] | None): Time frame for the trading data.
            strategy_id (int): Magic number. Used to identify the expert. Defaults to 0.
            strategy_name (str | None): The name of the expert.
            size_value (float): The number of lots for trading. Defaults to 0.01.
            stop_loss_pct (float): Stop loss value. Defaults to 0.0.
            take_profit_pct (float): Take profit value. Defaults to 0.0.
            trailing_stop_pct (float): Trailing stop value. Defaults to 0.0.
            slippage_pct (float): Slippage value. Defaults to 0.0.
            max_open_positions (int): Number of positions to manage. Defaults to 5.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
        """
        self.symbol = symbol
        self.timeframe = Timeframe.get_period_from(timeframe)
        self.strategy_id = strategy_id
        self.strategy_name = strategy_name
        self.size_value = size_value
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.trailing_stop_pct = trailing_stop_pct
        self.slippage_pct = slippage_pct
        self.max_open_positions = max_open_positions

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

            while Process.ON_TIMER.check_instance():
                timer = Process.ON_TIMER.pop_instance()
                if timer is not None:
                    logger.debug("Stopping timer...")
                    timer.stop()

            while Process.ON_BAR.check_instance():
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
        """Decorator for bar event handling.

        Args:
            timeframe (str): Time frame for the bar. Defaults to "1h".

        Returns:
            Callable: Decorated function that handles bar events.
        """
        if not isinstance(timeframe, str):
            logger.error("Timeframe must be a string, got %s", type(timeframe).__name__)
            raise TypeError("Timeframe must be a string")

        def outer(func: Callable[[str], Coroutine[Any, Any, None]]) -> Callable[[str], Coroutine[Any, Any, None]]:
            async def inner(rates: str = "tram-pam-pam") -> None:
                bar = Bar(timeframe=timeframe, callback=func, args=(rates,))
                Process.ON_BAR.push_instance(bar)
                await bar.start()

            return inner

        return outer

    @staticmethod
    def on_timer(interval: float = 60) -> Callable[[Callable[[], None]], Callable[[], Coroutine[Any, Any, None]]]:
        """Decorator for timer-based event handling.

        Args:
            interval (float): Interval in seconds for the timer. Defaults to 60 s.

        Returns:
            Callable: Decorated function that executes at specified intervals.
        """
        if interval <= 0:
            logger.error("Interval must be greater than 0, got %d", interval)
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
