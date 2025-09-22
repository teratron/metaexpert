# CLI Argument Parsing Contract

## Endpoint
POST /cli/parse

## Description
Parses command-line arguments and returns the parsed configuration.

## Request
```json
{
  "arguments": ["string"],
  "program_name": "string"
}
```

## Response
```json
{
  "status": "success|error",
  "parsed_arguments": {
    "exchange": "string",
    "trade_mode": "string",
    "market_type": "string",
    "contract_type": "string",
    "pair": "string",
    "timeframe": "string",
    "size": "number",
    "stop_loss": "number",
    "take_profit": "number",
    "trailing_stop": "number",
    "start_date": "string",
    "end_date": "string",
    "balance": "number",
    "log_level": "string",
    "api_key": "string",
    "api_secret": "string",
    "base_url": "string",
    "new": "string"
  },
  "errors": ["string"]
}
```

## Error Responses
- 400: Invalid arguments provided
- 500: Internal server error