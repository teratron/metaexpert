# Exchange API Contracts

## Overview

This document defines the API contracts for the unified trading interface, specifying the standardized endpoints and data structures that each exchange implementation must adhere to.

## Common Headers

All API requests must include the following headers:
- `Content-Type: application/json`
- `X-Exchange-ID: {exchange_id}` - Identifier for the specific exchange
- `X-API-Key: {api_key}` - API key for authentication
- `X-Timestamp: {timestamp}` - Request timestamp for rate limiting

## Endpoints

### 1. Exchange Connection Management

#### POST /api/v1/connect
Establish a connection to an exchange.

**Request:**
```json
{
  "exchange_id": "binance",
  "api_key": "your_api_key",
  "secret_key": "your_secret_key",
  "passphrase": "your_passphrase",
  "testnet": true
}
```

**Response:**
```json
{
  "connection_id": "conn_abc123",
  "exchange_id": "binance",
  "status": "connected",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### POST /api/v1/disconnect
Disconnect from an exchange.

**Request:**
```json
{
  "connection_id": "conn_abc123"
}
```

**Response:**
```json
{
  "connection_id": "conn_abc123",
  "status": "disconnected",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### 2. Account Management

#### GET /api/v1/account/{account_id}
Retrieve account information.

**Response:**
```json
{
  "account_id": "acc_123",
  "exchange_id": "binance",
  "account_type": "spot",
  "balances": {
    "BTC": {
      "available": 1.5,
      "on_order": 0.2,
      "total": 1.7
    },
    "USDT": {
      "available": 10000,
      "on_order": 2000,
      "total": 12000
    }
  },
  "positions": [
    {
      "position_id": "pos_456",
      "symbol": "BTCUSDT",
      "side": "long",
      "quantity": 0.5,
      "entry_price": 30000.0,
      "current_price": 32000.0,
      "unrealized_pnl": 1000.0,
      "margin_used": 15000.0,
      "leverage": 2.0
    }
  ],
  "permissions": ["read", "trade"]
}
```

#### GET /api/v1/account/{account_id}/balance
Retrieve account balance information.

**Response:**
```json
{
  "account_id": "acc_123",
  "exchange_id": "binance",
  "balances": {
    "BTC": {
      "available": 1.5,
      "on_order": 0.2,
      "total": 1.7
    },
    "USDT": {
      "available": 10000,
      "on_order": 2000,
      "total": 12000
    }
  }
}
```

### 3. Order Management

#### POST /api/v1/order
Place a new order.

**Request:**
```json
{
  "client_order_id": "cl_ord_123",
  "symbol": "BTCUSDT",
  "side": "buy",
  "order_type": "limit",
  "time_in_force": "GTC",
  "quantity": 0.001,
  "price": 40000.0
}
```

**Response:**
```json
{
  "order_id": "ord_456",
  "client_order_id": "cl_ord_123",
  "symbol": "BTCUSDT",
  "side": "buy",
  "order_type": "limit",
  "time_in_force": "GTC",
  "quantity": 0.001,
  "price": 40000.0,
  "status": "new",
  "filled_quantity": 0.0,
  "average_fill_price": null,
  "fees": [],
  "timestamp": "2023-01-01T00:00:00Z",
  "update_timestamp": "2023-01-01T00:00:00Z"
}
```

#### PUT /api/v1/order/{order_id}
Modify an existing order.

**Request:**
```json
{
  "order_id": "ord_456",
  "price": 41000.0
}
```

**Response:**
```json
{
  "order_id": "ord_456",
  "status": "modified",
  "price": 41000.0
}
```

#### DELETE /api/v1/order/{order_id}
Cancel an order.

**Request:**
```json
{
  "order_id": "ord_456",
  "symbol": "BTCUSDT"
}
```

**Response:**
```json
{
  "order_id": "ord_456",
  "status": "canceled",
  "canceled_quantity": 0.001
}
```

#### GET /api/v1/order/{order_id}
Retrieve order information.

**Response:**
```json
{
  "order_id": "ord_456",
  "client_order_id": "cl_ord_123",
  "symbol": "BTCUSDT",
  "side": "buy",
  "order_type": "limit",
  "time_in_force": "GTC",
  "quantity": 0.001,
  "price": 41000.0,
  "status": "partially_filled",
  "filled_quantity": 0.0005,
  "average_fill_price": 40500.0,
  "fees": [
    {
      "fee_id": "fee_789",
      "amount": 0.000001,
      "currency": "BTC",
      "fee_type": "maker",
      "rate": 0.001
    }
  ],
  "timestamp": "2023-01-01T00:00:00Z",
  "update_timestamp": "2023-01-01T00:05:00Z"
}
```

#### GET /api/v1/orders
Retrieve multiple orders.

**Query Parameters:**
- `symbol` (optional): Filter by trading pair
- `status` (optional): Filter by order status
- `limit` (optional): Number of orders to return (default: 100, max: 1000)

**Response:**
```json
{
  "orders": [
    {
      "order_id": "ord_456",
      "client_order_id": "cl_ord_123",
      "symbol": "BTCUSDT",
      "side": "buy",
      "order_type": "limit",
      "time_in_force": "GTC",
      "quantity": 0.001,
      "price": 41000.0,
      "status": "partially_filled",
      "filled_quantity": 0.0005,
      "timestamp": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### 4. Market Data

#### GET /api/v1/ticker/{symbol}
Retrieve ticker information for a symbol.

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "last_price": 41000.0,
  "price_change": 2.5,
  "price_change_amount": 1000.0,
  "high": 42000.0,
  "low": 39000.0,
  "volume": 1000.5,
  "quote_volume": 40500000.0,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### GET /api/v1/klines/{symbol}
Retrieve k-line (candlestick) data.

**Query Parameters:**
- `interval`: Time interval (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)
- `limit` (optional): Number of k-lines to return (default: 500, max: 1000)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "interval": "1h",
  "klines": [
    {
      "timestamp": "2023-01-01T00:00:00Z",
      "open": 40000.0,
      "high": 41000.0,
      "low": 39500.0,
      "close": 40800.0,
      "volume": 10.5,
      "quote_volume": 420000.0,
      "trades": 150
    }
  ]
}
```

#### GET /api/v1/depth/{symbol}
Retrieve order book depth.

**Query Parameters:**
- `limit` (optional): Number of entries to return (default: 100, max: 1000)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2023-01-01T00:00:00Z",
  "bids": [
    [40999.0, 0.5],  // [price, quantity]
    [40998.0, 0.3],
    [40997.0, 0.2]
  ],
  "asks": [
    [41000.0, 0.4],
    [41001.0, 0.6],
    [41002.0, 0.8]
  ]
}
```

### 5. Portfolio Management

#### GET /api/v1/portfolio
Retrieve portfolio information across all connected exchanges.

**Response:**
```json
{
  "portfolio_id": "port_abc",
  "name": "Main Portfolio",
  "total_balance": 50000.0,
  "positions": [
    {
      "position_id": "pos_456",
      "symbol": "BTCUSDT",
      "exchange_id": "binance",
      "side": "long",
      "quantity": 0.5,
      "entry_price": 30000.0,
      "current_price": 41000.0,
      "unrealized_pnl": 5500.0,
      "realized_pnl": 1200.0,
      "margin_used": 15000.0,
      "leverage": 2.0,
      "timestamp": "2023-01-01T00:00:00Z"
    }
  ],
  "balances": {
    "binance": {
      "BTC": 1.5,
      "USDT": 10000.0
    },
    "bybit": {
      "BTC": 0.8,
      "USDT": 8000.0
    }
  },
  "total_pnl": 6700.0,
  "daily_pnl": 200.0,
  "last_updated": "2023-01-01T00:00:00Z"
}
```

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "The specified order could not be found",
    "timestamp": "2023-01-01T00:00:00Z",
    "request_id": "req_123"
  }
}
```

### Common Error Codes

- `INVALID_REQUEST`: The request format is invalid
- `AUTHENTICATION_FAILED`: API key or signature is invalid
- `INSUFFICIENT_FUNDS`: Not enough balance to execute the operation
- `ORDER_NOT_FOUND`: The specified order does not exist
- `RATE_LIMIT_EXCEEDED`: Too many requests in a given time period
- `EXCHANGE_UNAVAILABLE`: The exchange API is temporarily unavailable
- `INVALID_SYMBOL`: The specified symbol is not valid