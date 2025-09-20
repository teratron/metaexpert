# Template Creation Contract

## Endpoint
POST /template/create

## Description
Creates a new trading strategy template file for a user.

## Request
```json
{
  "strategy_name": "string",
  "output_directory": "string"
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