# MetaExpert Trading Library API Contract

## Overview
This document defines the API contracts for the MetaExpert Trading Library, providing a unified interface for cryptocurrency trading across multiple exchanges.

## API Version
Version: 1.0

## Base Path
```
/api/v1
```

## Authentication
Most endpoints require API authentication. Include your API credentials in the request:

- API Key: Provided as `api_key` parameter or in request header
- API Secret: Used to sign requests (following each exchange's specific requirements)

## Core API Endpoints

### 1. Expert Management

#### Initialize Trading Expert
```
POST /experts
```

**Description:** Create and initialize a new trading expert with specified configuration.

**Request Body:**
```json
{
  "exchange": {
    "name": "binance",
    "api_key": "your_api_key",
    "api_secret": "your_api_secret", 
    "api_passphrase": "passphrase_if_needed",
    "testnet": false
  },
  "trading_config": {
    "market_type": "futures",
    "contract_type": "linear",
    "margin_mode": "isolated",
    "position_mode": "hedge"
  },
  "logging_config": {
    "log_level": "INFO",
    "log_file": "expert.log",
    "trade_log_file": "trades.log",
    "error_log_file": "errors.log",
    "log_to_console": true,
    "structured_logging": false,
    "async_logging": true
  },
  "strategy_config": {
    "symbol": "BTCUSDT",
    "timeframe": "1h",
    "lookback_bars": 100,
    "strategy_id": 1001,
    "strategy_name": "My Strategy",
    "leverage": 10,
    "max_drawdown_pct": 0.2,
    "size_type": "risk_based",
    "size_value": 1.5,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0,
    "trailing_stop_pct": 1.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "expert_id": "exp_12345",
  "status": "initialized",
  "connection_status": "connected",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

#### Get Expert Status
```
GET /experts/{expert_id}
```

**Response:**
```json
{
  "expert_id": "exp_12345",
  "status": "running",
  "connection_status": "connected",
  "active_positions": 2,
  "total_pnl": 125.43,
  "last_updated": "2025-10-09T10:00:00Z"
}
```

#### Start/Stop Expert
```
POST /experts/{expert_id}/control
```

**Request Body:**
```json
{
  "action": "start"  // "start" or "stop"
}
```

**Response:**
```json
{
  "success": true,
  "expert_id": "exp_12345",
  "new_status": "running",  // "running" or "stopped"
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### 2. Trading Operations

#### Place Order
```
POST /experts/{expert_id}/orders
```

**Request Body:**
```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "type": "limit",
  "quantity": 0.01,
  "price": 45000,
  "stop_loss": 44000,
  "take_profit": 47000,
  "time_in_force": "GTC"
}
```

**Response:**
```json
{
  "success": true,
  "order_id": "ord_67890",
  "status": "created",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

#### Get Order Details
```
GET /experts/{expert_id}/orders/{order_id}
```

**Response:**
```json
{
  "order_id": "ord_67890",
  "symbol": "BTCUSDT",
  "side": "buy",
  "type": "limit",
  "quantity": 0.01,
  "price": 45000,
  "status": "partially_filled",
  "filled_quantity": 0.005,
  "average_fill_price": 45050,
  "stop_loss": 44000,
  "take_profit": 47000,
  "created_at": "2025-10-09T09:00:00Z",
  "updated_at": "2025-10-09T10:00:00Z"
}
```

#### Cancel Order
```
DELETE /experts/{expert_id}/orders/{order_id}
```

**Response:**
```json
{
  "success": true,
  "order_id": "ord_67890",
  "status": "cancelled",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### 3. Positions Management

#### Get Active Positions
```
GET /experts/{expert_id}/positions
```

**Response:**
```json
{
  "positions": [
    {
      "position_id": "pos_11111",
      "symbol": "BTCUSDT",
      "side": "long",
      "size": 0.01,
      "entry_price": 45000,
      "current_price": 45500,
      "unrealized_pnl": 50,
      "leverage": 10,
      "margin_used": 4500,
      "liquidation_price": 40500,
      "stop_loss": 44000,
      "take_profit": 47000,
      "created_at": "2025-10-09T08:00:00Z"
    }
  ]
}
```

#### Close Position
```
POST /experts/{expert_id}/positions/{position_id}/close
```

**Response:**
```json
{
  "success": true,
  "position_id": "pos_11111",
  "status": "closed",
  "realized_pnl": 45.25,
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### 4. Market Data

#### Get Market Data
```
GET /experts/{expert_id}/market/{symbol}/data
```

**Query Parameters:**
- `timeframe`: e.g., "1m", "5m", "1h", "1d"
- `limit`: number of data points (default: 100)

**Response:**
```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "data": [
    {
      "timestamp": "2025-10-09T09:00:00Z",
      "open": 45000,
      "high": 45100,
      "low": 44900,
      "close": 45050,
      "volume": 1234.56
    }
  ]
}
```

### 5. Account Information

#### Get Account Balance
```
GET /experts/{expert_id}/account/balance
```

**Response:**
```json
{
  "balances": {
    "USDT": {
      "total": 10000,
      "available": 8500,
      "locked": 1500
    }
  },
  "equity": 10125.43,
  "margin": 1500,
  "available_margin": 8500,
  "last_updated": "2025-10-09T10:00:00Z"
}
```

### 6. Strategy Management

#### Update Strategy Parameters
```
PUT /experts/{expert_id}/strategy
```

**Request Body:**
```json
{
  "stop_loss_pct": 1.5,
  "take_profit_pct": 3.5,
  "trailing_stop_pct": 0.8,
  "max_drawdown_pct": 0.15
}
```

**Response:**
```json
{
  "success": true,
  "updated_parameters": [
    "stop_loss_pct",
    "take_profit_pct",
    "trailing_stop_pct",
    "max_drawdown_pct"
  ],
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### 7. Logging and Monitoring

#### Get Recent Logs
```
GET /experts/{expert_id}/logs
```

**Query Parameters:**
- `log_type`: "main", "trade", or "error" (default: "main")
- `limit`: number of log entries (default: 50)
- `level`: "DEBUG", "INFO", "WARNING", "ERROR" (default: "INFO")

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-10-09T10:00:00Z",
      "level": "INFO",
      "message": "New bar received for BTCUSDT",
      "context": {
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "close": 45500
      }
    }
  ]
}
```

## Error Responses

All API responses follow this structure for errors:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if available"
  },
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### Common Error Codes
- `INVALID_REQUEST`: Request parameters are invalid
- `AUTHENTICATION_FAILED`: API credentials are invalid
- `INSUFFICIENT_FUNDS`: Not enough balance for the operation
- `RATE_LIMIT_EXCEEDED`: Too many requests in a short period
- `EXCHANGE_UNAVAILABLE`: Target exchange is temporarily unavailable
- `POSITION_NOT_FOUND`: Requested position does not exist
- `ORDER_NOT_FOUND`: Requested order does not exist

## Webhook Endpoints

The system can send webhook notifications for important events:

### Register Webhook
```
POST /experts/{expert_id}/webhooks
```

**Request Body:**
```json
{
  "url": "https://your-webhook-url.com/endpoint",
  "events": ["order_filled", "position_closed", "error_occurred"]
}
```

### Webhook Payload Example
```json
{
  "event": "order_filled",
  "expert_id": "exp_12345",
  "timestamp": "2025-10-09T10:00:00Z",
  "data": {
    "order_id": "ord_67890",
    "symbol": "BTCUSDT",
    "side": "buy",
    "filled_quantity": 0.01,
    "average_fill_price": 45050
  }
}
```

## Rate Limits

The API enforces rate limits to ensure fair usage and prevent overloading:
- General requests: 1200 requests per minute per expert
- Market data requests: 600 requests per minute per expert
- Trading requests: 300 requests per minute per expert

When rate limits are exceeded, the API returns a 429 status code with:
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please wait before making more requests."
  }
}
```

## Compliance and Security

All API interactions are logged for compliance purposes. The system implements:
- Request/response logging with timestamps
- Audit trails for all trading operations
- Secure handling of API credentials
- Rate limiting to prevent abuse