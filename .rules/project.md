# Анализ кодовой базы: MetaExpert

## 📁 Структура проекта

```
metaexpert/
├── .env.example             # Пример файла переменных окружения
├── .gitattributes           # Настройки Git
├── .gitignore               # Игнорируемые файлы Git
├── .python-version          # Версия Python
├── LICENSE                  # Лицензия проекта
├── pyproject.toml           # Конфигурация проекта и зависимости
├── README.md                # Основное описание проекта
├── docs/                    # Документация проекта
│   ├── README.md            # Основная документация
│   ├── api/                 # API документация
│   ├── guides/              # Руководства
│   └── tutorials/           # Учебные материалы
├── examples/                # Примеры использования
│   ├── README.md            # Описание примеров
│   ├── expert_binance_ema/  # Пример EMA стратегии для Binance
│   ├── expert_bybit_rsi/    # Пример RSI стратегии для Bybit
│   └── expert_okx_macd/     # Пример MACD стратегии для OKX
└── src/metaexpert/          # Основной исходный код
    ├── __init__.py          # Инициализация пакета
    ├── __main__.py          # Точка входа приложения
    ├── __version__.py       # Версия приложения
    ├── config.py            # Конфигурации проекта
    ├── py.typed             # Индикатор типизации
    ├── backtest/            # Модуль бэктестирования
    ├── cli/                 # Интерфейс командной строки
    ├── core/                # Ядро системы
    ├── exchanges/           # Поддержка бирж
    ├── logger/              # Система логирования
    ├── template/            # Шаблоны для генерации экспертов
    ├── utils/               # Утилиты
    └── websocket/           # Обработка WebSocket соединений
```

**Описание директорий:**

- `src/metaexpert/` - основной исходный код библиотеки MetaExpert, включает ядро, биржевые интеграции, утилиты и другие компоненты
- `examples/` - примеры торговых экспертов для различных бирж (Binance, Bybit, OKX)
- `docs/` - документация проекта, включая API, руководства и учебные материалы
- `tests/` - модуль для тестов (не виден в структуре, но упоминается в конфигурации)

Проект организован по принципу Feature-Sliced Design (FSD), где каждый функциональный аспект представлен в отдельной директории. Архитектура следует объектно-ориентированному подходу с четким разделением ответственности между модулями.

## 🛠 Технологический стек

| Технология | Версия/Назначение |
|------------|------------------|
| Язык программирования | Python 3.12+ |
| Основная библиотека | MetaExpert (собственная) |
| CLI фреймворк | Typer |
| Логирование | structlog |
| Валидация данных | Pydantic |
| WebSocket | websockets |
| Управление зависимостями | uv |
| Линтинг | Ruff |
| Типизация | Pyright |
| Тестирование | pytest |

**Основные зависимости:**

- `structlog` - структурированное логирование
- `pydantic` - валидация данных и типизация
- `typer` - создание CLI интерфейса
- `websockets` - обработка WebSocket соединений

**Инструменты разработки:**

- `python-dotenv` - загрузка переменных окружения
- `pyright` - статическая проверка типов
- `pytest` - фреймворк для тестирования
- `ruff` - линтер и форматтер

## 🏗 Архитектура

Проект следует объектно-ориентированному подходу с применением паттернов проектирования. Архитектура построена на принципах SOLID и DRY.

### Компонентная архитектура

Основной компонент - класс `MetaExpert`, который интегрирует различные аспекты торговой системы:

```python
class MetaExpert(Events):
    def __init__(
        self,
        exchange: str,
        api_key: str | None = None,
        api_secret: str | None = None,
        # ... другие параметры
    ) -> None:
        # Инициализация логирования
        self.logger: Logger = MetaLogger(...)
        
        # Инициализация биржи
        self.client: MetaExchange = MetaExchange.create(...)
```

### Паттерны разделения логики

Проект использует декораторы для разделения логики событий:

```python
@expert.on_init(
    symbol="BTCUSDT",
    timeframe="1h",
    # ... параметры стратегии
)
def init() -> None:
    """Инициализация стратегии"""

@expert.on_bar(timeframe="1h")
def bar(rates) -> None:
    """Обработка закрытия бара"""
```

### Управление состоянием приложения

Состояние приложения управляется через класс `Expert` с использованием dataclass:

```python
@dataclass
class Expert:
    # Основные параметры торговли
    symbol: str
    timeframe: Timeframe
    lookback_bars: int
    # ... другие поля
```

### Организация API-слоя и работа с данными

API-слой реализован через абстрактный класс `MetaExchange`:

```python
@dataclass
class MetaExchange(Trade, Market, ABC):
    @classmethod
    def create(
        cls,
        exchange: str,
        api_key: str | None,
        # ... другие параметры
    ) -> Self:
        # Фабричный метод для создания экземпляра биржи
        module = import_module(f"metaexpert.exchanges.{cls.exchange}")
        return module.Adapter()
```

### Паттерны роутинга и навигации

В проекте не используется роутинг в традиционном смысле, так как это библиотека для торговли, а не веб-приложение. Однако реализованы паттерны обработки событий через декораторы.

### Обработка ошибок и loading состояний

Проект включает комплексную систему обработки ошибок:

```python
def run(
    self,
    trade_mode: str = DEFAULT_TRADE_MODE,
    # ... другие параметры
) -> None:
    try:
        # Основная логика
        EventType.ON_INIT.run()
    except KeyboardInterrupt:
        self.logger.info("Expert stopped by user")
    except (ConnectionError, TimeoutError) as e:
        self.logger.error("Network error occurred: %s", e)
    except ValueError as e:
        self.logger.error("Data validation error: %s", e)
    except RuntimeError as e:
        self.logger.error("Runtime error: %s", e)
    finally:
        # Очистка ресурсов
        EventType.ON_DEINIT.run()
```

