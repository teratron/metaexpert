# Data Model for MetaExpert Framework

## Core Entities

### Expert
- **Fields**:
  - `id`: Unique identifier for the expert
  - `name`: Name of the trading strategy
  - `description`: Description of the trading strategy
  - `exchange`: Exchange the expert operates on (Binance, Bybit, OKX)
  - `symbol`: Trading pair symbol (e.g., BTCUSDT)
  - `strategy_config`: Configuration parameters for the trading strategy
  - `state`: Current state (active, paused, stopped)
  - `created_at`: Timestamp of expert creation
  - `updated_at`: Timestamp of last update

- **Relationships**:
  - One-to-many with Trade records
  - One-to-many with Order records
  - Many-to-one with Exchange

- **Validation Rules**:
  - Name must be unique per exchange
  - Exchange must be one of supported exchanges
  - Symbol must be valid for the selected exchange
  - Strategy config must be valid JSON

### Exchange
- **Fields**:
  - `id`: Unique identifier for the exchange
  - `name`: Exchange name (Binance, Bybit, OKX)
  - `api_config`: API connection configuration
  - `supported_pairs`: List of supported trading pairs
  - `status`: Connection status (connected, disconnected)

- **Relationships**:
  - One-to-many with Experts
  - One-to-many with Markets

- **Validation Rules**:
  - Name must be unique
  - API config must contain required fields
  - Status must be valid enum value

### Market
- **Fields**:
  - `id`: Unique identifier for the market
  - `exchange_id`: Foreign key to Exchange
  - `symbol`: Trading pair symbol (e.g., BTCUSDT)
  - `base_currency`: Base currency (e.g., BTC)
  - `quote_currency`: Quote currency (e.g., USDT)
  - `min_order_size`: Minimum order size allowed
  - `price_precision`: Number of decimal places for prices
  - `status`: Market status (active, suspended)

- **Relationships**:
  - Many-to-one with Exchange
  - One-to-many with Price data

- **Validation Rules**:
  - Symbol must be unique per exchange
  - Min order size must be positive
  - Price precision must be non-negative integer

### Trade
- **Fields**:
  - `id`: Unique identifier for the trade
  - `expert_id`: Foreign key to Expert
  - `order_id`: Order ID from the exchange
  - `symbol`: Trading pair symbol
  - `side`: Trade side (buy, sell)
  - `quantity`: Quantity traded
  - `price`: Price at which trade executed
  - `timestamp`: Time of execution
  - `fee`: Fee amount paid
  - `fee_currency`: Currency of the fee

- **Relationships**:
  - Many-to-one with Expert
  - Many-to-one with Order (optional)

- **Validation Rules**:
  - Side must be buy or sell
  - Quantity must be positive
  - Price must be positive
  - Timestamp must be in the past

### Order
- **Fields**:
  - `id`: Unique identifier for the order
  - `expert_id`: Foreign key to Expert
  - `exchange_order_id`: Order ID from the exchange
  - `symbol`: Trading pair symbol
  - `side`: Order side (buy, sell)
  - `type`: Order type (market, limit, stop)
  - `quantity`: Order quantity
  - `price`: Order price (for limit orders)
  - `status`: Order status (new, partially_filled, filled, cancelled)
  - `timestamp`: Time of order creation
  - `filled_quantity`: Quantity filled so far

- **Relationships**:
  - Many-to-one with Expert
  - One-to-many with Trades

- **Validation Rules**:
  - Side must be buy or sell
  - Type must be valid enum value
  - Quantity must be positive
  - Status must be valid enum value

### Price
- **Fields**:
  - `id`: Unique identifier for the price record
  - `market_id`: Foreign key to Market
  - `timestamp`: Time of price data
  - `open`: Opening price
  - `high`: Highest price in the period
  - `low`: Lowest price in the period
  - `close`: Closing price
  - `volume`: Trading volume in the period
  - `interval`: Time interval (1m, 5m, 15m, 1h, 4h, 1d)

- **Relationships**:
  - Many-to-one with Market

- **Validation Rules**:
  - Prices must be positive
  - Volume must be non-negative
  - Interval must be valid enum value

## State Transitions

### Expert States
- `stopped` → `active`: When expert is started
- `active` → `paused`: When expert is paused
- `paused` → `active`: When expert is resumed
- `active` → `stopped`: When expert is stopped
- `paused` → `stopped`: When expert is stopped from paused state

### Order States
- `new` → `partially_filled`: When partial execution occurs
- `new` → `filled`: When fully executed immediately
- `new` → `cancelled`: When order is cancelled before execution
- `partially_filled` → `filled`: When remaining quantity is filled
- `partially_filled` → `cancelled`: When remaining quantity is cancelled