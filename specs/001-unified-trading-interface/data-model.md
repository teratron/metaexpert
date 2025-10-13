# Data Model: Unified Trading Interface

**Feature**: MetaExpert Unified Trading Interface
**Date**: 2025-10-13

## Overview

This document defines the core data entities for the MetaExpert library, which will be implemented as Pydantic models. These models serve as the unified data contract for all information passed within the system, ensuring consistency across all supported exchanges.

## Core Entities

### ExchangeConnection
Represents a connection to a specific cryptocurrency exchange with API credentials and configuration.

**Fields**:
- `exchange_id`: str - Unique identifier for the exchange (binance, bybit, okx)
- `api_key`: str - API key credential (encrypted)
- `secret_key`: str - Secret key credential (encrypted)
- `passphrase`: Optional[str] - Passphrase for exchanges requiring it
- `testnet`: bool - Whether to use testnet environment
- `proxy_url`: Optional[str] - Proxy URL if required
- `rate_limit_config`: RateLimitConfig - Configuration for rate limiting

### TradingAccount
Represents a user's account on an exchange with balance information and permissions.

**Fields**:
- `account_id`: str - Unique identifier for the account
- `exchange_id`: str - Reference to the exchange
- `account_type`: AccountType - Enum (spot, futures, margin, options)
- `balances`: Dict[str, Balance] - Available and on-order balances by currency
- `positions`: List[Position] - Current positions (for futures/margin)
- `permissions`: List[str] - Account permissions (read, trade, withdrawal)

### Balance
Represents available and on-order balance for a specific currency.

**Fields**:
- `currency`: str - Currency code (e.g., BTC, USDT)
- `available`: float - Available balance for trading
- `on_order`: float - Balance currently on open orders
- `total`: float - Total balance (available + on_order)

### TradingStrategy
Encapsulates algorithmic trading logic with entry/exit conditions and risk parameters.

**Fields**:
- `strategy_id`: str - Unique identifier for the strategy
- `name`: str - Human-readable name
- `description`: str - Description of the strategy
- `exchange_id`: str - Exchange the strategy runs on
- `symbol`: str - Trading pair (e.g., BTCUSDT)
- `entry_conditions`: List[Condition] - Conditions to enter trades
- `exit_conditions`: List[Condition] - Conditions to exit trades
- `risk_params`: RiskParameters - Risk management configuration
- `status`: StrategyStatus - Current status (active, paused, stopped)
- `created_at`: datetime - Creation timestamp
- `updated_at`: datetime - Last update timestamp

### Order
Represents a trading order with type, size, price, and exchange-specific parameters.

**Fields**:
- `order_id`: str - Unique order identifier from exchange
- `client_order_id`: str - Client-assigned order ID
- `exchange_id`: str - Exchange where order is placed
- `symbol`: str - Trading pair (e.g., BTCUSDT)
- `side`: OrderSide - Enum (buy, sell)
- `order_type`: OrderType - Enum (market, limit, stop, etc.)
- `time_in_force`: TimeInForce - Enum (GTC, IOC, FOK, etc.)
- `quantity`: float - Order quantity
- `price`: Optional[float] - Price for limit orders
- `stop_price`: Optional[float] - Stop price for stop orders
- `status`: OrderStatus - Enum (new, partially_filled, filled, canceled, etc.)
- `filled_quantity`: float - Quantity filled
- `average_fill_price`: Optional[float] - Average fill price
- `fees`: List[Fee] - Trading fees associated with order
- `timestamp`: datetime - Order creation timestamp
- `update_timestamp`: datetime - Last status update timestamp

### Position
Represents an open trading position.

**Fields**:
- `position_id`: str - Unique position identifier
- `symbol`: str - Trading pair (e.g., BTCUSDT)
- `exchange_id`: str - Exchange where position exists
- `side`: PositionSide - Enum (long, short, net)
- `quantity`: float - Position size
- `entry_price`: float - Average entry price
- `current_price`: float - Current market price
- `unrealized_pnl`: float - Unrealized profit/loss
- `realized_pnl`: float - Realized profit/loss
- `margin_used`: float - Margin used for position
- `leverage`: float - Position leverage
- `timestamp`: datetime - Position creation timestamp

