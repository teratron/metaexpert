# 📚 Руководство по использованию MetaExpert Logger

## 🎯 Основные принципы

### 1. Инициализация в точке входа приложения

```python
# src/metaexpert/__init__.py или main.py
from metaexpert.logger import LoggerConfig, setup_logging

def initialize_app():
    """Инициализация приложения."""
    # Настройка логирования
    config = LoggerConfig(
        log_level="INFO",
        log_to_console=True,
        log_to_file=True,
        use_colors=True,
        json_logs=False,  # True для production
    )
    setup_logging(config)
```

### 2. Использование в модулях

```python
# В любом модуле проекта
from metaexpert.logger import get_logger

# Получаем логгер для модуля
logger = get_logger(__name__)

def process_data():
    logger.info("processing started")
    logger.debug("debug information", extra_data="value")
```

---

## 🔥 Практические примеры

### Пример 1: Базовое логирование

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)

# Простое сообщение
logger.info("application started")

# Со структурированными данными
logger.info(
    "trade executed",
    symbol="BTCUSDT",
    side="BUY",
    price=50000,
    quantity=0.01
)

# Ошибка с исключением
try:
    risky_operation()
except Exception as e:
    logger.error("operation failed", exc_info=True)
```

### Пример 2: Контекстное логирование

```python
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__)

# Временный контекст для блока кода
with log_context(strategy_id=1001, symbol="ETHUSDT"):
    logger.info("strategy initialized")
    logger.info("executing trade")
    # Все логи включают strategy_id и symbol

# Контекст очищен
logger.info("outside context")
```

### Пример 3: Постоянное связывание контекста

```python
from metaexpert.logger import get_logger

# Создаем логгер с постоянным контекстом
logger = get_logger(__name__).bind(
    exchange="binance",
    market_type="futures"
)

# Весь последующий вывод включает exchange и market_type
logger.info("connected")
logger.info("subscribed to channel", channel="trades")
```

### Пример 4: Специализированное логирование торговли

```python
from metaexpert.logger import get_trade_logger, trade_context

# Логгер для торговых событий
trade_logger = get_trade_logger(strategy_id=1001)

# Контекст торговли с автоматической маркировкой
with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info(
        "trade executed",
        price=50000,
        order_id="abc123",
        commission=0.01
    )
    # Автоматически помечается как trade event
```

---

## 🏗️ Интеграция в MetaExpert

### В классе MetaExpert

```python
# src/metaexpert/__init__.py
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

class MetaExpert:
    def __init__(self, ...):
        # Настройка логирования при инициализации
        log_config = LoggerConfig(
            log_level=log_level,
            log_dir=Path("logs"),
            json_logs=structured_logging,
        )
        setup_logging(log_config)
        
        # Получаем логгер с контекстом
        self.logger = get_logger(__name__).bind(
            exchange=exchange,
            strategy_id=strategy_id
        )
        
        self.logger.info("expert initialized")
```

### В декораторах событий

```python
# src/metaexpert/core/events.py
from metaexpert.logger import get_logger, log_context

class Events:
    def on_init(self, ...):
        def decorator(func):
            def wrapper():
                logger = get_logger(__name__)
                
                with log_context(
                    event="on_init",
                    symbol=self.symbol,
                    timeframe=self.timeframe
                ):
                    logger.info("initializing strategy")
                    result = func()
                    logger.info("strategy initialized")
                
                return result
            return wrapper
        return decorator
```

### В обработке WebSocket

```python
# src/metaexpert/websocket/__init__.py
from metaexpert.logger import get_logger, bind_contextvars

class WebSocketClient:
    def __init__(self, url: str, name: str = "ws"):
        self.url = url
        self.name = name
        
        # Логгер с контекстом WebSocket
        self.logger = get_logger(__name__).bind(
            ws_name=name,
            ws_url=url
        )
    
    async def connect(self):
        # Привязываем connection_id к контексту
        bind_contextvars(connection_id=self._generate_connection_id())
        
        try:
            self.logger.info("connecting to websocket")
            # ... connection logic ...
            self.logger.info("connected successfully")
        except Exception as e:
            self.logger.error("connection failed", exc_info=True)
```

---

## 🎨 Продвинутые паттерны

### Паттерн 1: Логирование жизненного цикла

```python
from metaexpert.logger import get_logger
from contextlib import contextmanager

logger = get_logger(__name__)

