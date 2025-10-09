# API Contracts: Logger Module

## Overview
This document defines the API contracts for the enhanced MetaExpert logging module. These contracts specify the interfaces for logging operations, configuration management, and log data structures.

## Core Logger Interface

### Create Logger Instance
```
POST /logger
```

**Description**: Create a new logger instance with specified configuration

**Request Body**:
```json
{
  "name": "trading-logger",
  "logLevel": "INFO",
  "structuredLogging": true,
  "asyncLogging": true,
  "destinations": [
    {
      "type": "file",
      "path": "/var/log/trading/main.log",
      "format": "json"
    },
    {
      "type": "console",
      "format": "text"
    }
  ]
}
```

**Response**:
```json
{
  "loggerId": "logger_12345",
  "status": "created",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### Log Message
```
POST /logger/{loggerId}/log
```

**Description**: Log a message with optional structured data

**Request Body**:
```json
{
  "level": "INFO",
  "message": "Trade executed successfully",
  "timestamp": "2025-10-09T10:00:00Z",
  "extra": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 45000.0,
    "orderId": "order_12345"
  }
}
```

**Response**:
```json
{
  "status": "logged",
  "entryId": "entry_67890",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

### Get Logger Configuration
```
GET /logger/{loggerId}
```

**Description**: Retrieve the current configuration of a logger instance

**Response**:
```json
{
  "loggerId": "logger_12345",
  "name": "trading-logger",
  "logLevel": "INFO",
  "structuredLogging": true,
  "asyncLogging": true,
  "destinations": [
    {
      "type": "file",
      "path": "/var/log/trading/main.log",
      "format": "json",
      "enabled": true
    },
    {
      "type": "console",
      "format": "text",
      "enabled": true
    }
  ],
  "createdAt": "2025-10-09T09:00:00Z",
  "updatedAt": "2025-10-09T10:00:00Z"
}
```

### Update Logger Configuration
```
PUT /logger/{loggerId}
```

**Description**: Update the configuration of an existing logger instance

**Request Body**:
```json
{
  "logLevel": "DEBUG",
  "structuredLogging": true,
  "asyncLogging": true,
  "destinations": [
    {
      "type": "file",
      "path": "/var/log/trading/debug.log",
      "format": "json",
      "enabled": true
    },
    {
      "type": "console",
      "format": "text",
      "enabled": true
    },
    {
      "type": "http",
      "url": "https://logs.example.com/api/v1/logs",
      "format": "json",
      "enabled": true,
      "authentication": {
        "type": "bearer",
        "token": "secret_token"
      }
    }
  ]
}
```

**Response**:
```json
{
  "loggerId": "logger_12345",
  "status": "updated",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

## Trade Logging Interface

### Log Trade Event
```
POST /logger/{loggerId}/trade
```

**Description**: Log a specialized trade event with structured trade data

**Request Body**:
```json
{
  "eventType": "order_executed",
  "timestamp": "2025-10-09T10:00:00Z",
  "tradeData": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 45000.0,
    "orderId": "order_12345",
    "executionType": "MARKET",
    "commission": 4.5,
    "commissionAsset": "USDT",
    "strategyId": "strategy_001"
  }
}
```

**Response**:
```json
{
  "status": "logged",
  "entryId": "trade_67890",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

## Error Logging Interface

### Log Error
```
POST /logger/{loggerId}/error
```

**Description**: Log an error with detailed exception information and context

**Request Body**:
```json
{
  "message": "Order placement failed",
  "timestamp": "2025-10-09T10:00:00Z",
  "exception": {
    "type": "InsufficientFundsError",
    "message": "Not enough USDT balance to place order",
    "stackTrace": "Traceback (most recent call last):\n  File \"trading.py\", line 123, in place_order\n    result = client.place_order(...)\n  File \"client.py\", line 456, in place_order\n    raise InsufficientFundsError(\"Not enough USDT balance\")\nInsufficientFundsError: Not enough USDT balance"
  },
  "context": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 45000.0,
    "attempt": 1,
    "userId": "user_001"
  }
}
```

**Response**:
```json
{
  "status": "logged",
  "entryId": "error_67890",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

## Performance Monitoring Interface

### Log Performance Metric
```
POST /logger/{loggerId}/metric
```

**Description**: Log a performance metric with timestamp and value

**Request Body**:
```json
{
  "metricName": "order_execution_time",
  "value": 150,
  "unit": "milliseconds",
  "timestamp": "2025-10-09T10:00:00Z",
  "tags": {
    "exchange": "binance",
    "symbol": "BTCUSDT",
    "operation": "place_order"
  }
}
```

**Response**:
```json
{
  "status": "logged",
  "entryId": "metric_67890",
  "timestamp": "2025-10-09T10:00:00Z"
}
```

## Log Retrieval Interface

### Query Log Entries
```
GET /logger/{loggerId}/entries
```

**Description**: Query log entries with filtering and pagination

**Query Parameters**:
- `level`: Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `startTime`: Filter entries after this timestamp (ISO 8601)
- `endTime`: Filter entries before this timestamp (ISO 8601)
- `limit`: Maximum number of entries to return (default: 100)
- `offset`: Offset for pagination (default: 0)
- `search`: Search term to filter message content

**Response**:
```json
{
  "entries": [
    {
      "entryId": "entry_001",
      "timestamp": "2025-10-09T10:00:05Z",
      "level": "INFO",
      "logger": "trading-logger",
      "message": "Order executed successfully",
      "extra": {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "quantity": 0.1,
        "price": 45000.0,
        "orderId": "order_12345"
      }
    },
    {
      "entryId": "entry_002",
      "timestamp": "2025-10-09T10:00:03Z",
      "level": "DEBUG",
      "logger": "trading-logger",
      "message": "Market data updated",
      "extra": {
        "symbol": "BTCUSDT",
        "bidPrice": 44999.5,
        "askPrice": 45000.5,
        "spread": 1.0
      }
    }
  ],
  "total": 1250,
  "limit": 100,
  "offset": 0
}
```

### Get Log Statistics
```
GET /logger/{loggerId}/stats
```

**Description**: Retrieve statistics about log entries

**Response**:
```json
{
  "loggerId": "logger_12345",
  "totalEntries": 12500,
  "entriesByLevel": {
    "DEBUG": 8000,
    "INFO": 3500,
    "WARNING": 750,
    "ERROR": 240,
    "CRITICAL": 10
  },
  "entriesByType": {
    "general": 9000,
    "trade": 2500,
    "error": 300,
    "performance": 700
  },
  "firstEntry": "2025-10-09T09:00:00Z",
  "lastEntry": "2025-10-09T10:00:00Z",
  "storageUsed": "25.4 MB"
}
```

## Data Structures

### LogEntry
Represents a single log entry with all associated metadata.

```json
{
  "entryId": "string",
  "timestamp": "ISO 8601 timestamp",
  "level": "DEBUG | INFO | WARNING | ERROR | CRITICAL",
  "logger": "string",
  "message": "string",
  "module": "string",
  "function": "string",
  "lineNumber": "integer",
  "thread": {
    "id": "string",
    "name": "string"
  },
  "process": {
    "id": "string",
    "name": "string"
  },
  "exception": {
    "type": "string",
    "message": "string",
    "traceback": "string"
  },
  "extra": "object",
  "logType": "general | trade | error | performance",
  "tradeData": "object",
  "errorContext": "object"
}
```

### LoggerConfiguration
Represents the configuration of a logger instance.

```json
{
  "loggerId": "string",
  "name": "string",
  "logLevel": "DEBUG | INFO | WARNING | ERROR | CRITICAL",
  "structuredLogging": "boolean",
  "asyncLogging": "boolean",
  "destinations": [
    {
      "type": "file | console | syslog | http | tcp | udp",
      "path": "string",
      "port": "integer",
      "format": "json | text | xml",
      "enabled": "boolean"
    }
  ],
  "createdAt": "ISO 8601 timestamp",
  "updatedAt": "ISO 8601 timestamp"
}
```

### PerformanceMetric
Represents a performance metric with value and metadata.

```json
{
  "metricId": "string",
  "metricName": "string",
  "value": "number",
  "unit": "string",
  "timestamp": "ISO 8601 timestamp",
  "tags": "object"
}
```

## Error Responses

All API endpoints follow a consistent error response format:

```json
{
  "error": {
    "code": "string",
    "message": "human-readable error message",
    "details": "additional error details if available"
  },
  "timestamp": "ISO 8601 timestamp"
}
```

### Common Error Codes
- `INVALID_REQUEST`: Request parameters are invalid
- `LOGGER_NOT_FOUND`: Specified logger instance does not exist
- `PERMISSION_DENIED`: Insufficient permissions to perform operation
- `INTERNAL_ERROR`: Unexpected internal error occurred
- `RATE_LIMIT_EXCEEDED`: Too many requests in short period

## Webhook Notifications

The logger can send webhook notifications for important events:

### Register Webhook
```
POST /logger/{loggerId}/webhooks
```

**Request Body**:
```json
{
  "url": "https://your-service.com/webhook",
  "events": ["error_logged", "critical_alert"],
  "authentication": {
    "type": "bearer",
    "token": "webhook_secret"
  }
}
```

### Webhook Payload
```json
{
  "eventId": "event_12345",
  "eventType": "error_logged",
  "timestamp": "2025-10-09T10:00:00Z",
  "loggerId": "logger_12345",
  "payload": {
    "entry": {
      // Full LogEntry object
    }
  }
}
```