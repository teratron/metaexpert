# MetaExpert Logger Module

Производственная система логирования на основе `structlog` с поддержкой структурированных логов, управления контекстом и специализированных обработчиков.

## 🚀 Быстрый старт

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# 1. Инициализация (один раз при старте приложения)
config = LoggerConfig(log_level="INFO")
setup_logging(config)

# 2. Получение логгера в модуле
logger = get_logger(__name__)
logger.info("application started")

# 3. Логирование со структурированными данными
logger.info("trade executed", symbol="BTCUSDT", price=50000)
```

## 📁 Структура модуля

```text
logger/
├── __init__.py          # Публичный API
├── config.py            # Конфигурация (Pydantic)
├── setup.py             # Настройка structlog
├── processors.py        # Кастомные процессоры
├── formatters.py        # Форматтеры вывода
├── context.py           # Контекстные менеджеры
├── usage_guide.md       # Подробное руководство
├── migration_guide.md   # Руководство по миграции
└── performance_tips.md  # Советы по оптимизации
```

## 🎯 Основные возможности

### Структурированное логирование

```python
logger.info(
    "order placed",
    order_id="ORD123",
    symbol="BTCUSDT",
    price=50000,
    quantity=0.01
)
```

### Управление контекстом

```python
from metaexpert.logger import LogContext

with LogContext(strategy_id=1001, symbol="ETHUSDT"):
    logger.info("executing strategy")
    # Все логи включают strategy_id и symbol
```

### Постоянная привязка контекста

```python
logger = get_logger(__name__).bind(
    exchange="binance",
    market_type="futures"
)

logger.info("connected")  # Автоматически включает exchange и market_type
```

### Специализированное логирование торговли

```python
from metaexpert.logger import get_trade_logger, trade_context

trade_logger = get_trade_logger(strategy_id=1001)

with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info("trade executed", price=50000)
```

## 🔧 Конфигурация

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
    backup_count=5,  # Количество backup файлов
)
```

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

См. [migration_guide.md](migration_guide.md) для деталей.

## 🎨 Примеры для разных окружений

### Development

```python
config = LoggerConfig(
    log_level="DEBUG",
    use_colors=True,
    json_logs=False,
)
```

### Production

```python
config = LoggerConfig(
    log_level="WARNING",
    log_to_console=False,
    json_logs=True,
    max_bytes=50 * 1024 * 1024,
)
```

### Testing

```python
config = LoggerConfig(
    log_level="ERROR",
    log_to_console=False,
    log_dir=Path(tempfile.gettempdir()),
)
```

## 🐛 Проблемы и поддержка

При возникновении проблем см. документацию или создайте issue в репозитории проекта.

## 📄 Лицензия

См. LICENSE файл в корне проекта.