## 🎨 UI/UX и стилизация

Проект не включает визуальный интерфейс, так как это библиотека для создания торговых роботов. Взаимодействие с пользователем осуществляется через:

- CLI интерфейс
- Логирование в консоль и файлы
- Конфигурационные файлы

## ✅ Качество кода

### Конфигурации линтеров

Проект использует Ruff в качестве линтера и форматтера:

```toml
[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "C",      # flake8-comprehensions
    "B",      # flake8-bugbear
    "N",      # flake8-noqa
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "RUF",    # Ruff-specific rules
]
```

### Соглашения по именованию и организации кода

Код следует стандартам PEP 8 с использованием аннотаций типов Python. Используется систематическое именование переменных и функций на английском языке.

### Качество TypeScript типизации

Проект написан на Python с использованием аннотаций типов и Pydantic для валидации данных.

### Наличие и качество тестов

В конфигурации проекта указаны зависимости для тестирования (pytest, pytest-asyncio, pytest-cov), но в предоставленной структуре файлов тесты не видны.

### Документация в коде

Код включает подробные docstrings и комментарии:

```python
def on_init(
    self,
    symbol: str,
    timeframe: str,
    # ... параметры
) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """Decorator for initialization event handling.

    Args:
        symbol (str): Trading symbols (e.g., "BTCUSDT", "ETHUSDT").
        timeframe (str): Time frame for trading data (e.g., "1h", "1m").
        # ... другие параметры
    """
```

## 🔧 Ключевые компоненты

### 1. MetaExpert класс

**Назначение:** Основной класс торговой системы, координирующий все компоненты.

**Пример использования:**

```python
expert = MetaExpert(
    exchange="binance",
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    market_type="futures",
    contract_type="linear",
    # ... другие параметры
)

@expert.on_init(
    symbol="BTCUSDT",
    timeframe="1h",
    # ... параметры стратегии
)
def init() -> None:
    print("*** Strategy Initialized ***")
```

**Основные пропсы/API:** exchange, api_key, api_secret, market_type, contract_type, timeframe, symbol, и др.

### 2. Events класс

**Назначение:** Обработка событий торговой системы через декораторы.

**Пример использования:**

```python
class Events(Expert):
    def on_bar(timeframe: str = "1h") -> Callable[
        [Callable[[dict], None]], Callable[[dict], Coroutine[Any, Any, None]]]:
        def outer(func: Callable[[dict], None]) -> Callable[[dict], Coroutine[Any, Any, None]]:
            async def inner(rates: dict) -> None:
                bar = Bar(timeframe=timeframe, callback=func, args=(rates,))
                EventType.ON_BAR.push_instance(bar)
                await bar.start()
            return inner
        return outer
```

**Основные пропсы/API:** on_init, on_deinit, on_tick, on_bar, on_timer, on_order, on_position, и др.

### 3. MetaExchange абстрактный класс

**Назначение:** Абстрактный класс для интеграции с различными биржами.

**Пример использования:**

```python
@dataclass
class MetaExchange(Trade, Market, ABC):
    @classmethod
    def create(cls, exchange: str, ...) -> Self:
        module = import_module(f"metaexpert.exchanges.{cls.exchange}")
        return module.Adapter()
```

**Основные пропсы/API:** create, get_websocket_url, open_position, close_position, и др.

### 4. Конфигурационный модуль

**Назначение:** Централизованное хранение всех конфигурационных параметров.

**Пример использования:**

```python
DEFAULT_MARKET_TYPE: str = MARKET_TYPE_FUTURES
DEFAULT_CONTRACT_TYPE: str = CONTRACT_TYPE_LINEAR
DEFAULT_MARGIN_MODE: str = MARGIN_MODE_ISOLATED
DEFAULT_POSITION_MODE: str = POSITION_MODE_HEDGE
```

### 5. Биржевые адаптеры

**Назначение:** Реализация специфичной логики для каждой биржи.

**Пример использования (Binance):**

```python
class Adapter(MetaExchange):
    def _create_client(self) -> Self:
        match self.market_type:
            case MarketType.SPOT:
                return self._spot_client()
            case MarketType.FUTURES:
                return self._futures_client()
    
    def get_websocket_url(self, symbol: str, timeframe: str) -> str:
        base_url: str = ""
        match self.market_type:
            case MarketType.SPOT:
                base_url = SPOT_WS_BASE_URL
            case MarketType.FUTURES:
                base_url = FUTURES_WS_BASE_URL
        return f"{base_url}/ws/{symbol.lower()}@kline_{timeframe}"
```

## 📋 Выводы и рекомендации

**Сильные стороны проекта:**

1. Четкая архитектура с разделением ответственности
2. Поддержка нескольких бирж через абстрактные классы
3. Комплексная система конфигурации и настройки
4. Обширная система обработки событий через декораторы
5. Поддержка различных режимов торговли (paper, live, backtest)
6. Хорошо документированный код с аннотациями типов
7. Гибкие настройки рисков и управления позициями

**Потенциальные области для улучшения:**

1. Необходимо добавить полную реализацию методов в биржевых адаптерах (многие помечены как TODO)
2. Требуется создание тестовой базы для обеспечения качества (TDD как обязательное требование)
3. Нужно заполнить пустые разделы в README.md
4. Следует реализовать недостающие функции в примерах (например, EMA расчеты)

**Уровень сложности проекта:** Middle/Senior friendly - проект требует хорошего понимания как финансовых аспектов торговли, так и архитектурных паттернов в Python. Код написан с использованием современных практик и требует опыта для полноценной реализации всех функций.
