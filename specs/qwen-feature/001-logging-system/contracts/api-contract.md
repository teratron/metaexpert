# API Contract for MetaExpert Logging System

## Overview

This document defines the API contract for the MetaExpert logging system based on functional requirements and user stories in the feature specification.

## Configuration API

### LogConfiguration Model

```
{
  "log_level": "INFO",                    // str, enum: DEBUG, INFO, WARNING, ERROR, CRITICAL
  "log_directory": "./logs",              // str, path to log directory
  "expert_log_file": "expert.log",        // str, filename for expert logs
  "trades_log_file": "trades.log",        // str, filename for trade logs
  "errors_log_file": "errors.log",        // str, filename for error logs
  "enable_async": false,                  // bool, enable asynchronous logging
  "max_file_size_mb": 10,                 // int, max file size in MB before rotation
  "backup_count": 5,                      // int, number of backup files to keep
  "enable_structured_logging": false,     // bool, enable RFC 5424 JSON format
  "enable_contextual_logging": true,      // bool, enable contextual field inclusion
  "mask_sensitive_data": true,            // bool, enable masking of sensitive info
  "console_log_format": "text",           // str, enum: text, json
  "file_log_format": "json",              // str, enum: text, json
  "context_fields": [                     // list[str], contextual fields to include
    "expert_name",
    "symbol", 
    "trade_id",
    "order_id",
    "strategy_id",
    "account_id"
  ]
}
```

### Configuration Endpoints

#### GET /config/logging
Retrieve current logging configuration

**Response (200 OK)**:
```json
{
  "data": {
    "log_level": "INFO",
    "log_directory": "./logs",
    "expert_log_file": "expert.log",
    "trades_log_file": "trades.log",
    "errors_log_file": "errors.log",
    "enable_async": false,
    "max_file_size_mb": 10,
    "backup_count": 5,
    "enable_structured_logging": false,
    "enable_contextual_logging": true,
    "mask_sensitive_data": true,
    "console_log_format": "text",
    "file_log_format": "json",
    "context_fields": [
      "expert_name",
      "symbol",
      "trade_id", 
      "order_id",
      "strategy_id",
      "account_id"
    ]
  }
}
```

#### PUT /config/logging
Update logging configuration

**Request Body**:
```json
{
  "log_level": "DEBUG",
  "enable_async": true
}
```

**Response (200 OK)**:
```json
{
  "data": {
    "log_level": "DEBUG",
    "enable_async": true
  }
}
```

## Logging API

### Log Entry Model

```
{
  "timestamp": "2024-12-20T10:30:00.000Z",  // ISO 8601 timestamp
  "severity": "INFO",                         // str, enum: DEBUG, INFO, WARNING, ERROR, CRITICAL
  "message": "Log message content",           // str, log message
  "expert_name": "SampleExpert",              // str, name of trading expert
  "symbol": "BTCUSDT",                        // str, trading symbol (optional)
  "trade_id": "trade_123",                    // str, trade ID (optional)
  "order_id": "order_456",                    // str, order ID (optional)
  "strategy_id": "ema_strategy",              // str, strategy ID (optional)
  "account_id": "account_789",                // str, account ID (optional)
  "function": "place_order",                  // str, function name (optional)
  "file": "trading.py",                       // str, source file (optional)
  "line": 123,                                // int, line number (optional)
  "exception_details": {                      // object, exception info (optional)
    "type": "ExceptionType",
    "message": "Exception message",
    "traceback": "Full traceback"
  }
}
```

### Logging Endpoints

#### POST /log
Submit a log entry

**Request Body**:
```json
{
  "severity": "INFO",
  "message": "Expert initialized successfully",
  "expert_name": "SampleExpert",
  "symbol": "BTCUSDT"
}
```

**Response (201 Created)**:
```json
{
  "message": "Log entry submitted successfully"
}
```

#### GET /logs/expert
Retrieve expert log entries

**Query Parameters**:
- `limit`: number of entries to return (default: 100)
- `offset`: number of entries to skip (default: 0)
- `from`: start timestamp (ISO 8601 format)
- `to`: end timestamp (ISO 8601 format)
- `level`: minimum severity level (optional)

**Response (200 OK)**:
```json
{
  "data": [
    {
      "timestamp": "2024-12-20T10:30:00.000Z",
      "severity": "INFO",
      "message": "Expert initialized successfully",
      "expert_name": "SampleExpert",
      "symbol": "BTCUSDT"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "total": 1
  }
}
```

#### GET /logs/trades
Retrieve trade log entries with same parameters as expert logs

#### GET /logs/errors
Retrieve error log entries with same parameters as expert logs

## Context Management API

### POST /context
Bind contextual information to subsequent log entries

**Request Body**:
```json
{
  "context": {
    "expert_name": "SampleExpert",
    "symbol": "BTCUSDT",
    "trade_id": "trade_123",
    "account_id": "account_789"
  }
}
```

**Response (200 OK)**:
```json
{
  "message": "Context bound successfully",
  "context_id": "ctx_abc123"
}
```

### DELETE /context/{context_id}
Remove bound context

**Response (200 OK)**:
```json
{
  "message": "Context removed successfully"
}
```

## Error Handling

### Standard Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error details
    }
  }
}
```

### Common Error Codes

- `LOG_CONFIG_INVALID`: Configuration parameters are invalid
- `LOG_FILE_WRITE_ERROR`: Unable to write to log file
- `LOG_HANDLER_ERROR`: Error in log handler
- `LOG_DISK_FULL`: Insufficient disk space for logging