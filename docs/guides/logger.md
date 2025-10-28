# Логирование в MetaExpert

## Обзор

Система логирования MetaExpert основана на библиотеке `structlog` и предоставляет мощные возможности для структурированного логирования, управления контекстом и специализированные обработчики для трейдинга. Система обеспечивает надежное ведение журналов как для разработки, так и для продакшена, с акцентом на безопасность и производительность.

## Основные возможности

### Структурированное логирование

Система поддерживает структурированное логирование, позволяя добавлять произвольные данные к сообщениям:

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)
logger.info(
    "order placed",
    order_id="ORD123",
    symbol="BTCUSDT",
    price=50000,
    quantity=0.01,
    exchange="binance"
)
```

### Управление контекстом

Система предоставляет несколько способов управления контекстом логирования:

#### Временный контекст с LogContext

```python
from metaexpert.logger import LogContext, get_logger

logger = get_logger(__name__)

with LogContext(strategy_id=1001, symbol="ETHUSDT"):
    logger.info("executing strategy")
    # Все логи в этом блоке будут содержать strategy_id и symbol
    logger.info("position opened", side="BUY", price=2500)
```

#### Постоянное связывание контекста

```python
logger = get_logger(__name__).bind(
    exchange="binance",
    market_type="futures"
)

logger.info("connected")  # Автоматически включает exchange и market_type
```

#### Специализированный логгер для трейдинга

```python
from metaexpert.logger import get_trade_logger

trade_logger = get_trade_logger(strategy_id=1001)

with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info("trade executed", price=50000)
```

## Конфигурация логирования

### Основные параметры конфигурации

Класс `LoggerConfig` использует Pydantic для валидации конфигурации:

```python
from metaexpert.logger import LoggerConfig
from pathlib import Path

config = LoggerConfig(
    log_level="INFO",           # Уровень логирования
    log_to_console=True,        # Вывод в консоль
    log_to_file=True,           # Вывод в файлы
    use_colors=True,            # Цветной вывод в консоли
    json_logs=False,            # JSON формат (рекомендуется для продакшена)
    log_dir=Path("logs"),       # Директория для файлов логов
    log_file="metaexpert.log",  # Имя основного файла логов
    trade_log_file="trades.log", # Имя файла для трейдинг логов
    error_log_file="errors.log", # Имя файла для ошибок
    max_bytes=10 * 1024 * 1024, # Максимальный размер файла до ротации (10MB)
    backup_count=5,             # Количество файлов резервных копий
    cache_logger_on_first_use=True # Кэширование логгеров для производительности
)
```

### Пресеты конфигурации

Для удобства система предоставляет предопределенные пресеты для разных сред:

#### Development Preset

```python
from metaexpert.logger import LoggerConfig

# Подробное логирование с цветами, удобное для разработки
config = LoggerConfig.for_development()
# Эквивалентно:
# config = LoggerConfig(
#     log_level="DEBUG",
#     use_colors=True,
#     json_logs=False,
#     log_to_console=True,
#     log_to_file=True
# )
```

#### Production Preset

```python
# Минималистичное логирование, JSON формат, без цветов
config = LoggerConfig.for_production()
# Эквивалентно:
# config = LoggerConfig(
#     log_level="WARNING",
#     use_colors=False,
#     json_logs=True,
#     log_to_console=False,
#     log_to_file=True
# )
```

#### Backtesting Preset

```python
# Оптимизированное логирование для симуляций
config = LoggerConfig.for_backtesting()
# Эквивалентно:
# config = LoggerConfig(
#     log_level="INFO",
#     use_colors=False,
#     json_logs=True,
#     log_to_console=False,
#     log_to_file=True
# )
```

### Валидация конфигурации

Конфигурация автоматически проверяется на корректность:

- Максимальный размер файла не может превышать 1GB
- Директория логов создается автоматически при необходимости
- Должен быть включен хотя бы один метод вывода (консоль или файл)
- Конфигурация неизменяема после создания (frozen=True)

## Инициализация системы логирования

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Инициализация (один раз при запуске приложения)
config = LoggerConfig.for_production()
setup_logging(config)

# Получение логгера в модуле
logger = get_logger(__name__)
logger.info("application started")
```

## Безопасность

