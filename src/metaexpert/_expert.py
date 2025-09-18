from dataclasses import dataclass
from datetime import datetime

from metaexpert._timeframe import Timeframe


@dataclass
class Expert:
    # Core Trading Parameters
    symbol: str | set[str] | None
    timeframe: Timeframe | None
    lookback_bars: int
    warmup_bars: int

    # Strategy Metadata
    strategy_id: int
    strategy_name: str | None
    comment: str | None

    # Risk & Position Sizing
    leverage: int
    max_drawdown_pct: float
    daily_loss_limit: float
    size_type: str
    size_value: float
    max_position_size_quote: float

    # Trade Parameters
    stop_loss_pct: float
    take_profit_pct: float
    trailing_stop_pct: float
    trailing_activation_pct: float
    breakeven_pct: float
    slippage_pct: float
    max_spread_pct: float

    # Portfolio Management
    max_open_positions: int
    max_positions_per_symbol: int

    # Entry Filters
    trade_hours: set[int] | None
    allowed_days: set[int] | None
    min_volume: int
    volatility_filter: bool
    trend_filter: bool

    _label: str | None

    _lots_min: float
    _lots_max: float
    _lots_step: float

    _long_time: datetime
    _long_positions: int
    _long_profit: float
    _long_lots: float
    _short_time: datetime
    _short_positions: int
    _short_profit: float
    _short_lots: float
    _digits: int
    _digits_format: str
    _point: float

    def __init__(self):
        pass

    # @property
    # def strategy_id(self) -> int:
    #     return self._magic
    #
    # @strategy_id.setter
    # def strategy_id(self, value: int) -> None:
    #     self._magic = value
    #
    # @property
    # def comment(self) -> str:
    #     return self.__comment
    #
    # @comment.setter
    # def comment(self, value: str) -> None:
    #     self.__comment = value + f"Magic number: {self._magic}"


class Position:
    def __init__(self, symbol: str, lots: float, price: float, sl: float, tp: float):
        self.symbol = symbol
        self.lots = lots
        self.price = price
        self.sl = sl
        self.tp = tp

    def __repr__(self):
        return f"Position(symbol={self.symbol}, lots={self.lots}, price={self.price}, sl={self.sl}, tp={self.tp})"


class Order:
    def __init__(self, symbol: str, lots: float, price: float, sl: float, tp: float):
        self.symbol = symbol
        self.lots = lots
        self.price = price
        self.sl = sl
        self.tp = tp

    def __repr__(self):
        return f"Order(symbol={self.symbol}, lots={self.lots}, price={self.price}, sl={self.sl}, tp={self.tp})"
