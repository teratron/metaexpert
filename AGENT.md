# MetaExpert Project Context

## Development Conventions

### Language Requirements

Code and documentation language:

- All code, comments, documentation, variable names, function names, class names, method names, attribute names, and technical terms must be in English
- Maintain English as the primary language for all technical elements including error messages, log entries, configuration keys, and API responses to ensure readability and maintainability
- Technical documentation, inline comments, docstrings, and README files must be written in English
- All commit messages, pull request descriptions, and issue titles related to code changes should be in English

Communication style:

- Explanations and discussions in the chat interface should be in Russian
- Use Russian for conversational responses, clarifications, project planning, and non-technical interactions
- Project management communications, feature discussions, and strategic decisions should be conducted in Russian
- Code review comments and technical discussions during development can be in Russian unless collaborating with English-speaking developers

## Project Overview

## Architecture & Core Components

### Main Structure

```text
src/metaexpert/                    # Main application package for MetaExpert
├── __init__.py                    # Package initialization
├── __main__.py                    # Entry point for running the application as a module
├── __version__.py                 # Application version definition
├── config.py                      # Global settings and configurations
├── core/                          # Core system - main components
│   ├── __init__.py                # Core module initialization
│   └── [other core modules]       # Additional core modules (markets, trades, timeframes, etc.)
├── exchanges/                     # Support for various exchanges
│   ├── __init__.py                # Exchanges module initialization
│   ├── binance/                   # Implementation for Binance exchange
│   │   ├── __init__.py            # Binance module initialization
│   │   ├── config.py              # Binance configuration
│   │   └── [other binance modules] # Additional Binance modules
│   ├── bybit/                     # Implementation for Bybit exchange
│   │   ├── __init__.py            # Bybit module initialization
│   │   ├── config.py              # Bybit configuration
│   │   └── [other bybit modules]  # Additional Bybit modules
│   └── okx/                       # Implementation for OKX exchange
│       ├── __init__.py            # OKX module initialization
│       ├── config.py              # OKX configuration
│       └── [other okx modules]    # Additional OKX modules
├── backtest/                      # Backtesting module for strategy testing on historical data
│   ├── __init__.py                # Backtest module initialization
│   ├── README.md                  # Documentation for backtesting usage
│   └── [other backtest modules]   # Backtest components
├── logger/                        # Logging system
│   ├── __init__.py                # Logging module initialization
│   └── README.md                  # Logging documentation
│   └── [other logger modules]     # Logging components
├── cli/                           # Command line interface
│   ├── __init__.py                # CLI module initialization
│   ├── README.md                  # Documentation for CLI usage
│   └── [other cli modules]        # Command line interface components
├── template/                      # Templates for generating new experts
│   ├── __init__.py                # Templates module initialization
│   ├── template.py                # Template implementation
│   └── README.md                  # Templates documentation
├── utils/                         # Utility functions
│   ├── __init__.py                # Utilities module initialization
│   ├── package.py                 # Utilities for package management
│   ├── file.py                    # Utilities for files management
│   ├── time.py                    # Utilities for time management
│   ├── README.md                  # Utilities documentation
│   └── [other utils modules]      # Additional helper functions
├── websocket/                     # WebSocket connection handling
│   ├── __init__.py                # WebSocket module initialization
│   └── [other websocket modules]  # WebSocket connection components
└── py.typed                       # Type checking marker

examples/                          # Examples of trading expert implementations
├── expert_binance_ema/            # EMA expert example for Binance
│   ├── main.py                    # Entry point for EMA example on Binance
│   ├── pyproject.toml             # Dependencies and settings for the example
│   ├── .env                       # Environment variables file (not in repo)
│   ├── .env.example               # Example .env file
│   └── README.md                  # Documentation for the example
├── expert_bybit_rsi/              # RSI expert example for Bybit
│   ├── main.py                    # Entry point for RSI example on Bybit
│   ├── pyproject.toml             # Dependencies and settings for the example
│   ├── .env                       # Environment variables file (not in repo)
│   ├── .env.example               # Example .env file
│   └── README.md                  # Documentation for the example
├── expert_okx_macd/               # MACD expert example for OKX
│   ├── main.py                    # Entry point for MACD example on OKX
│   ├── pyproject.toml             # Dependencies and settings for the example
│   ├── .env                       # Environment variables file (not in repo)
│   ├── .env.example               # Example .env file
│   └── README.md                  # Documentation for the example
└── README.md                      # General documentation for examples

tests/                             # Application tests
├── contract/                      # Contract tests (API verification)
├── integration/                   # Integration tests (module interaction)
└── unit/                          # Unit tests (individual component testing)

docs/                              # Application documentation
├── README.md                      # General documentation for the project
├── architecture.md                # System architecture overview
├── setup.md                       # Installation and setup instructions
├── usage.md                       # Usage guidelines and examples
├── api/                           # API documentation
├── guides/                        # Usage guides
└── tutorials/                     # Tutorials for using the system
```
