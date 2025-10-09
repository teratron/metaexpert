# Data Model: MetaExpert Trading Library

## Core Entities

### MetaExpert
**Description:** Main class that encapsulates the trading logic, manages connections to exchanges, and handles event processing.
**Fields:**
- exchange: str - The cryptocurrency exchange to connect to (binance, bybit, okx, etc.)
- api_key: str | None - User's API key for authentication
- api_secret: str | None - User's secret key for authentication
- api_passphrase: str | None - Passphrase for specific exchanges (OKX/KuCoin)
- subaccount: str | None - For Bybit multi-account
- base_url: str | None - Custom API URL
- testnet: bool - Whether to use exchange testnet
- proxy: dict | None - Proxy settings as {http: "...", https: "..."}
- market_type: str - Market type ('spot', 'futures', 'options')
- contract_type: str - Contract type for futures ('linear' or 'inverse')
- margin_mode: str - Margin mode ('isolated' or 'cross')
- position_mode: str - Position mode ('hedge' or 'oneway')
- log_level: str - Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
- log_file: str - Main log file
- trade_log_file: str - Trade-specific log file
- error_log_file: str - Error-specific log file
- log_to_console: bool - Whether to log to console
- structured_logging: bool - Whether to use structured JSON logging
- async_logging: bool - Whether to use asynchronous logging
- rate_limit: int - Max requests per minute
- enable_metrics: bool - Whether to enable performance metrics
- persist_state: bool - Whether to persist state between runs
- state_file: str - State persistence file

**Relationships:**
- 1 MetaExpert → 1 Exchange (connection)
- 1 MetaExpert → * Strategy (configuration)
- 1 MetaExpert → * Order (placements)
- 1 MetaExpert → * Position (management)

### Exchange
**Description:** Represents a cryptocurrency exchange connection with specific parameters like API endpoints, rate limits, supported features, and authentication methods.
**Fields:**
- name: str - Exchange name (binance, bybit, okx, etc.)
- api_endpoints: dict - API endpoint URLs
- rate_limits: dict - Rate limit configurations
- supported_features: list - Features supported by the exchange
- authentication_methods: list - Authentication methods supported
- connection_status: str - Current connection status
- last_heartbeat: float - Timestamp of last successful communication

**Relationships:**
- 1 Exchange → * Account (for different users)
- 1 Exchange → * Order (on this exchange)
- 1 Exchange → * Trade (execution on this exchange)

### Strategy
**Description:** Defines the trading approach with parameters like symbol, timeframe, lookback periods, risk management settings, and position sizing rules. Includes performance metrics and evaluation criteria.
**Fields:**
- symbol: str - Trading symbol (e.g., 'BTCUSDT')
- timeframe: str - Primary timeframe ('1m','5m','15m','1h','4h','1d', etc.)
- lookback_bars: int - Number of historical bars to fetch for analysis
- lookback_time: str | None - Alternative time period ('1h','4h','1d','7d','30d')
- warmup_bars: int - Skip initial bars to initialize indicators (0 = no warmup)
- strategy_id: int - Unique ID for order tagging
- strategy_name: str - Display name
- comment: str - Order comment (max 32 chars Binance, 36 Bybit)
- leverage: int - Leverage (verify per-symbol limits; ignored for spot, validated via API)
- max_drawdown_pct: float - Max drawdown from peak equity (0.2 = 20%)
- daily_loss_limit: float - Daily loss limit in auto-detected settlement currency
- size_type: str - Position sizing ('fixed_base', 'fixed_quote', 'percent_equity', 'risk_based')
- size_value: float - Size value based on size_type
- max_position_size_quote: float - Max position size in quote currency
- stop_loss_pct: float - Stop-Loss % from entry
- take_profit_pct: float - Take-Profit % from entry
- trailing_stop_pct: float - Trailing stop distance %
- trailing_activation_pct: float - Activate after X% profit
- breakeven_pct: float - Move SL to breakeven after X% profit
- slippage_pct: float - Expected slippage %
- max_spread_pct: float - Max allowed spread %
- max_open_positions: int - Max total open positions
- max_positions_per_symbol: int - Max positions per symbol
- trade_hours: set - Trade only during these UTC hours
- allowed_days: set - Trade only these days (1=Mon, 7=Sun)
- min_volume: int - Min volume in settlement_currency
- volatility_filter: bool - Enable volatility filter
- trend_filter: bool - Enable trend filter
- performance_metrics: dict - Performance metrics (sharpe ratio, max drawdown, profit factor)
- backtesting_params: dict - Backtesting parameters (data sources, slippage models, commission calculations)
- optimization_params: dict - Optimization parameters (parameter ranges, optimization algorithms, fitness functions)
- sharing_perms: dict - Sharing/copying permissions

**Relationships:**
- 1 Strategy → * Order (orders placed by this strategy)
- 1 Strategy → * Position (positions managed by this strategy)
- 1 Strategy → * Trade (trades generated by this strategy)

