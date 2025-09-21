# Template Creation Contract

## Endpoint
POST /template/create

## Description
Creates a new trading strategy template file for a user with optional configuration parameters.

## Request
```json
{
  "strategy_name": "string",
  "output_directory": "string",
  "exchange": "string",           // Optional: binance, bybit, okx, bitget, kucoin
  "symbol": "string",             // Optional: Trading pair (e.g., BTCUSDT)
  "timeframe": "string",          // Optional: Timeframe (e.g., 1h, 5m)
  "market_type": "string",        // Optional: spot, futures, options
  "contract_type": "string",      // Optional: linear, inverse
  "leverage": "integer",          // Optional: Leverage value
  "strategy_id": "integer",       // Optional: Strategy ID
  "strategy_name": "string",      // Optional: Strategy name
  "comment": "string"             // Optional: Order comment
}
```

## Response
```json
{
  "status": "success|error",
  "message": "string",
  "file_path": "string"
}
```

## Error Responses
- 400: Invalid request parameters
- 500: Internal server error

## Additional Endpoints

### GET /template/exchanges
Returns a list of supported exchanges.

### GET /template/parameters
Returns a list of configurable template parameters with descriptions and default values.