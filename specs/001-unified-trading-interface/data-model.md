# Data Model: Unified Trading Entities

This document outlines the core data entities for the MetaExpert library, which will be implemented as Pydantic models. These models serve as the unified data contract for all information passed within the system.

## Enumerations

Shared enumerations will be used to ensure consistency for categorical data.

- **`OrderStatus`**: `OPEN`, `CLOSED`, `CANCELED`, `EXPIRED`
- **`OrderType`**: `MARKET`, `LIMIT`
- **`TradeType`**: `BUY`, `SELL`
- **`Timeframe`**: `TICK`, `M1`, `M5`, `M15`, `H1`, `H4`, `D1`

## Core Entities

### MarketData

Normalized market information from an exchange.

| Attribute | Type | Description |
|---|---|---|
| `symbol` | `str` | The trading symbol (e.g., `BTC/USDT`). |
| `timestamp` | `datetime` | The timestamp of the data point. |
| `open` | `float` | The opening price of the bar. |
| `high` | `float` | The highest price of the bar. |
| `low` | `float` | The lowest price of the bar. |
| `close` | `float` | The closing price of the bar. |
| `volume` | `float` | The trading volume. |

### Order

Represents a trading order.

| Attribute | Type | Description |
|---|---|---|
| `id` | `str` | The unique identifier for the order. |
| `symbol` | `str` | The trading symbol. |
| `type` | `OrderType` | The type of the order (MARKET or LIMIT). |
| `side` | `TradeType` | The side of the trade (BUY or SELL). |
| `amount` | `float` | The quantity of the asset to trade. |
| `price` | `Optional[float]` | The price for a LIMIT order. |
| `status` | `OrderStatus` | The current status of the order. |
| `created_at` | `datetime` | The timestamp when the order was created. |

### Trade

Represents an executed trade or fill.

| Attribute | Type | Description |
|---|---|---|
| `id` | `str` | The unique identifier for the trade. |
| `order_id` | `str` | The ID of the order that generated this trade. |
| `symbol` | `str` | The trading symbol. |
| `side` | `TradeType` | The side of the trade. |
| `amount` | `float` | The quantity traded. |
| `price` | `float` | The execution price. |
| `fee` | `float` | The trading fee paid. |
| `timestamp` | `datetime` | The timestamp of the execution. |

### Position

Represents an open position in the market.

| Attribute | Type | Description |
|---|---|---|
| `symbol` | `str` | The trading symbol. |
| `amount` | `float` | The size of the position. A positive value indicates a long position, negative indicates short. |
| `entry_price` | `float` | The average price at which the position was entered. |
| `unrealized_pnl` | `float` | The current unrealized profit or loss. |

### Portfolio

Aggregates positions and balances.

| Attribute | Type | Description |
|---|---|---|
| `balances` | `Dict[str, float]` | A dictionary mapping asset symbols to their available balance. |
| `positions` | `List[Position]` | A list of all open positions. |
| `total_value_usd` | `float` | The estimated total value of the portfolio in USD. |