### Order
**Description:** Represents a trading instruction (buy/sell) with parameters like type, size, price, stop-loss, take-profit, and status transitions.
**Fields:**
- order_id: str - Unique identifier for the order
- symbol: str - Trading symbol (e.g., 'BTCUSDT')
- side: str - Order side ('buy' or 'sell')
- type: str - Order type ('limit', 'market', 'stop', etc.)
- size: float - Order size in base currency
- price: float - Order price (None for market orders)
- stop_loss: float | None - Stop-loss price
- take_profit: float | None - Take-profit price
- status: str - Order status ('created', 'submitted', 'partially_filled', 'filled', 'cancelled', 'rejected')
- time_in_force: str - Time in force ('GTC', 'IOC', 'FOK', 'GTD')
- commission_fee: float - Commission/fee for the order
- cost_calculation: dict - Cost calculation details for different order types
- entry_time: float - Time when order was placed
- fill_time: float | None - Time when order was filled
- filled_size: float - Amount that has been filled
- avg_fill_price: float | None - Average fill price
- strategy_id: int - Strategy that placed this order

**Relationships:**
- 1 Order → 1 Strategy (strategy that placed it)
- 1 Order → 1 Exchange (exchange where it's placed)
- 1 Order → 0..1 Position (if it creates or modifies a position)

### Position
**Description:** Represents an open trading position with attributes like symbol, size, entry price, current value, profit/loss, and risk parameters.
**Fields:**
- position_id: str - Unique identifier for the position
- symbol: str - Trading symbol (e.g., 'BTCUSDT')
- size: float - Position size in base currency
- entry_price: float - Price at which position was opened
- current_price: float - Current market price
- current_value: float - Current value of the position
- pnl: float - Profit/loss in quote currency
- pnl_percentage: float - Profit/loss as percentage
- entry_time: float - Time when position was opened
- leverage: int - Leverage used for this position
- margin_used: float - Amount of margin used
- liquidation_price: float | None - Price at which position would be liquidated
- stop_loss: float | None - Stop-loss price
- take_profit: float | None - Take-profit price
- trailing_stop_distance: float | None - Trailing stop distance
- strategy_id: int - Strategy that created this position

**Relationships:**
- 1 Position → 1 Strategy (strategy that created it)
- 1 Position → 1 Exchange (on which it exists)
- * Order → 1 Position (orders that affect this position)

### Trade
**Description:** Represents an executed transaction with details like symbol, side, size, price, fees, and execution time.
**Fields:**
- trade_id: str - Unique identifier for the trade
- symbol: str - Trading symbol (e.g., 'BTCUSDT')
- side: str - Trade side ('buy' or 'sell')
- size: float - Trade size in base currency
- price: float - Execution price
- fees: float - Fees paid for the trade
- timestamp: float - Time of execution
- order_id: str - Order that generated this trade
- position_id: str | None - Position that this trade affects
- strategy_id: int - Strategy that executed this trade
- exchange: str - Exchange where the trade was executed

**Relationships:**
- 1 Trade → 1 Order (order that generated it)
- 1 Trade → 1 Position (position it affects)
- 1 Trade → 1 Strategy (strategy that executed it)
- 1 Trade → 1 Exchange (exchange where executed)

### Account
**Description:** Represents user account information including balance, equity, margin, and currency information.
**Fields:**
- account_id: str - Unique identifier for the account
- exchange: str - Exchange name
- balance: dict - Current balances by currency
- equity: float - Current equity (balance + unrealized PnL)
- margin: float - Current margin used
- available_margin: float - Available margin for new positions
- currency: str - Primary currency
- timestamp: float - Last update timestamp
- position_mode: str - Current position mode
- margin_mode: str - Current margin mode
- leverage: float - Current leverage setting

**Relationships:**
- 1 Account → * Position (open positions on this account)
- 1 Account → * Order (orders on this account)
- 1 Account → 1 Exchange (on this exchange)

## Validation Rules

### MetaExpert Validation
- exchange must be one of the supported exchanges (binance, bybit, okx, etc.)
- market_type must be 'spot', 'futures', or 'options'
- contract_type must be 'linear' or 'inverse' for futures, ignored for spot
- position_mode must be 'hedge' or 'oneway' (required for Binance futures)
- log_level must be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'

### Order Validation
- size must be positive
- price must be positive for limit orders
- status must be one of the defined order statuses
- stop_loss and take_profit must be valid prices if specified

### Strategy Validation
- symbol must be a valid trading pair format (e.g., 'BTCUSDT')
- leverage must be within exchange limits
- timeframes must be supported by the exchange
- daily_loss_limit must be non-negative
- max_drawdown_pct must be between 0 and 1

### Position Validation
- size must not be zero
- entry_price must be positive
- leverage must be within exchange limits

## State Transitions

### Order State Transitions
- created → submitted (when submitted to exchange)
- submitted → partially_filled (when partially filled)
- submitted → filled (when fully filled)
- submitted → cancelled (when cancelled by user)
- submitted → rejected (when rejected by exchange)
- partially_filled → filled (when remaining quantity filled)
- partially_filled → cancelled (when remaining quantity cancelled)

### Position State Transitions
- opened → open (position is active)
- open → closed (position is fully closed)
- open → liquidated (position is liquidated due to margin call)
- closed → reopened (new position in same direction)