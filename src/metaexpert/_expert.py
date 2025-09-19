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

    # Internal State
    _label: str | None = None
    _lots_min: float = 0.0
    _lots_max: float = 0.0
    _lots_step: float = 0.0
    _long_time: datetime | None = None
    _long_positions: int = 0
    _long_profit: float = 0.0
    _long_lots: float = 0.0
    _short_time: datetime | None = None
    _short_positions: int = 0
    _short_profit: float = 0.0
    _short_lots: float = 0.0
    _digits: int = 0
    _digits_format: str | None = None
    _point: float = 0.0