### Portfolio
Aggregates positions and balances across multiple exchanges to provide unified view.

**Fields**:
- `portfolio_id`: str - Unique portfolio identifier
- `name`: str - Portfolio name
- `total_balance`: float - Total balance in base currency
- `positions`: List[Position] - All positions across exchanges
- `balances`: Dict[str, Dict[str, float]] - Balances by exchange and currency
- `total_pnl`: float - Total profit/loss
- `daily_pnl`: float - Daily profit/loss
- `last_updated`: datetime - Timestamp of last update

### MarketData
Normalized market information from various exchanges including prices, volumes, and order books.

**Fields**:
- `symbol`: str - Trading pair (e.g., BTCUSDT)
- `exchange_id`: str - Source exchange
- `timestamp`: datetime - Data timestamp
- `open`: float - Opening price
- `high`: float - Highest price in period
- `low`: float - Lowest price in period
- `close`: float - Closing price
- `volume`: float - Trading volume
- `quote_volume`: float - Quote currency volume
- `price_change`: float - Price change percentage
- `price_change_amount`: float - Price change amount
- `best_bid`: float - Best bid price
- `best_ask`: float - Best ask price
- `bid_quantity`: float - Bid quantity at best price
- `ask_quantity`: float - Ask quantity at best price

### Transaction
Record of executed trades with details about price, fees, and timing.

**Fields**:
- `transaction_id`: str - Unique transaction identifier
- `order_id`: str - Associated order ID
- `exchange_id`: str - Exchange where transaction occurred
- `symbol`: str - Trading pair (e.g., BTCUSDT)
- `side`: OrderSide - Enum (buy, sell)
- `quantity`: float - Executed quantity
- `price`: float - Execution price
- `fees`: List[Fee] - Trading fees
- `timestamp`: datetime - Execution timestamp
- `fee_currency`: str - Currency of fees

### Fee
Represents trading fees associated with transactions.

**Fields**:
- `fee_id`: str - Unique fee identifier
- `amount`: float - Fee amount
- `currency`: str - Currency of the fee
- `fee_type`: FeeType - Enum (maker, taker, commission, funding)
- `rate`: float - Fee rate as percentage

## Enums

### AccountType
- spot
- futures
- margin
- options

### OrderSide
- buy
- sell

### OrderType
- market
- limit
- stop_market
- stop_limit
- trailing_stop

### TimeInForce
- GTC (Good Till Cancelled)
- IOC (Immediate or Cancel)
- FOK (Fill or Kill)
- GTD (Good Till Date)

### OrderStatus
- new
- partially_filled
- filled
- canceled
- pending_cancel
- rejected
- expired

### PositionSide
- long
- short
- net

### FeeType
- maker
- taker
- commission
- funding

### StrategyStatus
- active
- paused
- stopped

## Validation Rules

1. **Balance validation**: Available + on_order should equal total balance
2. **Order validation**: Required fields based on order type (e.g., limit orders require price)
3. **Risk parameters validation**: Must not allow risk parameters that exceed account limits
4. **Market data validation**: Prices must be positive, volumes non-negative
5. **Position validation**: Leverage must be within exchange limits

## State Transitions

### Order State Transitions
- `new` → `partially_filled` → `filled` (successful execution)
- `new` → `partially_filled` → `canceled` (partially canceled)
- `new` → `canceled` (canceled before execution)
- `new` → `rejected` (rejected by exchange)

### Position State Transitions
- `open` (new position)
- `open` → `closed` (position fully closed)
- `open` → `partially_closed` → `closed` (partial closes)

### Strategy State Transitions
- `paused` → `active` (strategy activated)
- `active` → `paused` (strategy paused)
- `active` → `stopped` (strategy stopped)
- `paused` → `stopped` (strategy stopped while paused)