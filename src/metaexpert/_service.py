from collections.abc import Callable, Coroutine
from typing import Any

from metaexpert import Process
from metaexpert._bar import Bar
from metaexpert._expert import Expert
from metaexpert._size_type import SizeType
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
        symbol: str | None = None,
        timeframe: str | None = None,
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
        size_type: str = "risk_based",
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
        trade_hours: set[int] | None = None,
        allowed_days: set[int] | None = None,
        min_volume: int = 10000,
        volatility_filter: bool = True,
        trend_filter: bool = True
    ) -> Callable[[Callable[[], None]], Callable[[], None]]:
        """Decorator for initialization event handling.

        Args:
            symbol (str | None): Trading symbols (e.g., "BTCUSDT", "ETHUSDT"). Defaults to "BTCUSDT".
            timeframe (str | None): Time frame for trading data (e.g., "1h", "1m"). Defaults to "1h".
            lookback_bars (int): Number of historical bars to fetch for analysis. Defaults to 100.
            warmup_bars (int): Skip initial bars to initialize indicators. Defaults to 0.
            strategy_id (int): Unique ID for order tagging. Defaults to 1001.
            strategy_name (str | None): Display name of the strategy. Defaults to "My Strategy".
            comment (str | None): Order comment (max 32 chars for Binance, 36 for Bybit). Defaults to "my_strategy".
            leverage (int): Leverage for margin trading (ignored for spot). Defaults to 10.
            max_drawdown_pct (float): Max drawdown from peak equity (0.2 = 20%). Defaults to 0.2.
            daily_loss_limit (float): Daily loss limit in settlement currency (auto-detected). Defaults to 1000.0.
            size_type (str): Position sizing method ('fixed_base', 'fixed_quote', 'percent_equity', 'risk_based'). Defaults to "risk_based".
            size_value (float): Size value based on size_type (e.g., 1.5% for risk_based). Defaults to 1.5.
            max_position_size_quote (float): Max position size in quote currency. Defaults to 50000.0.
            stop_loss_pct (float): Stop-loss % from entry. Defaults to 2.0.
            take_profit_pct (float): Take-profit % from entry. Defaults to 4.0.
            trailing_stop_pct (float): Trailing stop distance (%). Defaults to 1.0.
            trailing_activation_pct (float): Activate trailing stop after X% profit. Defaults to 2.0.
            breakeven_pct (float): Move SL to breakeven after X% profit. Defaults to 1.5.
            slippage_pct (float): Expected slippage (%). Defaults to 0.1.
            max_spread_pct (float): Max allowed spread (%). Defaults to 0.1.
            max_open_positions (int): Max total open positions. Defaults to 3.
            max_positions_per_symbol (int): Max positions per symbol. Defaults to 1.
            trade_hours (set[int] | None): Trade only during these UTC hours. Defaults to {9, 10, 11, 15}.
            allowed_days (set[int] | None): Trade only these days (1=Mon, 7=Sun). Defaults to {1, 2, 3, 4, 5}.
            min_volume (int): Min volume in settlement currency. Defaults to 1000000.
            volatility_filter (bool): Enable volatility filter (implement inside). Defaults to True.
            trend_filter (bool): Enable trend filter (implement inside). Defaults to True.

        Returns:
            Callable: Decorated function that handles the initialization event.
        """
        super().__init__(
            symbol=symbol,
            timeframe=Timeframe.get_period_from(timeframe),
            lookback_bars=lookback_bars,
            warmup_bars=warmup_bars,
            strategy_id=strategy_id,
            strategy_name=strategy_name,
            comment=comment,
            leverage=leverage,
            max_drawdown_pct=max_drawdown_pct,
            daily_loss_limit=daily_loss_limit,
            size_type=SizeType.get_size_type_from(size_type),
            size_value=size_value,
            max_position_size_quote=max_position_size_quote,
            stop_loss_pct=stop_loss_pct,
            take_profit_pct=take_profit_pct,
            trailing_stop_pct=trailing_stop_pct,
            trailing_activation_pct=trailing_activation_pct,
            breakeven_pct=breakeven_pct,
            slippage_pct=slippage_pct,
            max_spread_pct=max_spread_pct,
            max_open_positions=max_open_positions,
            max_positions_per_symbol=max_positions_per_symbol,
            trade_hours=trade_hours,
            allowed_days=allowed_days,
            min_volume=min_volume,
            volatility_filter=volatility_filter,
            trend_filter=trend_filter,
        )

        def outer(func: Callable[[], None]) -> Callable[[], None]:
            def inner() -> None:
                logger.debug("Initializing strategy: %s", self.strategy_name)
                func()

            return inner

        return outer

    @staticmethod
    def on_deinit(func: Callable[[str], None]) -> Callable:
        """Decorator for deinitialization event handling.

        Args:
            func (Callable): Function to handle deinitialization.

        Returns:
            Callable: Decorated function that handles the deinitialization event.
        """
        def inner(reason: str = "user_stop") -> None:
            logger.debug("Deinitializing with reason: %s", reason)
            func(reason)

            while Process.ON_TIMER.check_instance():
                timer = Process.ON_TIMER.pop_instance()
                if timer is not None:
                    logger.debug("Stopping timer...")
                    if hasattr(timer, "stop") and callable(getattr(timer, "stop", None)):
                        timer.stop()

            while Process.ON_BAR.check_instance():
                bar = Process.ON_BAR.pop_instance()
                if bar is not None:
                    logger.debug("Stopping bar...")
                    if hasattr(bar, "stop") and callable(getattr(bar, "stop", None)):
                        bar.stop()

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    @staticmethod
    def on_tick(func: Callable) -> Callable:
        def inner(rates: dict) -> None:
            func(rates)

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]
    @staticmethod
    def on_bar(timeframe: str = "1h") -> Callable[[Callable[[Any], Coroutine[Any, Any, None]]], Callable[[Any], Coroutine[Any, Any, None]]]:
        """Decorator for bar event handling.

        Args:
            timeframe (str): Time frame for the bar. Defaults to "1h".

        Returns:
            Callable: Decorated function that handles bar events.
        """
        def outer(func: Callable[[Any], Coroutine[Any, Any, None]]) -> Callable[[Any], Coroutine[Any, Any, None]]:
            async def inner(rates: dict) -> None:
                bar = Bar(timeframe=timeframe, callback=func, args=(rates,))
                Process.ON_BAR.push_instance(bar)
                await bar.start()

            return inner

        return outer

    @staticmethod
    def on_timer(interval: int = 60) -> Callable[[Callable[[], None]], Callable[[], Coroutine[Any, Any, None]]]:
        """Decorator for timer-based event handling.

        Args:
            interval (int): Interval in seconds for the timer. Defaults to 60 s.

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

    @staticmethod
    def on_order(func: Callable[[dict], None]) -> Callable:
        """Decorator for order event handling.

        Args:
            func (Callable): Function to handle order status changes.

        Returns:
            Callable: Decorated function that handles order events.
        """
        def inner(order: dict) -> None:
            func(order)

        return inner

    @staticmethod
    def on_position(func: Callable[[dict], None]) -> Callable:
        """Decorator for position event handling.

        Args:
            func (Callable): Function to handle position state changes.

        Returns:
            Callable: Decorated function that handles position events.
        """
        def inner(pos: dict) -> None:
            func(pos)

        return inner

    @staticmethod
    def on_transaction(func: Callable[[dict, dict], None]) -> Callable:
        """Decorator for transaction event handling.

        Args:
            func (Callable): Function to handle transaction completions.

        Returns:
            Callable: Decorated function that handles transaction events.
        """
        def inner(request: dict, result: dict) -> None:
            func(request, result)

        return inner

    @staticmethod
    def on_book(func: Callable[[dict], None]) -> Callable:
        """Decorator for book event handling.

        Args:
            func (Callable): Function to handle order book changes.

        Returns:
            Callable: Decorated function that handles book events.
        """
        def inner(orderbook: dict) -> None:
            func(orderbook)

        return inner

    @staticmethod
    def on_error(func: Callable[[Exception], None]) -> Callable:
        """Decorator for error event handling.

        Args:
            func (Callable): Function to handle errors (API, network, logic).

        Returns:
            Callable: Decorated function that handles error events.
        """
        def inner(err: Exception) -> None:
            func(err)

        return inner

    @staticmethod
    def on_account(func: Callable[[dict], None]) -> Callable:
        """Decorator for account event handling.

        Args:
            func (Callable): Function to handle account state updates.

        Returns:
            Callable: Decorated function that handles account events.
        """
        def inner(acc: dict) -> None:
            func(acc)

        return inner

    @staticmethod
    def on_backtest_init(func: Callable[[], None]) -> Callable:
        """Decorator for backtest initialization event handling.

        Args:
            func (Callable): Function to handle backtest initialization.

        Returns:
            Callable: Decorated function that handles backtest init events.
        """
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_backtest_deinit(func: Callable[[], None]) -> Callable:
        """Decorator for backtest deinitialization event handling.

        Args:
            func (Callable): Function to handle backtest deinitialization.

        Returns:
            Callable: Decorated function that handles backtest deinit events.
        """
        def inner() -> None:
            func()

        return inner

    @staticmethod
    def on_backtest(func: Callable[[], float]) -> Callable[[], float]:
        """Decorator for backtest per-bar event handling.

        Args:
            func (Callable): Function to handle backtest bar events.

        Returns:
            Callable: Decorated function that handles backtest events.
        """
        def inner() -> float:
            return func()

        return inner

    @staticmethod
    def on_backtest_pass(func: Callable[[], None]) -> Callable:
        """Decorator for backtest per-pass event handling.

        Args:
            func (Callable): Function to handle backtest per-pass events.

        Returns:
            Callable: Decorated function that handles backtest pass events.
        """
        def inner() -> None:
            func()

        return inner
