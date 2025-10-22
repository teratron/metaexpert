# 🔄 Руководство по миграции с старого Logger на новый

## 📋 Пошаговая миграция

### Шаг 1: Удалить старые файлы

Удалите следующие файлы из `src/metaexpert/logger/`:

- `async_handler.py` (больше не нужен)
- Старые части `__init__.py`

### Шаг 2: Обновить импорты во всем проекте

#### Было (старый код)

```python
from metaexpert.logger import MetaLogger, BoundLogger

logger: BoundLogger = MetaLogger.create(
    log_level="INFO",
    log_file="expert.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    console_logging=True,
    structured_logging=False,
    async_logging=True,
)
```

#### Стало (новый код)

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Один раз при инициализации
config = LoggerConfig(
    log_level="INFO",
    log_file="expert.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    log_to_console=True,
    json_logs=False,
)
setup_logging(config)

# В каждом модуле
logger = get_logger(__name__)
```

---

## 🔧 Миграция класса MetaExpert

### Было

```python
class MetaExpert(Events):
    def __init__(self, ...):
        self.logger: BoundLogger = MetaLogger.create(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            console_logging=log_to_console,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )
        
        self.logger.info("Starting expert on %s", exchange)
```

### Стало

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

class MetaExpert(Events):
    def __init__(self, ...):
        # Настраиваем логирование один раз
        config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_to_console=log_to_console,
            json_logs=structured_logging,
        )
        setup_logging(config)
        
        # Получаем логгер с контекстом
        self.logger = get_logger(__name__).bind(
            exchange=exchange,
            market_type=market_type,
        )
        
        self.logger.info("starting expert", exchange=exchange)
```

---

## 🔄 Миграция различных паттернов

### 1. Специализированные логгеры

#### Было

```python
main_logger = logger.get_main_logger()
trade_logger = logger.get_trade_logger()
error_logger = logger.get_error_logger()

main_logger.info("App started")
trade_logger.info("Trade executed", symbol="BTCUSDT")
error_logger.error("Error occurred", exception=e)
```

#### Стало

```python
from metaexpert.logger import get_logger, get_trade_logger

logger = get_logger(__name__)
trade_logger = get_trade_logger(strategy_id=1001)

logger.info("app started")
trade_logger.info("trade executed", symbol="BTCUSDT", price=50000)
logger.error("error occurred", exc_info=True)
```

### 2. Метод log_trade

#### Было

```python
logger.log_trade(
    "Trade executed successfully",
    symbol="BTC/USDT",
    price=60000,
    quantity=0.01
)
```

#### Стало

```python
from metaexpert.logger import get_trade_logger, trade_context

trade_logger = get_trade_logger()

with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info("trade executed", price=60000)
```

### 3. Метод log_error

#### Было

```python
logger.log_error("An error occurred", exception=e, user_id=123)
```

#### Стало

```python
logger.error("an error occurred", user_id=123, exc_info=True)
```

---

## 📦 Миграция в других модулях

### В `src/metaexpert/core/_bar.py`

#### Было

```python
from metaexpert.logger import BoundLogger, get_logger

class Bar:
    def __init__(self, ...):
        self.logger: BoundLogger = get_logger("Bar")
    
    async def start(self) -> None:
        self.logger.debug("Bar with timeframe %s started.", self._timeframe)
```

#### Стало

```python
from metaexpert.logger import get_logger

class Bar:
    def __init__(self, ...):
        self.logger = get_logger(__name__).bind(
            component="Bar",
            timeframe=timeframe
        )
    
    async def start(self) -> None:
        self.logger.debug("bar started")
```

### В `src/metaexpert/core/_timer.py`

#### Было

```python
from metaexpert.logger import BoundLogger, get_logger

class Timer:
    def __init__(self, interval: float, callback: Callable | None = None):
        self.logger: BoundLogger = get_logger("Timer")
        self.logger.debug("Timer with interval %.1f seconds started.", self._interval)
```

#### Стало

```python
from metaexpert.logger import get_logger

class Timer:
    def __init__(self, interval: float, callback: Callable | None = None):
        self.logger = get_logger(__name__).bind(
            component="Timer",
            interval=interval
        )
        self.logger.debug("timer started")
```

### В `src/metaexpert/websocket/__init__.py`

#### Было

```python
from metaexpert.logger import BoundLogger, get_logger

class WebSocketClient:
    def __init__(self, url: str, name: str = "ws"):
        self.logger: BoundLogger = get_logger("WebSocketClient")
        self.logger.info("Connected to {url}", url=self.url, name=self.name)
```

