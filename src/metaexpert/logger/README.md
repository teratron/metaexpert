# MetaExpert Logger Module

Production logging system based on `structlog` with support for structured logging, context management, and specialized handlers.

## 🚀 Quick Start

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# 1. Initialization (once at application startup)
config = LoggerConfig(log_level="INFO")
setup_logging(config)

# 2. Get logger in module
logger = get_logger(__name__)
logger.info("application started")

# 3. Logging with structured data
logger.info("trade executed", symbol="BTCUSDT", price=50000)
```

## 📁 Module Structure

```text
logger/
├── __init__.py          # Public API
├── config.py            # Configuration (Pydantic)
├── setup.py             # structlog setup
├── processors.py        # Custom processors
├── formatters.py        # Output formatters
├── context.py           # Context managers
├── usage_guide.md       # Detailed guide
├── migration_guide.md   # Migration guide
└── performance_tips.md  # Performance tips
```

## 🎯 Main Features

### Structured Logging

```python
logger.info(
    "order placed",
    order_id="ORD123",
    symbol="BTCUSDT",
    price=50000,
    quantity=0.01
)
```

### Context Management

```python
from metaexpert.logger import LogContext

with LogContext(strategy_id=1001, symbol="ETHUSDT"):
    logger.info("executing strategy")
    # All logs include strategy_id and symbol
```

### Persistent Context Binding

```python
logger = get_logger(__name__).bind(
    exchange="binance",
    market_type="futures"
)

logger.info("connected")  # Automatically includes exchange and market_type
```

### Specialized Trading Logging

```python
from metaexpert.logger import get_trade_logger, trade_context

trade_logger = get_trade_logger(strategy_id=1001)

with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info("trade executed", price=50000)
```

## 🔧 Конфигурация

### Configuration Validation

The `LoggerConfig` class uses Pydantic for validation, ensuring that all configuration parameters are correct before logging is set up:

```python
from metaexpert.logger import LoggerConfig

config = LoggerConfig(
    log_level="INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_to_console=True,  # Вывод в консоль
    log_to_file=True,  # Вывод в файлы
    use_colors=True,  # Цветной вывод
    json_logs=False,  # JSON формат (для production)
    log_dir=Path("logs"),  # Директория логов
    max_bytes=10 * 1024 * 1024,  # Размер файла перед ротацией
    backup_count=5,  # Количество backup файлов,
)
```

Validation includes:

- File size limits (max 1GB)
- Directory creation if it doesn't exist
- At least one output method (console or file) required
- Immutable configuration after creation

### Configuration Presets

The logger provides pre-configured presets for different environments:

```python
from metaexpert.logger import LoggerConfig

# Development preset: verbose logging with colors
dev_config = LoggerConfig.for_development()

# Production preset: minimal logging, JSON format, no colors
prod_config = LoggerConfig.for_production()

# Backtesting preset: optimized for backtesting scenarios
backtest_config = LoggerConfig.for_backtesting()
```

### Configuration Preset Details

#### Development Preset

```python
config = LoggerConfig.for_development()
# Equivalent to:
# log_level="DEBUG"
# use_colors=True
# json_logs=False
# log_to_console=True
# log_to_file=True
```

#### Production Preset

```python
config = LoggerConfig.for_production()
# Equivalent to:
# log_level="WARNING"
# use_colors=False
# json_logs=True
# log_to_console=False
# log_to_file=True
```

#### Backtesting Preset

```python
config = LoggerConfig.for_backtesting()
# Equivalent to:
# log_level="INFO"
# use_colors=False
# json_logs=True
# log_to_console=False
# log_to_file=True
```

## 🛡️ Security Features

### Sensitive Data Filtering

The logging system includes automatic filtering of sensitive data to prevent API keys, passwords, and other confidential information from being logged:

```python
# This will automatically mask sensitive data
logger.info("api call", api_key="secret12345")  # Logs as api_key="***345"
logger.info("auth", token="mytoken12345")       # Logs as token="***345"
```

Sensitive keys that are automatically filtered include:

- `password`, `token`, `api_key`, `secret`, `private_key`
- `apikey`, `api_secret`, `access_token`, `refresh_token`

## ⚡ Performance Monitoring

### Performance Monitoring

The system includes performance monitoring capabilities that can detect slow operations:

```python
from metaexpert.logger import TimedOperation

logger = get_logger(__name__)
with TimedOperation(logger, "fetch_data", threshold_ms=1000):
    data = fetch_expensive_data()  # Operation timing will be logged
```

Performance monitoring features:

- Automatic detection of slow operations based on threshold
- Logging of operation duration
- Warning for operations that exceed the defined threshold

## 📚 Документация

- **[usage_guide.md](usage_guide.md)** - Подробное руководство с примерами
- **[migration_guide.md](migration_guide.md)** - Миграция со старого логгера
- **[performance_tips.md](performance_tips.md)** - Оптимизация производительности

## 🔄 Миграция со старого логгера

```python
# Было
from metaexpert.logger import MetaLogger

logger = MetaLogger.create(log_level="INFO", ...)

# Стало
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

config = LoggerConfig(log_level="INFO")
setup_logging(config)
logger = get_logger(__name__)
```

See [migration_guide.md](migration_guide.md) for details.

## 🎨 Examples for Different Environments

### Development

```python
config = LoggerConfig.for_development()
# Or customize:
# config = LoggerConfig(
#     log_level="DEBUG",
#     use_colors=True,
#     json_logs=False,
# )
```

### Production

```python
config = LoggerConfig.for_production()
# Or customize:
# config = LoggerConfig(
#     log_level="WARNING",
#     log_to_console=False,
#     json_logs=True,
#     max_bytes=50 * 1024 * 1024,
# )
```

### Backtesting

```python
config = LoggerConfig.for_backtesting()
# Or customize:
# config = LoggerConfig(
#     log_level="INFO",
#     use_colors=False,
#     json_logs=True,
#     log_to_console=False,
# )
```

## 🐛 Issues and Support

When encountering problems, see the documentation or create an issue in the project repository.

## 📄 License

See the LICENSE file in the root of the project.
