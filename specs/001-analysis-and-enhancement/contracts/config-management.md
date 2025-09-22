# Configuration Management Contract

## Endpoint
GET /config/parameters

## Description
Returns a list of all configurable parameters with their descriptions, default values, and configuration sources.

## Request
```json
{
  "category": "string",           // Optional: Filter by parameter category
  "exchange": "string"            // Optional: Filter by exchange-specific parameters
}
```

## Response
```json
{
  "status": "success|error",
  "parameters": [
    {
      "name": "string",
      "description": "string",
      "default_value": "string",
      "category": "string",
      "env_var_name": "string",
      "cli_arg_name": "string",
      "required": "boolean"
    }
  ]
}
```

## Error Responses
- 400: Invalid request parameters
- 500: Internal server error

---

## Endpoint
POST /config/validate

## Description
Validates a set of configuration parameters.

## Request
```json
{
  "parameters": {
    "parameter_name": "parameter_value"
  }
}
```

## Response
```json
{
  "status": "success|error",
  "valid": "boolean",
  "errors": [
    {
      "parameter": "string",
      "error": "string"
    }
  ]
}
```

## Error Responses
- 400: Invalid request parameters
- 500: Internal server error