@contextmanager
def lifecycle_logging(operation: str):
    """Автоматическое логирование начала и конца операции."""
    logger.info(f"{operation} started")
    try:
        yield
        logger.info(f"{operation} completed successfully")
    except Exception as e:
        logger.error(f"{operation} failed", exc_info=True)
        raise

# Использование
with lifecycle_logging("backtesting"):
    run_backtest()
```

### Паттерн 2: Метрики производительности

```python
from metaexpert.logger import get_logger
import time

logger = get_logger(__name__)

class PerformanceLogger:
    """Логирование метрик производительности."""
    
    def __init__(self, operation: str):
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.debug(f"{self.operation} starting")
        return self
    
    def __exit__(self, *args):
        duration = time.time() - self.start_time
        logger.info(
            f"{self.operation} completed",
            duration_ms=round(duration * 1000, 2),
            operation=self.operation
        )

# Использование
with PerformanceLogger("data_processing"):
    process_large_dataset()
```

### Паттерн 3: Иерархическое логирование

```python
from metaexpert.logger import get_logger

class TradingStrategy:
    def __init__(self, strategy_id: int, name: str):
        # Создаем иерархию логгеров
        self.logger = get_logger(f"strategy.{name}").bind(
            strategy_id=strategy_id,
            strategy_name=name
        )
        
        # Под-логгеры для различных компонентов
        self.risk_logger = self.logger.bind(component="risk_manager")
        self.entry_logger = self.logger.bind(component="entry_signals")
        self.exit_logger = self.logger.bind(component="exit_signals")
    
    def check_risk(self):
        self.risk_logger.info("checking risk parameters")
    
    def generate_signal(self):
        self.entry_logger.info("signal generated", signal_type="LONG")
```

### Паттерн 4: Асинхронное логирование

```python
from metaexpert.logger import get_logger
import asyncio

logger = get_logger(__name__)

async def process_trades():
    """Асинхронная обработка с логированием."""
    logger.info("starting async processing")
    
    tasks = []
    for symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]:
        task = asyncio.create_task(
            process_symbol(symbol)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for symbol, result in zip(["BTCUSDT", "ETHUSDT", "BNBUSDT"], results):
        if isinstance(result, Exception):
            logger.error(
                "symbol processing failed",
                symbol=symbol,
                exc_info=result
            )
        else:
            logger.info("symbol processed", symbol=symbol, result=result)

async def process_symbol(symbol: str):
    # Каждая задача имеет свой контекст
    logger_with_ctx = logger.bind(symbol=symbol)
    logger_with_ctx.info("processing started")
    await asyncio.sleep(1)
    logger_with_ctx.info("processing completed")
```

---

## 🔧 Конфигурация для разных окружений

### Development (разработка)

```python
from metaexpert.logger import LoggerConfig, setup_logging

config = LoggerConfig(
    log_level="DEBUG",
    log_to_console=True,
    log_to_file=True,
    use_colors=True,
    json_logs=False,  # Читаемый формат
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=3,
)
setup_logging(config)
```

### Production (продакшн)

```python
from metaexpert.logger import LoggerConfig, setup_logging
from pathlib import Path

config = LoggerConfig(
    log_level="INFO",
    log_to_console=False,  # Только файлы
    log_to_file=True,
    use_colors=False,
    json_logs=True,  # Структурированные логи для анализа
    log_dir=Path("/var/log/metaexpert"),
    max_bytes=50 * 1024 * 1024,  # 50MB
    backup_count=10,
)
setup_logging(config)
```

### Testing (тестирование)

```python
from metaexpert.logger import LoggerConfig, setup_logging
import tempfile

config = LoggerConfig(
    log_level="WARNING",  # Только важные сообщения
    log_to_console=False,
    log_to_file=True,
    log_dir=Path(tempfile.gettempdir()) / "test_logs",
    json_logs=False,
)
setup_logging(config)
```

---

## 📊 Структурированное логирование для анализа

### JSON логи для ELK Stack / Datadog

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)

# Богатые структурированные данные
logger.info(
    "trade_executed",
    event_type="trade",
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.01,
    price=50000,
    commission=0.5,
    commission_asset="USDT",
    strategy_id=1001,
    execution_time_ms=45,
    slippage_pct=0.02,
    timestamp=datetime.now().isoformat(),
)

# Результат в JSON:
# {
#   "event": "trade_executed",
#   "timestamp": "2025-10-22T15:30:00.123Z",
#   "level": "info",
#   "logger": "trading.executor",
#   "symbol": "BTCUSDT",
#   "side": "BUY",
#   ...
# }
```

---

## 🚨 Обработка ошибок

### Правильное логирование исключений

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)

