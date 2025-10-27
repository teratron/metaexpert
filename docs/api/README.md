# MetaExpert API Documentation

Welcome to the MetaExpert API documentation. This section provides detailed information about the MetaExpert API, including endpoints, request/response formats, and authentication.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [WebSockets](#websockets)

## Overview

The MetaExpert API provides programmatic access to trading functionalities, including market data, order management, and account information. It is designed to be RESTful and uses JSON for request and response payloads.

## Authentication

All API requests must be authenticated using an API key. To obtain an API key, you need to create an account on the MetaExpert platform.

### API Key

To authenticate, include your API key in the `Authorization` header of your requests:

```
Authorization: Bearer YOUR_API_KEY
```

### Example

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.metaexpert.com/v1/account/info
```

## Endpoints

### Account

#### Get Account Info

- **URL**: `/v1/account/info`
- **Method**: `GET`
- **Description**: Retrieve account information.
- **Response**:
  ```json
  {
    "account_id": "123456789",
    "balance": 10000.0,
    "currency": "USDT",
    "positions": [
      {
        "symbol": "BTCUSDT",
        "amount": 0.5,
        "side": "LONG"
      }
    ]
  }
  ```

### Market Data

#### Get Ticker

- **URL**: `/v1/market/ticker`
- **Method**: `GET`
- **Description**: Get the latest ticker for a symbol.
- **Parameters**:
  - `symbol` (required): Trading pair symbol (e.g., BTCUSDT).
- **Response**:
  ```json
  {
    "symbol": "BTCUSDT",
    "price": 50000.0,
    "timestamp": "2023-10-27T10:00:00Z"
  }
  ```

#### Get Order Book

- **URL**: `/v1/market/orderbook`
- **Method**: `GET`
- **Description**: Get the order book for a symbol.
- **Parameters**:
  - `symbol` (required): Trading pair symbol (e.g., BTCUSDT).
  - `depth` (optional): Depth of the order book (default: 10).
- **Response**:
  ```json
  {
    "symbol": "BTCUSDT",
    "bids": [
      [49999.0, 0.1],
      [49998.0, 0.2]
    ],
    "asks": [
      [50001.0, 0.1],
      [50002.0, 0.2]
    ]
  }
  ```

### Orders

#### Place Order

- **URL**: `/v1/orders/place`
- **Method**: `POST`
- **Description**: Place a new order.
- **Request Body**:
  ```json
  {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "price": 49999.0,
    "quantity": 0.1
  }
  ```
- **Response**:
  ```json
  {
    "order_id": "987654321",
    "status": "NEW"
  }
  ```

#### Get Order

- **URL**: `/v1/orders/{order_id}`
- **Method**: `GET`
- **Description**: Get order details by ID.
- **Response**:
  ```json
  {
    "order_id": "987654321",
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "price": 49999.0,
    "quantity": 0.1,
    "status": "FILLED",
    "filled_quantity": 0.1,
    "timestamp": "2023-10-27T10:00:00Z"
  }
  ```

#### Cancel Order

- **URL**: `/v1/orders/{order_id}`
- **Method**: `DELETE`
- **Description**: Cancel an order by ID.
- **Response**:
  ```json
  {
    "order_id": "987654321",
    "status": "CANCELLED"
  }
  ```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests.

### Common Status Codes

- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or missing required parameters.
- `401 Unauthorized`: The API key is invalid or missing.
- `403 Forbidden`: The API key does not have permission to access the requested resource.
- `404 Not Found`: The requested resource was not found.
- `429 Too Many Requests`: Rate limit exceeded.
- `500 Internal Server Error`: An unexpected error occurred on the server.

### Error Response Format

When an error occurs, the API returns a JSON object with an error message:

```json
{
  "error": "Invalid API key"
}
```

## Rate Limiting

To ensure fair usage and prevent abuse, the API implements rate limiting. The default rate limit is 1000 requests per minute per API key.

If you exceed the rate limit, you will receive a `429 Too Many Requests` response. You should wait before making additional requests.

## WebSockets

For real-time market data and order updates, MetaExpert provides WebSocket endpoints.

### Connecting

WebSocket endpoint: `wss://ws.metaexpert.com/v1`

### Authentication

To authenticate a WebSocket connection, send an authentication message after connecting:

```json
{
  "type": "auth",
  "api_key": "YOUR_API_KEY"
}
```

### Subscriptions

Once authenticated, you can subscribe to various channels:

#### Ticker Updates

```json
{
  "type": "subscribe",
  "channel": "ticker",
  "symbol": "BTCUSDT"
}
```

#### Order Book Updates

```json
{
  "type": "subscribe",
  "channel": "orderbook",
  "symbol": "BTCUSDT"
}
```

#### Order Updates

```json
{
  "type": "subscribe",
  "channel": "orders"
}
```

### Messages

The WebSocket server sends messages in the following format:

```json
{
  "type": "ticker",
  "data": {
    "symbol": "BTCUSDT",
    "price": 50000.0,
    "timestamp": "2023-10-27T10:00:00Z"
  }
}
