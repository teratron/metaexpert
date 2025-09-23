# Модуль логгера

## Описание

Модуль логгера предоставляет расширенные возможности логирования для торгового бота, включая структурированное логирование, асинхронное логирование и централизованную конфигурацию.

## Структура модуля

### [`__init__.py`](__init__.py)

Основной интерфейс модуля логгера. Предоставляет функции `setup_logger` и `get_logger` для настройки и получения экземпляров логгеров.

#### Функции интерфейса

- `setup_logger(name, level, structured, async_enabled, buffered)` - Настраивает и конфигурирует логгер с расширенными возможностями
- `get_logger(name)` - Получает экземпляр логгера из централизованного реестра

### [`async_log_handler.py`](async_log_handler.py)

Асинхронные обработчики логов, которые не блокируют основной поток выполнения.

#### Классы обработчиков

- `AsyncLogHandler` - Асинхронный обработчик логов
- `BufferedAsyncLogHandler` - Буферизованный асинхронный обработчик логов

### [`config.json`](config.json)

Файл конфигурации логгера в формате JSON. Определяет форматтеры, обработчики и логгеры.

### [`config.py`](config.py)

Python-файл конфигурации логгера. Предоставляет программный доступ к конфигурации и интеграцию с переменными окружения.

#### Функции конфигурации

- `get_logging_config()` - Получает текущую конфигурацию логгера
- `update_logging_config(new_config)` - Обновляет конфигурацию логгера
- `get_handler_config(handler_name)` - Получает конфигурацию конкретного обработчика
- `update_handler_config(handler_name, config)` - Обновляет конфигурацию конкретного обработчика

### [`logger_factory.py`](logger_factory.py)

Фабрика логгеров для создания и управления экземплярами логгеров.

#### Классы (Фабрика логгеров)

- `LoggerFactory` - Фабрика для создания и управления логгерами

#### Функции фабрики

- `get_logger(name, level, structured, async_enabled, buffered)` - Получает логгер с указанной конфигурацией
- `get_structured_logger(name, level)` - Получает структурированный логгер
- `get_async_logger(name, level, buffered)` - Получает асинхронный логгер
- `get_structured_async_logger(name, level, buffered)` - Получает структурированный асинхронный логгер

### [`logging_endpoint.py`](logging_endpoint.py)

Точка входа для настройки логгера через HTTP.

#### Функции

- `configure_logging_endpoint(request)` - Обрабатывает запросы на настройку логгера

### [`performance_monitor.py`](performance_monitor.py)

Монитор производительности для отслеживания и измерения производительности операций логирования.

#### Классы мониторинга

- `PerformanceMonitor` - Монитор производительности
- `PerformanceTimer` - Контекстный менеджер для тайминга операций

#### Функции мониторинга

- `get_performance_monitor()` - Получает глобальный экземпляр монитора производительности
- `start_operation(operation_name)` - Начинает тайминг операции
- `end_operation(operation_id, success)` - Завершает тайминг операции
- `record_metric(metric_name, value, tags)` - Записывает пользовательскую метрику
- `get_performance_report()` - Получает отчет о производительности
- `time_operation(operation_name)` - Декоратор для тайминга операций

### [`structured_log_formatter.py`](structured_log_formatter.py)

Форматировщики структурированных логов для вывода в форматах JSON и key-value.

#### Классы

- `StructuredLogFormatter` - Форматировщик JSON-логов
- `KeyValueLogFormatter` - Форматировщик key-value логов

## Уровни логирования

- `NOTSET` < `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`

- `DEBUG` - самая подробная информация, нужна только разработчику и только для отладки, например значения переменных, какие данные получены и т.д.
- `INFO` - информационные сообщения, как подтверждение работы, например запуск сервиса.
- `WARNING` - еще не ошибка, но уже надо посмотреть - мало места на диске, мало памяти, много созданных объектов и т.д.
- `ERROR` - приложение еще работает и может работать, но что-то пошло не так.
- `CRITICAL` - приложение не может работать дальше.

## Использование

### Базовое использование

```python
from metaexpert.logger import setup_logger, get_logger

# Настройка логгера
logger = setup_logger("my_app", level="INFO")

# Использование логгера
logger.info("Приложение запущено")
logger.warning("Предупреждение")
logger.error("Ошибка")
```

### Структурированное логирование

```python
from metaexpert.logger import setup_logger

# Настройка структурированного логгера
logger = setup_logger("my_app", level="INFO", structured=True)

# Использование логгера
logger.info("Сообщение со структурированными данными", extra={"user_id": 123, "action": "login"})
```

### Асинхронное логирование

```python
from metaexpert.logger import setup_logger

# Настройка асинхронного логгера
logger = setup_logger("my_app", level="INFO", async_enabled=True)

# Использование логгера
logger.info("Асинхронное сообщение")
```

### Буферизованное асинхронное логирование

```python
from metaexpert.logger import setup_logger

# Настройка буферизованного асинхронного логгера
logger = setup_logger("my_app", level="INFO", async_enabled=True, buffered=True)

# Использование логгера
logger.info("Буферизованное асинхронное сообщение")
