# CLI Parsing Contract Test

from src.metaexpert.cli.endpoint import parse_cli_arguments


# Test that the CLI parsing endpoint works correctly
def test_cli_parsing_success():
    # Given a valid set of command-line arguments
    request = {
        "arguments": [
            "--exchange",
            "binance",
            "--pair",
            "BTCUSDT",
            "--timeframe",
            "1h",
        ],
        "program_name": "metaexpert",
    }

    # When the CLI parsing endpoint is called
    response = parse_cli_arguments(request)

    # Then a success response with parsed arguments should be returned
    assert response["status"] == "success"
    assert response["parsed_arguments"]["exchange"] == "binance"
    assert response["parsed_arguments"]["pair"] == "BTCUSDT"
    assert response["parsed_arguments"]["timeframe"] == "1h"


# Test that the CLI parsing fails with invalid arguments
def test_cli_parsing_invalid_arguments():
    # Given an invalid set of command-line arguments
    request = {
        "arguments": ["--invalid-argument", "value"],
        "program_name": "metaexpert",
    }

    # When the CLI parsing endpoint is called
    response = parse_cli_arguments(request)

    # Then an error response should be returned
    assert response["status"] == "error"
    assert "unrecognized arguments" in response["errors"][0]
