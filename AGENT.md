# MetaExpert Project Context

## Project Overview

**MetaExpert** is a Python library for cryptocurrency trading that provides a unified interface for multiple exchanges and trading types. The system is designed to be modular, extensible, and easy to use while maintaining high performance and reliability. It currently supports major cryptocurrency exchanges including Binance, Bybit, OKX, Bitget, KuCoin, etc.

The project is built for Python 3.12+ and uses a unified interface for different trading types (spot, futures, options) and market modes (linear, inverse contracts). It supports paper trading, live trading, and backtesting modes.

The project follows a strict set of development principles outlined in the `constitution.md` file, which emphasizes a library-first architecture, mandatory Test-Driven Development (TDD), and adherence to SOLID, DRY, and KISS principles.

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

### Performance Benchmarks

All components must meet defined performance benchmarks: Maximum response times for user interactions (sub-200ms for simple operations), Efficient resource utilization (memory, CPU, network), Scalability under expected load conditions, Optimized algorithms and data structures for performance-critical paths.

### Quality Maintenance

Quality must be maintained throughout the development lifecycle: Automated quality checks on all commits, Regular refactoring to maintain code health, Continuous monitoring of performance metrics, Regular security assessments and updates.

### SOLID Principles

Classes, methods, functions and modules must follow the SOLID principles: Single Responsibility Principle (each class/module has one reason to change), Open/Closed Principle (software entities should be open for extension but closed for modification), Liskov Substitution Principle (objects should be replaceable with instances of their subtypes), Interface Segregation Principle (clients should not be forced to depend on interfaces they don't use), Dependency Inversion Principle (high-level modules should not depend on low-level modules, both should depend on abstractions).

### DRY Principle

"Do not Repeat Yourself" - Code duplication must be eliminated and each piece of knowledge must have a single authoritative representation in the system. All shared functionality must be extracted into reusable components, functions, or modules to ensure a single source of truth and reduce maintenance overhead.

### KISS Principle

"Keep It Simple, Stupid" - Code and architectural solutions must maintain simplicity and avoid unnecessary complexity. Before implementing complex solutions, evaluate if a simpler approach would be equally effective. Simple code is easier to understand, maintain, test, and debug.

### YAGNI Principle

"You Ain't Gonna Need It" - Only implement functionality that is currently needed, not anticipated future needs. Avoid adding features or infrastructure for potential future use cases that are not immediately required. This prevents code bloat and reduces maintenance burden.

### FSD Principle

"Feature-Sliced Design" - Architectural methodology for creating scalable applications with layer-based organization. Each feature should be implemented as a cohesive slice that spans all necessary layers (UI, business logic, data access), promoting better maintainability and clearer separation of concerns. This approach improves scalability and simplifies feature development, particularly for frontend applications.

### OOP Principle

"Object-Oriented Programming" - All code must follow OOP principles: Encapsulation to hide internal state and implementation details, Inheritance to promote code reuse and create hierarchical relationships, Polymorphism to allow objects of different types to be treated uniformly, and Abstraction to focus on behavior rather than implementation details. This ensures maintainable and scalable code design.

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
├── api/                           # API documentation
├── guides/                        # Usage guides
├── tutorials/                     # Tutorials for using the system
├── README.md                      # General documentation for the project
├── architecture.md                # System architecture overview
├── setup.md                       # Installation and setup instructions
├── usage.md                       # Usage guidelines and examples
└── [other docs]                   # Additional documentation files
```