# ✅ ПРАВИЛЬНО: С exc_info=True
try:
    dangerous_operation()
except ValueError as e:
    logger.error(
        "validation failed",
        exc_info=True,  # Включает полный traceback
        input_value=value,
        expected_type="float"
    )

# ✅ ПРАВИЛЬНО: С exception в контексте
try:
    api_call()
except APIError as e:
    logger.error(
        "api call failed",
        error_code=e.code,
        error_message=str(e),
        exc_info=True
    )

# ❌ НЕПРАВИЛЬНО: Потеря информации
try:
    something()
except Exception as e:
    logger.error(f"Error: {e}")  # Нет traceback!
```

---

## 🎯 Best Practices

### 1. Используйте правильные уровни

```python
logger = get_logger(__name__)

# DEBUG - детальная отладочная информация
logger.debug("processing item", item_id=123, step="validation")

# INFO - важные события в нормальном потоке
logger.info("user logged in", user_id=456, session_id="abc")

# WARNING - что-то необычное, но не ошибка
logger.warning("cache miss", key="user:789", fallback="database")

# ERROR - ошибка, требующая внимания
logger.error("database connection failed", exc_info=True)

# CRITICAL - критическая ошибка, система не работает
logger.critical("out of memory", available_mb=10)
```

### 2. Структурируйте данные

```python
# ✅ ПРАВИЛЬНО: Структурированные данные
logger.info(
    "order placed",
    order_id="ORD123",
    symbol="BTCUSDT",
    price=50000,
    quantity=0.01
)

# ❌ НЕПРАВИЛЬНО: Всё в строке
logger.info(f"Order ORD123 for BTCUSDT at 50000, qty 0.01")
```

### 3. Используйте контекст для общих данных

```python
# ✅ ПРАВИЛЬНО: Контекст один раз
logger = get_logger(__name__).bind(
    user_id=user_id,
    session_id=session_id
)

logger.info("action 1")
logger.info("action 2")
logger.info("action 3")

# ❌ НЕПРАВИЛЬНО: Повторение
logger.info("action 1", user_id=user_id, session_id=session_id)
logger.info("action 2", user_id=user_id, session_id=session_id)
```

### 4. Не логируйте чувствительные данные

```python
# ❌ ОПАСНО: Секреты в логах
logger.info("connecting", api_key=api_key, api_secret=api_secret)

# ✅ БЕЗОПАСНО: Маскируйте чувствительные данные
logger.info(
    "connecting",
    api_key_prefix=api_key[:8] + "...",
    api_secret="***"
)
```

---

## 🧪 Тестирование с логами

```python
import pytest
from metaexpert.logger import setup_logging, LoggerConfig, get_logger
import tempfile

@pytest.fixture(scope="session")
def configure_test_logging():
    """Настройка логирования для тестов."""
    config = LoggerConfig(
        log_level="WARNING",
        log_to_console=False,
        log_to_file=True,
        log_dir=Path(tempfile.gettempdir()),
    )
    setup_logging(config)

def test_trading_logic(configure_test_logging):
    """Тест с логированием."""
    logger = get_logger(__name__)
    logger.info("test started")
    
    # Ваша логика
    assert True
    
    logger.info("test passed")
```

---

## 📈 Мониторинг и метрики

### Интеграция с Prometheus

```python
from metaexpert.logger import get_logger
from prometheus_client import Counter, Histogram

logger = get_logger(__name__)

# Метрики
trades_total = Counter("trades_total", "Total trades", ["symbol", "side"])
trade_duration = Histogram("trade_duration_seconds", "Trade execution time")

def execute_trade(symbol: str, side: str):
    with trade_duration.time():
        logger.info("executing trade", symbol=symbol, side=side)
        
        # ... торговая логика ...
        
        trades_total.labels(symbol=symbol, side=side).inc()
        logger.info("trade completed", symbol=symbol, side=side)
```

---

## 🔍 Дебаг и траблшутинг

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)

# Добавьте callsite info для дебага
logger = logger.bind(
    filename=__file__,
    function=inspect.currentframe().f_code.co_name
)

logger.debug(
    "detailed debug info",
    local_vars=locals(),
    stack_depth=len(inspect.stack())
)
```
