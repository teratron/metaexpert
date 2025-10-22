# ⚡ Оптимизация производительности логгера

## 🎯 Ключевые принципы

### 1. Ленивое вычисление дорогих операций

```python
from metaexpert.logger import get_logger

logger = get_logger(__name__)

# ❌ ПЛОХО: Всегда вычисляется
logger.debug(f"Data: {expensive_computation()}")

# ✅ ХОРОШО: Вычисляется только если DEBUG включен
logger.debug("data computed", data=lambda: expensive_computation())

# ✅ ХОРОШО: Проверка уровня логирования
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("data computed", data=expensive_computation())
```

### 2. Кэширование логгеров

```python
# ✅ ХОРОШО: Создаем логгер один раз на модуль
logger = get_logger(__name__)

class MyClass:
    def method1(self):
        # Используем кэшированный логгер
        logger.info("method1 called")
    
    def method2(self):
        logger.info("method2 called")

# ❌ ПЛОХО: Создаем логгер каждый раз
class BadClass:
    def method(self):
        get_logger(__name__).info("method called")  # Overhead!
```

### 3. Минимизация строковых операций

```python
# ❌ ПЛОХО: f-strings всегда вычисляются
logger.debug(f"Processing {item.id} with {len(data)} items")

# ✅ ХОРОШО: Ленивая интерполяция
logger.debug("processing item", item_id=item.id, data_count=len(data))
```

---

## 📊 Профилирование логирования

### Измерение влияния на производительность

```python
import cProfile
import pstats
from metaexpert.logger import get_logger

logger = get_logger(__name__)

def log_intensive_function():
    """Функция с большим количеством логирования."""
    for i in range(10000):
        logger.debug("iteration", count=i, data={"key": "value"})

# Профилирование
profiler = cProfile.Profile()
profiler.enable()

log_intensive_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Бенчмарк различных подходов

```python
import timeit
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__)

# Тест 1: Простое логирование
time1 = timeit.timeit(
    'logger.info("message")',
    globals={"logger": logger},
    number=10000
)

# Тест 2: С параметрами
time2 = timeit.timeit(
    'logger.info("message", key1="value1", key2="value2")',
    globals={"logger": logger},
    number=10000
)

# Тест 3: С контекстом
time3 = timeit.timeit(
    '''
with log_context(key1="value1", key2="value2"):
    logger.info("message")
    ''',
    globals={"logger": logger, "log_context": log_context},
    number=10000
)

print(f"Простое: {time1:.4f}s")
print(f"С параметрами: {time2:.4f}s ({time2/time1:.2f}x)")
print(f"С контекстом: {time3:.4f}s ({time3/time1:.2f}x)")
```

---

## 🔧 Оптимизация конфигурации

### Production конфигурация для максимальной производительности

```python
from metaexpert.logger import LoggerConfig, setup_logging

config = LoggerConfig(
    log_level="WARNING",  # Меньше логов = больше скорость
    log_to_console=False,  # Файлы быстрее консоли
    log_to_file=True,
    json_logs=True,  # JSON быстрее форматирования текста
    max_bytes=100 * 1024 * 1024,  # Реже ротация
