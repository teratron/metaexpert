"""Trading Expert Template for the MetaExpert library.
Generated automatically by 'metaexpert new' command.

This file is the starting point for creating your own trading strategy.
Fill in the parameters and add your logic to the corresponding event handlers.
"""

import os

from dotenv import load_dotenv

from metaexpert import MetaExpert

# Load environment variables
_ = load_dotenv()

expert = MetaExpert(
    # --- Required Parameters ---
    exchange="bybit",  # Supported: 'binance', 'bybit', 'okx', 'bitget', 'kucoin'
    # --- API Credentials (required for live mode) ---
    api_key=os.getenv("BYBIT_API_KEY"),  # User to provide API key
    api_secret=os.getenv("BYBIT_API_SECRET"),  # User to provide secret key
    api_passphrase=None,  # Required only for OKX/KuCoin
    # --- Connection Settings ---
    subaccount=None,  # For Bybit multi-account (optional)
    base_url=os.getenv("BYBIT_BASE_URL"),  # Custom API URL (optional)
    testnet=False,  # True to use exchange testnet
    proxy=None,  # Proxy settings: dict like {"http": "...", "https": "..."} (optional)
    # --- Market & Trading Mode ---
    market_type="futures",  # 'spot', 'futures', 'options' (note: 'options' only on Binance, OKX)
    contract_type="linear",  # Only for futures: 'linear' (USDT-M) or 'inverse' (COIN-M)
    margin_mode="isolated",  # Only for futures: 'isolated' or 'cross' (ignored for spot)
    position_mode="hedge",
    # 'hedge' (two-way) or 'oneway' (one-way) — Binance futures (required for Binance; ignored on other exchanges)
    # --- Logging Configuration ---
    log_level=os.getenv("LOG_LEVEL", "INFO"),  # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    log_file="expert.log",  # Main log file
    trade_log_file="trades.log",  # Trade execution log
    error_log_file="errors.log",  # Error-specific log
    log_to_console=True,  # Print logs to console
    # --- Advanced System Settings ---
    rate_limit=1200,  # Max requests per minute (RPM). Varies by exchange and API tier.
    enable_metrics=True,  # Enable performance metrics
    persist_state=True,  # Persist state between runs
    state_file="state.json",  # State persistence file (relative to working directory)
)


@expert.on_init(
    # --- Core Trading Parameters ---
    symbol="BTCUSDT",  # Trading symbols (str or list[str])
    timeframe="1h",  # Primary timeframe: '1m','5m','15m','1h','4h','1d',...
    lookback_bars=100,  # Number of historical bars to fetch for analysis
    warmup_bars=0,  # Skip initial bars to initialize indicators (optional, 0 = no warmup)
    # --- Strategy Metadata ---
    strategy_id=1002,  # Unique ID for order tagging
    strategy_name="RSI Strategy",  # Display name
    comment="rsi_strategy",  # Order comment (max 32 chars Binance, 36 Bybit)
    # --- Risk & Position Sizing ---
    leverage=10,  # Leverage (verify per-symbol limits; ignored for spot, validated via API)
    max_drawdown_pct=0.2,  # Max drawdown from peak equity (0.2 = 20%)
    daily_loss_limit=1000,
    # Daily loss limit in auto-detected settlement currency (e.g., USDT for linear, BTC for inverse, auto-determined)
    size_type="risk_based",  # Position sizing: 'fixed_base', 'fixed_quote', 'percent_equity', 'risk_based'
    size_value=1.5,
    # Size value: fixed_base (e.g., 0.01 BTC), fixed_quote (e.g., 1000 USDT), percent_equity (e.g., 0.01 = 1%), risk_based (e.g., 1.5% risk per trade)
    max_position_size_quote=50000.0,  # Max position size in quote currency
    # --- Trade Parameters ---
    stop_loss_pct=2.0,  # Stop-Loss % from entry
    take_profit_pct=4.0,  # Take-Profit % from entry
    trailing_stop_pct=1.0,  # Trailing stop distance (%)
    trailing_activation_pct=2.0,  # Activate after X% profit
    breakeven_pct=1.5,  # Move SL to breakeven after X% profit
    slippage_pct=0.1,  # Expected slippage %
    max_spread_pct=0.1,  # Max allowed spread %
    # --- Portfolio Management ---
    max_open_positions=3,  # Max total open positions
    max_positions_per_symbol=1,  # Max positions per symbol
    # --- Entry Filters ---
    trade_hours=[9, 10, 11, 15],  # Trade only during these UTC hours
    allowed_days=[1, 2, 3, 4, 5],  # Trade only these days (1=Mon, 7=Sun)
    min_volume=10000,  # Min volume in settlement_currency
    volatility_filter=True,  # Enable volatility filter (implement inside)
    trend_filter=True,  # Enable trend filter (implement inside)
)
def init() -> None:
    """Called once at expert startup. Initialize indicators or load data here."""
    print("*** RSI Strategy Initialized ***")