#### Стало

```python
from metaexpert.logger import get_logger

class WebSocketClient:
    def __init__(self, url: str, name: str = "ws"):
        self.logger = get_logger(__name__).bind(
            component="WebSocketClient",
            ws_name=name,
            ws_url=url
        )
        self.logger.info("connected to websocket")
```

---

## 🧹 Очистка устаревшего кода

### Удалить из `pyproject.toml`

- Не нужно, `structlog` уже в зависимостях ✅

### Обновить в `config.py`

#### Было

```python
LOG_ASYNC_LOGGING: bool = False
LOG_STRUCTURED_LOGGING: bool = False
```

#### Стало

```python
# Эти настройки теперь в LoggerConfig
# LOG_ASYNC_LOGGING больше не нужен
LOG_JSON_LOGS: bool = False  # Переименован из STRUCTURED_LOGGING
```

---

## ✅ Чек-лист миграции

- [ ] Удалить `async_handler.py`
- [ ] Заменить все импорты `MetaLogger` на `setup_logging` + `get_logger`
- [ ] Обновить инициализацию в `MetaExpert.__init__`
- [ ] Заменить `get_main_logger()` на `get_logger(__name__)`
- [ ] Заменить `get_trade_logger()` на новый API
- [ ] Заменить `log_trade()` на `get_trade_logger().info()`
- [ ] Заменить `log_error()` на `logger.error(exc_info=True)`
- [ ] Обновить все классы с `BoundLogger` на `get_logger(__name__)`
- [ ] Добавить `.bind()` для постоянного контекста
- [ ] Использовать `log_context` для временного контекста
- [ ] Обновить тесты для работы с новым логгером
- [ ] Проверить, что логи пишутся корректно
- [ ] Обновить документацию

---

## 🧪 Тестирование после миграции

```python
import pytest
from metaexpert.logger import setup_logging, get_logger, LoggerConfig
from pathlib import Path
import tempfile

def test_new_logger():
    """Проверка нового логгера."""
    # Настройка
    test_dir = Path(tempfile.gettempdir()) / "test_logs"
    config = LoggerConfig(
        log_level="INFO",
        log_dir=test_dir,
        log_to_console=False,
        log_to_file=True,
    )
    setup_logging(config)
    
    # Использование
    logger = get_logger(__name__)
    logger.info("test message", test_value=123)
    
    # Проверка
    log_file = test_dir / "expert.log"
    assert log_file.exists()
    
    content = log_file.read_text()
    assert "test message" in content
    assert "test_value" in content
```

---

## 📊 Сравнение производительности

### Старый код

- Много ручного управления handlers
- AsyncHandler добавляет overhead
- Дублирование конфигурации

### Новый код

- Меньше кода, проще поддержка
- Нативная производительность structlog
- Единая точка конфигурации
- Лучшая интеграция со стандартным logging

### Бенчмарк

```python
import timeit

# Старый подход
old_time = timeit.timeit(
    "logger.info('test', key='value')",
    setup="from old_logger import get_old_logger; logger = get_old_logger()",
    number=10000
)

# Новый подход
new_time = timeit.timeit(
    "logger.info('test', key='value')",
    setup="from metaexpert.logger import get_logger; logger = get_logger(__name__)",
    number=10000
)

print(f"Старый: {old_time:.4f}s")
print(f"Новый: {new_time:.4f}s")
print(f"Улучшение: {((old_time - new_time) / old_time * 100):.1f}%")
```

---

## 🎯 Итоговые преимущества

### ✅ Что улучшилось

1. **Простота** - меньше кода, понятнее API
2. **Производительность** - нативный structlog без лишних слоев
3. **Гибкость** - мощный context management
4. **Стандартность** - идиоматичное использование structlog
5. **Поддержка** - проще добавлять новые возможности
6. **Тестируемость** - легче писать тесты

### 🎨 Новые возможности

- Контекстные менеджеры (`log_context`, `trade_context`)
- Привязка постоянного контекста (`.bind()`)
- Специализированные процессоры
- Кастомные форматтеры
- Лучшая интеграция с async/await
- JSON логи для production
- Цветной вывод в консоль

### 🚀 Рекомендации

1. Мигрируйте постепенно, модуль за модулем
2. Начните с точки входа (`MetaExpert.__init__`)
3. Обновите тесты параллельно
4. Используйте контекст вместо повторения параметров
5. Настройте JSON логи для production
6. Добавьте метрики через структурированные логи
