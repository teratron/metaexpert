# Data Model: Crypto Trading Library

## Overview

This document defines the core data models for the MetaExpert cryptocurrency trading library, following the unified interface requirements while supporting multiple exchanges and trading types.

## Core Entities

### Exchange
Represents a cryptocurrency exchange (Binance, Bybit, etc.) with its own API endpoints, rate limits, and features.

**Attributes:**
- `id` (str): Unique identifier for the exchange
- `name` (str): Display name of the exchange
- `api_endpoint` (str): Base URL for the exchange API
- `web_socket_endpoint` (str): WebSocket endpoint for real-time data
- `rate_limit` (int): Maximum requests per time window
- `supported_trading_types` (list[str]): Trading types supported by this exchange (spot, futures, options, margin)
- `supported_futures_types` (list[str]): Futures contract types (usd_m, coin_m)
- `status` (str): Exchange status (online, maintenance, offline)
- `api_key` (str): API key for authentication (encrypted)
- `api_secret` (str): API secret for authentication (encrypted)

**Relationships:**
- One-to-many with TradingAccount
- One-to-many with TradingInstrument

### TradingInstrument
Represents a tradeable asset pair (e.g., BTCUSDT) with specific properties and trading rules.

**Attributes:**
- `symbol` (str): Trading pair symbol (e.g., BTCUSDT)
- `base_currency` (str): Base currency of the pair (e.g., BTC)
- `quote_currency` (str): Quote currency of the pair (e.g., USDT)
- `min_order_size` (Decimal): Minimum order size allowed
- `max_order_size` (Decimal): Maximum order size allowed
- `price_precision` (int): Number of decimal places for price
- `quantity_precision` (int): Number of decimal places for quantity
- `tick_size` (Decimal): Minimum price increment
- `exchange_id` (str): Reference to the exchange where this instrument is traded
- `trading_types` (list[str]): Supported trading types for this instrument
- `contract_specifications` (dict): Exchange-specific contract specifications

**Relationships:**
- Many-to-one with Exchange
- One-to-many with Order

### Order
Represents a trading instruction (buy/sell) with parameters like type, size, price, stop-loss, take-profit, etc.

**Attributes:**
- `order_id` (str): Unique order identifier
- `exchange_order_id` (str): Exchange-specific order identifier
- `instrument` (TradingInstrument): The instrument being traded
- `side` (str): Order side (buy, sell)
- `order_type` (str): Type of order (market, limit, stop, stop_limit, trailing_stop)
- `quantity` (Decimal): Quantity to buy/sell
- `price` (Decimal): Price for limit orders
- `stop_price` (Decimal): Price for stop orders
- `time_in_force` (str): Time in force (GTC, IOC, FOK, GTD)
- `status` (str): Order status (pending, filled, partial, cancelled, rejected)
- `created_at` (datetime): Order creation timestamp
- `updated_at` (datetime): Last update timestamp
- `stop_loss_price` (Decimal): Stop loss price
- `take_profit_price` (Decimal): Take profit price
- `trailing_stop_callback_rate` (Decimal): Trailing stop callback rate
- `trailing_stop_activation_price` (Decimal): Trailing stop activation price
- `trading_account_id` (str): Reference to the account placing the order

**Relationships:**
- Many-to-one with TradingInstrument
- Many-to-one with TradingAccount

### Position
Represents an open trading position with current value, profit/loss, and risk parameters.

**Attributes:**
- `position_id` (str): Unique position identifier
- `instrument` (TradingInstrument): The instrument held in the position
- `side` (str): Position side (long, short)
- `quantity` (Decimal): Quantity held
- `entry_price` (Decimal): Average entry price
- `current_price` (Decimal): Current market price
- `unrealized_pnl` (Decimal): Unrealized profit/loss
- `realized_pnl` (Decimal): Realized profit/loss
- `liquidation_price` (Decimal): Liquidation price for leveraged positions
- `leverage` (int): Leverage used for this position
- `margin_used` (Decimal): Margin used for this position
- `created_at` (datetime): Position creation timestamp
- `updated_at` (datetime): Last update timestamp
- `trading_account_id` (str): Reference to the account holding this position

**Relationships:**
- Many-to-one with TradingInstrument
- Many-to-one with TradingAccount

### TradingAccount
Represents a user's account on a specific exchange with balances, permissions, and configurations.

**Attributes:**
- `account_id` (str): Unique account identifier
- `user_id` (str): Reference to the user who owns this account
- `exchange_id` (str): Reference to the exchange
- `account_name` (str): Display name for the account
- `account_type` (str): Account type (spot, futures, margin, etc.)
- `permissions` (list[str]): Account permissions (read, trade, withdraw)
- `balance` (dict): Balance information keyed by currency
- `available_balance` (dict): Available balance for trading
- `used_balance` (dict): Balance currently in use (in orders/positions)
- `total_pnl` (Decimal): Total profit/loss
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp

**Relationships:**
- Many-to-one with Exchange
- One-to-many with Order
- One-to-many with Position

### TradingStrategy
Represents a trading strategy that can be executed using the library.

**Attributes:**
- `strategy_id` (str): Unique strategy identifier
- `name` (str): Strategy name
- `description` (str): Strategy description
- `parameters` (dict): Strategy parameters and configuration
- `risk_controls` (dict): Risk management settings (stop loss, take profit, etc.)
- `created_at` (datetime): Strategy creation timestamp
- `updated_at` (datetime): Last update timestamp
- `user_id` (str): Reference to the user who created this strategy

**Relationships:**
- One-to-many with StrategyExecution

### StrategyExecution
Represents a running instance of a trading strategy.

**Attributes:**
- `execution_id` (str): Unique execution identifier
- `strategy_id` (str): Reference to the strategy being executed
- `trading_account_id` (str): Reference to the account used for trading
- `status` (str): Execution status (running, paused, stopped)
- `start_time` (datetime): Execution start timestamp
- `end_time` (datetime): Execution end timestamp (if completed)
- `performance_metrics` (dict): Strategy performance metrics

**Relationships:**
- Many-to-one with TradingStrategy
- Many-to-one with TradingAccount

## Validation Rules

- All monetary values must be positive (except PnL which can be negative)
- Order quantities must be within instrument's min/max limits
- Order prices must be positive multiples of tick size
- Position leverage must not exceed exchange's maximum for that instrument
- Stop loss and take profit prices must be set appropriately relative to market price
- API keys and secrets must be encrypted at rest

## State Transitions

### Order State Transitions
- `pending` → `partial` (when partially filled)
- `pending` → `filled` (when fully filled)
- `pending` → `cancelled` (when cancelled by user)
- `pending` → `rejected` (when rejected by exchange)
- `partial` → `filled` (when remaining quantity filled)
- `partial` → `cancelled` (when partially filled order cancelled)

### Position State Transitions
- `open` → `closed` (when position closed through offsetting trade)
- `open` → `liquidated` (when liquidated due to margin requirements)

### StrategyExecution State Transitions
- `stopped` → `running` (when strategy execution starts)
- `running` → `paused` (when strategy execution is paused)
- `paused` → `running` (when strategy execution resumes)
- `running` → `stopped` (when strategy execution is stopped by user)
- `paused` → `stopped` (when strategy execution is stopped by user)

## Constraints

- An instrument must exist on an exchange before orders can be placed for it
- An order must reference a valid trading account
- A position must reference a valid trading account
- Order and position quantities must be positive
- Account balances must be updated after order execution
- Strategy executions must reference a valid strategy and trading account