@expert.on_deinit
def deinit(reason) -> None:
    """Called when expert stops. Clean up resources if needed.

    Args:
        reason: Shutdown reason (e.g., "user_stop", "error")
    """
    print(f"*** RSI Strategy Deinitialized: {reason} ***")


@expert.on_tick
def tick(rates) -> None:
    """Called on every price tick. Use for HFT, real-time adjustments.

    Args:
        rates: Real-time market data (ask, bid, last, etc.)
    """
    pass


@expert.on_bar(
    timeframe="1h",  # Bar timeframe. Defaults to init timeframe if omitted. Use for multi-timeframe strategies.
)
def bar(rates) -> None:
    """Called when a new bar closes. Implement core strategy logic here.

    RSI trading logic:
    1. Extract closing prices from historical data
    2. Calculate RSI indicator (typically 14-period)
    3. Generate buy signals when RSI crosses above 30 (oversold)
    4. Generate sell signals when RSI crosses below 70 (overbought)
    5. Execute trades based on the signals

    Args:
        rates: OHLCV data for the completed bar
    """
    print("*** RSI Bar Processing ***", rates)

    # RSI trading logic placeholder
    # Uncomment these imports when implementing actual RSI calculation
    # import numpy as np
    # import talib

    # Example implementation (commented out):
    # close = np.array([rate.close for rate in rates])
    # rsi = talib.RSI(close, timeperiod=14)
    # print(rsi)


@expert.on_timer(
    interval=1.0  # Interval in seconds (float)
)
def timer() -> None:
    """Called periodically. Useful for monitoring, heartbeat, non-market logic."""
    print("*** RSI Timer Tick ***")


@expert.on_order
def order(order) -> None:
    """Called when order status changes.

    Args:
        order: Order object (symbol, side, status, price, qty, etc.)
    """
    print("*** RSI Order Update ***", order)


@expert.on_position
def position(pos) -> None:
    """Called when position state changes. Ideal for dynamic risk management.

    Args:
        pos: Position object (symbol, size, entry_price, pnl, etc.)
    """
    print("*** RSI Position Update ***", pos)


@expert.on_transaction
def transaction(request, result) -> None:
    """Called when a transaction completes (e.g., order fill).

    Args:
        request: Original request details
        result: Execution result (status, filled_qty, avg_price, fees, etc.)
    """
    print("*** RSI Transaction Completed ***")


@expert.on_book
def book(orderbook) -> None:
    """Called when order book changes. Useful for market making or liquidity analysis.

    Args:
        orderbook: Object with symbol, bids [(price, qty)], asks [(price, qty)]
    """
    print("*** RSI Order Book Update ***", orderbook)


@expert.on_error
def error(err) -> None:
    """Called on error (API, network, logic). Implement recovery or alerting here.

    Args:
        err: Error object or message
    """
    print("*** RSI Error ***", err)


@expert.on_account
def account(acc) -> None:
    """Called when account state updates (balance, equity, margin).

    Args:
        acc: Account object (balance, currency, equity, timestamp, etc.)
    """
    print("*** RSI Account Update ***", acc)


def main() -> None:
    """Main entry point. Starts the trading expert."""
    expert.run(
        trade_mode="paper",  # 'paper' or 'live' or 'backtest'
        backtest_start="2024-01-01",  # YYYY-MM-DD
        backtest_end="2025-08-31",  # YYYY-MM-DD
        initial_capital=10000,
        # Starting capital in settlement_currency (used in 'paper' and 'backtest' modes; ignored in 'live')
    )


if __name__ == "__main__":
    main()