### Фильтрация чувствительных данных

Система автоматически фильтрует чувствительные данные, чтобы предотвратить их попадание в логи:

```python
# Эти данные будут автоматически замаскированы
logger.info("api call", api_key="secret12345")  # В логе: api_key="***345"
logger.info("auth", token="mytoken12345")       # В логе: token="***345"
logger.info("connect", password="mypass")       # В логе: password="***"
```

Автоматически фильтруемые ключи данных:

- `password`, `token`, `api_key`, `secret`, `private_key`
- `apikey`, `api_secret`, `access_token`, `refresh_token`

## Мониторинг производительности

### Измерение времени операций

Для мониторинга производительности используется контекстный менеджер `TimedOperation`:

```python
from metaexpert.logger import get_logger, TimedOperation

logger = get_logger(__name__)

# Измерение времени выполнения операции
with TimedOperation(logger, "fetch_data", threshold_ms=1000):
    data = fetch_expensive_data()  # Время выполнения будет залогировано
```

Это позволяет:

- Автоматически измерять время выполнения операций
- Выдавать предупреждения для операций, превышающих пороговое значение
- Записывать время выполнения в логи для анализа

### Мониторинг медленных операций

Система включает в себя `PerformanceMonitor`, который отслеживает медленные операции и выдает предупреждения:

```python
# Медленные операции (превышающие порог) будут отмечены
# Порог по умолчанию 100мс, можно настроить при создании
```

## Контекстные менеджеры

### TradeContext

Специализированный контекстный менеджер для трейдинга:

```python
from metaexpert.logger import TradeContext

with TradeContext(symbol="BTCUSDT", side="BUY", quantity=0.01) as ctx:
    # Автоматически логируется начало трейда
    # Измеряется время выполнения
    logger.info("executing trade", price=500)
    
    # Установка результата трейда
    ctx.set_result(filled=0.01, avg_price=50123.45)
    
    # Добавление промежуточной заметки
    ctx.add_note("order submitted", order_id="12345")
```

### IterateWithContext

Итерация с привязкой контекста для каждого элемента:

```python
from metaexpert.logger import iterate_with_context

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

for symbol in iterate_with_context(symbols, strategy_id=1001):
    logger.info("processing", symbol=symbol)
    # Каждый лог будет содержать strategy_id=1001
```

## Практические примеры

### Пример использования в трейдинг-боте

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig, LogContext

# Инициализация логирования
config = LoggerConfig.for_production()
setup_logging(config)

class TradingBot:
    def __init__(self, strategy_id: int):
        self.logger = get_logger(self.__class__.__name__).bind(
            strategy_id=strategy_id
        )
        self.strategy_id = strategy_id
    
    def execute_trade(self, symbol: str, side: str, quantity: float):
        with LogContext(symbol=symbol, side=side, quantity=quantity) as ctx:
            self.logger.info("starting trade execution")
            
            # Выполнение трейда
            result = self._place_order(symbol, side, quantity)
            
            if result.success:
                self.logger.info("trade executed", **result.data)
            else:
                self.logger.error("trade failed", error=result.error)
            
            return result
    
    def _place_order(self, symbol: str, side: str, quantity: float):
        # Логика размещения ордера
        pass
```

### Пример использования в backtesting

```python
from metaexpert.logger import setup_logging, LoggerConfig

# Использование пресета для бэктестинга
config = LoggerConfig.for_backtesting()
setup_logging(config)

def run_backtest(data, strategy):
    logger = get_logger(__name__)
    
    logger.info("starting backtest", 
                strategy=strategy.name, 
                start_date=data.start_date, 
                end_date=data.end_date)
    
    # Выполнение бэктеста
    results = strategy.run(data)
    
    logger.info("backtest completed", 
                total_trades=results.total_trades,
                profit=results.total_profit,
                max_drawdown=results.max_drawdown)
    
    return results
```

## Лучшие практики

1. Используйте структурированное логирование с понятными ключами данных
2. Применяйте контекстное управление для корреляции связанных событий
3. Используйте соответствующие пресеты конфигурации для разных сред
4. Не логируйте чувствительные данные напрямую
5. Используйте `TimedOperation` для измерения производительности критических операций
6. Применяйте соответствующие уровни логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
