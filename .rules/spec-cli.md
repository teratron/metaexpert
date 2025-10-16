# Спецификация CLI для MetaExpert

**ID:** `SPEC-CLI`  
**Статус:** Утверждено  
**Версия:** 2.0  
**Дата:** 2025-10-16

---

## 1. Обзор

Этот документ определяет полную спецификацию для интерфейса командной строки (CLI) проекта MetaExpert. CLI построен на библиотеке `Typer` и служит основной точкой взаимодействия пользователя с библиотекой для создания, управления и запуска торговых экспертов.

### 1.1. Цели CLI

- Предоставить интуитивный интерфейс для работы с торговыми экспертами
- Обеспечить быстрый старт для новых пользователей
- Поддержать все основные сценарии использования библиотеки
- Следовать принципу "библиотека-первичной архитектуры"

---

## 2. Основные принципы проектирования

- **Интуитивность:** Команды и параметры должны быть самодокументируемыми с автоматической генерацией справки
- **Расширяемость:** Модульная архитектура для легкого добавления новых команд
- **Надежность:** Строгая валидация входных данных и информативная обработка ошибок
- **Соответствие стандартам:** Использование современных практик CLI в Python
- **Библиотека-первичность:** Каждая функция CLI доступна через программный API

---

## 3. Архитектура CLI

### 3.1. Точка входа

```
metaexpert [GLOBAL_OPTIONS] COMMAND [ARGS]...
```

### 3.2. Глобальные опции

- `--version`, `-v`: Показать версию библиотеки и выйти
- `--log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]`: Переопределить уровень логирования
- `--help`, `-h`: Показать справку

### 3.3. Файловая структура модуля

```
src/metaexpert/
├── __init__.py                 # Инициализация библиотеки
├── __main__.py                 # Точка входа: python -m metaexpert
├── __version__.py              # Версия библиотеки
└── cli/
    ├── __init__.py
    ├── main.py                 # Основное приложение Typer
    ├── commands/
    │   ├── __init__.py
    │   ├── run.py              # Команда run
    │   ├── new.py              # Команда new
    │   ├── backtest.py         # Команда backtest
    │   ├── list.py             # Команда list
    │   ├── status.py           # Команда status
    │   ├── stop.py             # Команда stop
    │   ├── logs.py             # Команда logs
    │   ├── portfolio.py        # Команда portfolio
    │   ├── market.py           # Команда market
    │   ├── optimize.py         # Команда optimize
    │   ├── compare.py          # Команда compare
    │   ├── export.py           # Команда export
    │   ├── import.py           # Команда import
    │   ├── schedule.py         # Команда schedule
    │   ├── risk.py             # Команда risk
    │   ├── sync.py             # Команда sync
    │   ├── replay.py           # Команда replay
    │   ├── config/
    │   │   ├── __init__.py
    │   │   ├── base.py         # Базовая команда config
    │   │   ├── show.py         # Подкоманда show
    │   │   ├── set.py          # Подкоманда set
    │   │   ├── get.py          # Подкоманда get
    │   │   └── reset.py        # Подкоманда reset
    │   ├── notify/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── setup.py
    │   │   ├── add.py
    │   │   ├── remove.py
    │   │   ├── test.py
    │   │   └── list.py
    │   └── model/
    │       ├── __init__.py
    │       ├── base.py
    │       ├── train.py
    │       ├── predict.py
    │       ├── evaluate.py
    │       ├── list.py
    │       └── delete.py
    ├── utils/
    │   ├── __init__.py
    │   ├── validators.py       # Валидаторы параметров
    │   ├── formatters.py       # Форматтеры вывода
    │   └── helpers.py          # Вспомогательные функции
    └── templates/
        ├── __init__.py
        ├── template.py         # Шаблон эксперта
        └── generator.py        # Генератор шаблонов
```

---

## 4. Основные команды

### 4.1. `metaexpert new`

**Назначение:** Создание нового проекта торгового эксперта из шаблона `src/metaexpert/cli/templates/template.py`.

**Синтаксис:**

```bash
metaexpert new [OPTIONS] PROJECT_NAME
metaexpert --new [OPTIONS] PROJECT_NAME  # Альтернативная форма
```

**Аргументы:**

- `PROJECT_NAME` (обязательный, `str`) - Имя нового проекта (используется как имя директории)

**Опции:**

- `--force`, `-f` (флаг) - Перезаписать существующую директорию
- `--exchange`, `-e` (`str`, по умолчанию: "binance") - Целевая биржа
- `--strategy`, `-s` (`str`, по умолчанию: "template") - Тип стратегии (ema, rsi, macd)
- `--output-dir`, `-o` (`str`, по умолчанию: текущая директория) - Директория для создания проекта
- `--market-type` (`str`, по умолчанию: "futures") - Тип рынка (spot, futures, options)

**Поведение:**

1. **Валидация:**
   - Проверяет, что `PROJECT_NAME` соответствует требованиям именования Python модулей
   - Проверяет существование директории `PROJECT_NAME`
   - Если директория существует и флаг `--force` не указан, завершается с ошибкой:

     ```
     [ERROR] Директория "my-first-bot" уже существует. Используйте --force для перезаписи.
     ```

2. **Создание структуры проекта:**

   ```
   <PROJECT_NAME>/
   ├── main.py              # Копия src/metaexpert/template/template.py
   ├── .env.example         # Шаблон переменных окружения
   ├── .gitignore           # Стандартный .gitignore для Python проектов
   ├── README.md            # Описание проекта
   └── pyproject.toml       # Конфигурация проекта с зависимостью от metaexpert
   ```

3. **Генерация файлов:**

   **`main.py`:**
   - Копируется из `src/metaexpert/template/template.py`
   - Параметры `exchange` и `market_type` подставляются на основе опций CLI
   - Если указан `--strategy`, в комментариях добавляются подсказки по реализации выбранной стратегии

   **`.env.example`:**

   ```env
   # API Keys для биржи {exchange}
   API_KEY=your_api_key_here
   API_SECRET=your_api_secret_here
   API_PASSPHRASE=your_passphrase_here  # Если требуется для биржи
   
   # Настройки подключения
   TESTNET=true
   
   # Логирование
   LOG_LEVEL=INFO
   ```

   **`pyproject.toml`:**

   ```toml
   [project]
   name = "{project_name}"
   version = "0.1.0"
   description = "Trading expert built with MetaExpert"
   requires-python = ">=3.12"
   dependencies = [
       "metaexpert>=0.1.0",
   ]

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [tool.uv]
   dev-dependencies = [
       "pytest>=7.0.0",
       "pytest-cov>=4.0.0",
   ]
   ```

   **`README.md`:**

   ```markdown
   # {PROJECT_NAME}

   Trading expert built with MetaExpert framework.

   ## Конфигурация

   1. Скопируйте `.env.example` в `.env`:
      ```bash
      cp .env.example .env
      ```

   2. Заполните ваши API ключи в `.env`

   ## Установка зависимостей

   ```bash
   uv sync
   ```

   ## Запуск

   ### Paper trading (демо-режим)

   ```bash
   metaexpert run
   ```

   ### Live trading (реальная торговля)

   ```bash
   metaexpert run --trade-mode live
   ```

   ### Backtest

   ```bash
   metaexpert backtest main.py --start-date 2024-01-01
   ```

   **`.gitignore`:**

   ```gitignore
   # Переменные окружения
   .env
   .env.local
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   env/
   venv/
   .venv/
   
   # Логи
   *.log
   logs/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   
   # Результаты тестов
   .pytest_cache/
   .coverage
   htmlcov/
   
   # Данные
   data/
   *.csv
   *.db
   ```

4. **Вывод информации:**
   - Выводит сообщение об успехе
   - Показывает структуру созданного проекта
   - Предоставляет четкие инструкции для следующих шагов

**Примеры:**

```bash
# Создание базового проекта
metaexpert new my-first-bot

# Создание проекта для конкретной биржи и стратегии
metaexpert new rsi_bybit --exchange bybit --strategy rsi

# Создание проекта в конкретной директории
metaexpert --new macd_okx --exchange okx --output-dir ./experts

# Перезапись существующего проекта
metaexpert new my-bot --force

# Создание проекта для спотового рынка
metaexpert new spot_trader --market-type spot --exchange binance
```

**Вывод при успехе:**

```
[SUCCESS] Проект "my-first-bot" успешно создан в ./my-first-bot/

Структура проекта:
my-first-bot/
├── main.py              # Основной файл эксперта
├── .env.example         # Шаблон переменных окружения
├── .gitignore           # Git ignore файл
├── README.md            # Документация проекта
└── pyproject.toml       # Конфигурация зависимостей

Следующие шаги:
1. cd my-first-bot
2. Скопируйте .env.example в .env и заполните ваши API-ключи:
   cp .env.example .env
3. Установите зависимости:
   uv sync
4. Запустите эксперта в режиме paper trading:
   metaexpert run

Дополнительные команды:
- Бэктест: metaexpert backtest main.py --start-date 2024-01-01
- Live режим: metaexpert run --trade-mode live
- Справка: metaexpert --help

Документация: https://github.com/teratron/metaexpert
```

**Обработка ошибок:**

1. **Директория уже существует:**

   ```
   [ERROR] Директория "my-first-bot" уже существует. 
   Используйте --force для перезаписи или выберите другое имя.
   ```

2. **Некорректное имя проекта:**

   ```
   [ERROR] Имя проекта "123-invalid" некорректно.
   Имя должно начинаться с буквы и содержать только буквы, цифры, дефисы и подчеркивания.
   ```

3. **Шаблон не найден:**

   ```
   [ERROR] Шаблон template.py не найден по пути: src/metaexpert/template/template.py
   Пожалуйста, переустановите библиотеку MetaExpert.
   ```

4. **Недостаточно прав для создания директории:**

   ```
   [ERROR] Недостаточно прав для создания директории: /protected/path/
   Проверьте права доступа или выберите другую директорию с --output-dir.
   ```

**Технические детали реализации:**

- Команда использует `shutil.copytree()` для копирования шаблона
- Подстановка параметров выполняется через Jinja2 templates или простое string replacement
- Валидация имени проекта через regex: `^[a-zA-Z][a-zA-Z0-9_-]*# Спецификация CLI для MetaExpert

**ID:** `SPEC-CLI`  
**Статус:** Утверждено  
**Версия:** 2.0  
**Дата:** 2025-10-16

---

## 1. Обзор

Этот документ определяет полную спецификацию для интерфейса командной строки (CLI) проекта MetaExpert. CLI построен на библиотеке Typer и служит основной точкой взаимодействия пользователя с библиотекой для создания, управления и запуска торговых экспертов.

### 1.1. Цели CLI

- Предоставить интуитивный интерфейс для работы с торговыми экспертами
- Обеспечить быстрый старт для новых пользователей
- Поддержать все основные сценарии использования библиотеки
- Следовать принципу "библиотека-первичной архитектуры"

---

## 2. Основные принципы проектирования

- **Интуитивность:** Команды и параметры должны быть самодокументируемыми с автоматической генерацией справки
- **Расширяемость:** Модульная архитектура для легкого добавления новых команд
- **Надежность:** Строгая валидация входных данных и информативная обработка ошибок
- **Соответствие стандартам:** Использование современных практик CLI в Python
- **Библиотека-первичность:** Каждая функция CLI доступна через программный API

---

## 3. Архитектура CLI

### 3.1. Точка входа

```
metaexpert [GLOBAL_OPTIONS] COMMAND [ARGS]...
```

### 3.2. Глобальные опции

- `--version`, `-v`: Показать версию библиотеки и выйти
- `--log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]`: Переопределить уровень логирования
- `--help`, `-h`: Показать справку

### 3.3. Файловая структура модуля

```
src/metaexpert/
├── __main__.py                 # Точка входа: python -m metaexpert
├── __version__.py              # Версия библиотеки
└── cli/
    ├── __init__.py
    ├── main.py                 # Основное приложение Typer
    ├── commands/
    │   ├── __init__.py
    │   ├── run.py              # Команда run
    │   ├── new.py              # Команда new
    │   ├── backtest.py         # Команда backtest
    │   ├── list.py             # Команда list
    │   ├── status.py           # Команда status
    │   ├── stop.py             # Команда stop
    │   ├── logs.py             # Команда logs
    │   ├── portfolio.py        # Команда portfolio
    │   ├── market.py           # Команда market
    │   ├── optimize.py         # Команда optimize
    │   ├── compare.py          # Команда compare
    │   ├── export.py           # Команда export
    │   ├── import.py           # Команда import
    │   ├── schedule.py         # Команда schedule
    │   ├── risk.py             # Команда risk
    │   ├── sync.py             # Команда sync
    │   ├── replay.py           # Команда replay
    │   ├── config/
    │   │   ├── __init__.py
    │   │   ├── base.py         # Базовая команда config
    │   │   ├── show.py         # Подкоманда show
    │   │   ├── set.py          # Подкоманда set
    │   │   ├── get.py          # Подкоманда get
    │   │   └── reset.py        # Подкоманда reset
    │   ├── notify/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── setup.py
    │   │   ├── add.py
    │   │   ├── remove.py
    │   │   ├── test.py
    │   │   └── list.py
    │   └── model/
    │       ├── __init__.py
    │       ├── base.py
    │       ├── train.py
    │       ├── predict.py
    │       ├── evaluate.py
    │       ├── list.py
    │       └── delete.py
    ├── utils/
    │   ├── __init__.py
    │   ├── validators.py       # Валидаторы параметров
    │   ├── formatters.py       # Форматтеры вывода
    │   └── helpers.py          # Вспомогательные функции
    └── templates/
        ├── __init__.py
        └── generator.py        # Генератор шаблонов
```

---

## 4. Основные команды

- Все файлы создаются с правильными правами доступа (0o644 для файлов, 0o755 для директорий)

---

### 4.2. `metaexpert run`

**Назначение:** Запуск торгового эксперта.

**Синтаксис:**

```bash
metaexpert run [OPTIONS] [EXPERT_PATH]
```

**Аргументы:**

- `EXPERT_PATH` (необязательный, `pathlib.Path`, по умолчанию: `main.py`) - Путь к файлу эксперта

**Опции:**

- `--trade-mode`, `-t` (`TradeMode`, по умолчанию: "paper") - Режим торговли (paper, live, backtest)
- `--symbol` (`str`) - Торговый символ (например, BTCUSDT)
- `--timeframe` (`str`) - Таймфрейм (1m, 5m, 1h, 4h, 1d)
- `--exchange` (`str`) - Биржа для торговли
- `--api-key` (`str`) - API ключ (если не указан, берется из .env)
- `--api-secret` (`str`) - API секрет (если не указан, берется из .env)
- `--testnet` (флаг, по умолчанию: true) - Использовать тестовую сеть
- `--config` (`pathlib.Path`) - Путь к файлу конфигурации .env
- `--log-level` (`LogLevel`, по умолчанию: "INFO") - Уровень логирования
- `--initial-capital` (`float`, по умолчанию: 10000.0) - Начальный капитал

**Поведение:**

1. Динамически импортирует файл эксперта
2. Находит экземпляр класса `MetaExpert`
3. Переопределяет параметры значениями из CLI (приоритет CLI > код)
4. Вызывает метод `.run()`

**Примеры:**

```bash
metaexpert run
metaexpert run examples/expert_binance_ema/main.py
metaexpert run my_expert.py --trade-mode live --exchange binance
metaexpert run my_expert.py --trade-mode backtest --initial-capital 50000
```

---

### 4.3. `metaexpert backtest`

**Назначение:** Запуск бэктестинга стратегии на исторических данных.

**Синтаксис:**

```bash
metaexpert backtest [OPTIONS] EXPERT_PATH
```

**Аргументы:**

- `EXPERT_PATH` (обязательный, `pathlib.Path`) - Путь к файлу эксперта

**Опции:**

- `--start-date`, `-s` (`str`, формат: YYYY-MM-DD, по умолчанию: год назад) - Начальная дата
- `--end-date`, `-e` (`str`, формат: YYYY-MM-DD, по умолчанию: сегодня) - Конечная дата
- `--initial-capital`, `-c` (`float`, по умолчанию: 10000.0) - Начальный капитал
- `--symbol` (`str`) - Торговая пара (переопределяет значение из эксперта)
- `--timeframe` (`str`) - Таймфрейм (переопределяет значение из эксперта)
- `--report-format` (`str`, по умолчанию: "text") - Формат отчета (text, json, html)
- `--save-results` (`pathlib.Path`) - Сохранить результаты в файл

**Примеры:**

```bash
metaexpert backtest examples/expert_binance_ema/main.py
metaexpert backtest my_expert.py --start-date 2024-01-01 --end-date 2024-12-31
metaexpert backtest my_expert.py --report-format json --save-results results.json
```

---

### 4.4. `metaexpert list`

**Назначение:** Отображение списка доступных экспертов.

**Синтаксис:**

```bash
metaexpert list [OPTIONS]
```

**Опции:**

- `--path`, `-p` (`str`, по умолчанию: ./examples) - Директория для поиска
- `--format`, `-f` (`str`, по умолчанию: "table") - Формат вывода (table, json, list)
- `--recursive`, `-r` (флаг) - Рекурсивный поиск

**Примеры:**

```bash
metaexpert list
metaexpert list --path ./my_experts --format json
metaexpert list --recursive
```

---

### 4.5. `metaexpert config`

**Назначение:** Управление конфигурацией.

**Синтаксис:**

```bash
metaexpert config [SUBCOMMAND]
```

#### Подкоманды

**`show`** - Показать текущую конфигурацию

```bash
metaexpert config show [--format table|json|yaml]
```

**`set`** - Установить параметр

```bash
metaexpert config set <key> <value>
```

**`get`** - Получить значение параметра

```bash
metaexpert config get <key>
```

**`reset`** - Сбросить конфигурацию

```bash
metaexpert config reset [--confirm]
```

**Примеры:**

```bash
metaexpert config show
metaexpert config set default_exchange binance
metaexpert config get log_level
metaexpert config reset --confirm
```

---

### 4.6. `metaexpert status`

**Назначение:** Отображение статуса запущенных экспертов.

**Синтаксис:**

```bash
metaexpert status [OPTIONS]
```

**Опции:**

- `--format`, `-f` (`str`, по умолчанию: "table") - Формат вывода (table, json, yaml)
- `--watch`, `-w` (флаг) - Непрерывное обновление информации
- `--expert`, `-e` (`str`) - Конкретный эксперт

**Примеры:**

```bash
metaexpert status
metaexpert status --format json --watch
metaexpert status --expert my_ema_strategy
```

---

### 4.7. `metaexpert stop`

**Назначение:** Остановка запущенного эксперта.

**Синтаксис:**

```bash
metaexpert stop [OPTIONS] EXPERT_NAME_OR_ID
```

**Аргументы:**

- `EXPERT_NAME_OR_ID` (обязательный, `str`) - Имя или ID эксперта

**Опции:**

- `--force`, `-f` (флаг) - Принудительная остановка
- `--timeout`, `-t` (`int`, по умолчанию: 30) - Таймаут в секундах

**Примеры:**

```bash
metaexpert stop my_ema_strategy
metaexpert stop 12345 --force
metaexpert stop my_rsi_expert --timeout 60
```

---

### 4.8. `metaexpert logs`

**Назначение:** Просмотр логов экспертов.

**Синтаксис:**

```bash
metaexpert logs [OPTIONS]
```

**Опции:**

- `--expert`, `-e` (`str`) - Имя эксперта
- `--level`, `-l` (`str`, по умолчанию: "INFO") - Уровень логов (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--limit`, `-n` (`int`, по умолчанию: 50) - Количество строк
- `--follow`, `-f` (флаг) - Следовать за новыми записями (tail -f)
- `--format` (`str`, по умолчанию: "text") - Формат вывода (text, json)

**Примеры:**

```bash
metaexpert logs
metaexpert logs --expert my_ema_strategy --level DEBUG
metaexpert logs --follow --limit 100
```

---

### 4.9. `metaexpert portfolio`

**Назначение:** Информация о портфеле.

**Синтаксис:**

```bash
metaexpert portfolio [OPTIONS]
```

**Опции:**

- `--exchange`, `-x` (`str`) - Конкретная биржа
- `--format`, `-f` (`str`, по умолчанию: "table") - Формат вывода (table, json, chart)
- `--show-history`, `-H` (флаг) - Показать историю изменений

**Примеры:**

```bash
metaexpert portfolio
metaexpert portfolio --exchange binance --format chart
metaexpert portfolio --show-history
```

---

### 4.10. `metaexpert market`

**Назначение:** Рыночные данные для торговой пары.

**Синтаксис:**

```bash
metaexpert market [OPTIONS] SYMBOL
```

**Аргументы:**

- `SYMBOL` (обязательный, `str`) - Торговая пара (например, BTCUSDT)

**Опции:**

- `--exchange`, `-x` (`str`) - Биржа
- `--timeframe`, `-t` (`str`, по умолчанию: "1h") - Таймфрейм
- `--indicators`, `-i` (`str`) - Список индикаторов (например, "sma,rsi,macd")
- `--output`, `-o` (`str`, по умолчанию: "table") - Формат вывода

**Примеры:**

```bash
metaexpert market BTCUSDT
metaexpert market ETHUSDT --exchange bybit --timeframe 15m
metaexpert market BTCUSDT --indicators "sma,rsi,macd" --output chart
```

---

### 4.11. `metaexpert optimize`

**Назначение:** Оптимизация параметров стратегии.

**Синтаксис:**

```bash
metaexpert optimize [OPTIONS] EXPERT_PATH
```

**Аргументы:**

- `EXPERT_PATH` (обязательный, `pathlib.Path`) - Путь к файлу эксперта

**Опции:**

- `--parameter-ranges`, `-p` (`str`) - Диапазоны параметров (формат: "ma_period:10,50;rsi_period:7,21")
- `--optimization-method`, `-m` (`str`, по умолчанию: "grid") - Метод (grid, genetic, bayesian)
- `--fitness-function`, `-f` (`str`, по умолчанию: "sharpe") - Функция оптимизации (sharpe, profit, max_drawdown)
- `--population-size`, `-s` (`int`, по умолчанию: 50) - Размер популяции (для genetic)
- `--generations`, `-g` (`int`, по умолчанию: 100) - Количество поколений
- `--output-file`, `-o` (`pathlib.Path`) - Файл для сохранения результатов

**Примеры:**

```bash
metaexpert optimize my_expert.py --parameter-ranges "ma_period:10,50;rsi_period:7,21"
metaexpert optimize my_expert.py --optimization-method genetic --fitness-function profit
metaexpert optimize my_expert.py --output-file optimization_results.json
```

---

### 4.12. `metaexpert compare`

**Назначение:** Сравнение производительности стратегий.

**Синтаксис:**

```bash
metaexpert compare [OPTIONS] EXPERT_FILES...
```

**Аргументы:**

- `EXPERT_FILES` (обязательный, `list[pathlib.Path]`) - Список файлов экспертов

**Опции:**

- `--start-date`, `-s` (`str`, формат: YYYY-MM-DD) - Начальная дата
- `--end-date`, `-e` (`str`, формат: YYYY-MM-DD) - Конечная дата
- `--initial-capital`, `-c` (`float`, по умолчанию: 10000.0) - Начальный капитал
- `--benchmark`, `-b` (`str`, по умолчанию: "BTCUSDT") - Бенчмарк
- `--format`, `-f` (`str`, по умолчанию: "table") - Формат вывода (table, json, html, chart)
- `--metrics`, `-m` (`str`) - Список метрик (например, "sharpe,profit,drawdown")

**Примеры:**

```bash
metaexpert compare expert1.py expert2.py expert3.py
metaexpert compare *.py --start-date 2024-01-01 --end-date 2024-12-31
metaexpert compare expert1.py expert2.py --format chart --metrics "sharpe,profit"
```

---

### 4.13. `metaexpert export`

**Назначение:** Экспорт данных в различные форматы.

**Синтаксис:**

```bash
metaexpert export [OPTIONS] DATA_TYPE
```

**Аргументы:**

- `DATA_TYPE` (обязательный, `str`) - Тип данных (trades, positions, portfolio, config, backtest_results, reports)

**Опции:**

- `--output`, `-o` (`pathlib.Path`) - Путь для сохранения
- `--format`, `-f` (`str`, по умолчанию: "json") - Формат (json, csv, excel, xml)
- `--start-date`, `-s` (`str`, формат: YYYY-MM-DD) - Начальная дата
- `--end-date`, `-e` (`str`, формат: YYYY-MM-DD) - Конечная дата
- `--expert` (`str`) - Конкретный эксперт

**Примеры:**

```bash
metaexpert export trades --output my_trades.csv --format csv
metaexpert export backtest_results --expert my_ema_strategy --format json
metaexpert export portfolio --start-date 2024-01-01 --end-date 2024-12-31
```

---

### 4.14. `metaexpert import`

**Назначение:** Импорт данных из внешних источников.

**Синтаксис:**

```bash
metaexpert import [OPTIONS] DATA_TYPE FILE_PATH
```

**Аргументы:**

- `DATA_TYPE` (обязательный, `str`) - Тип данных (trades, positions, config, strategies, historical_data)
- `FILE_PATH` (обязательный, `pathlib.Path`) - Путь к файлу

**Опции:**

- `--format`, `-f` (`str`) - Формат данных (json, csv, excel)
- `--validate`, `-v` (флаг, по умолчанию: true) - Валидировать данные
- `--overwrite`, `-o` (флаг) - Перезаписать существующие данные

**Примеры:**

```bash
metaexpert import strategies my_strategy.json
metaexpert import trades trades.csv --format csv --validate
metaexpert import config settings.json --overwrite
```

---

### 4.15. `metaexpert notify`

**Назначение:** Управление уведомлениями.

**Синтаксис:**

```bash
metaexpert notify [SUBCOMMAND]
```

#### Подкоманды

**`setup`** - Настройка системы уведомлений

```bash
metaexpert notify setup --provider email|telegram|discord|slack [--config-file FILE]
```

**`add`** - Добавление метода уведомлений

```bash
metaexpert notify add <notification_type> [--settings JSON]
```

**`remove`** - Удаление метода

```bash
metaexpert notify remove <id>
```

**`test`** - Тестирование метода

```bash
metaexpert notify test <id>
```

**`list`** - Список настроенных уведомлений

```bash
metaexpert notify list [--format table|json]
```

---

### 4.16. `metaexpert schedule`

**Назначение:** Планирование запуска экспертов.

**Синтаксис:**

```bash
metaexpert schedule [OPTIONS] EXPERT_PATH
```

**Аргументы:**

- `EXPERT_PATH` (обязательный, `pathlib.Path`) - Путь к файлу эксперта

**Опции:**

- `--cron`, `-c` (`str`) - Выражение cron
- `--start-date`, `-s` (`str`, формат: YYYY-MM-DD) - Дата начала
- `--end-date`, `-e` (`str`, формат: YYYY-MM-DD) - Дата окончания
- `--interval`, `-i` (`str`) - Интервал (daily, weekly, monthly)
- `--parameters`, `-p` (`str`) - Параметры для передачи эксперту

**Примеры:**

```bash
metaexpert schedule my_expert.py --cron "0 9 * * 1-5"
metaexpert schedule my_expert.py --interval daily --parameters "--trade-mode paper"
metaexpert schedule my_expert.py --start-date 2024-01-01 --end-date 2024-12-31
```

---

### 4.17. `metaexpert risk`

**Назначение:** Анализ и управление рисками.

**Синтаксис:**

```bash
metaexpert risk [OPTIONS] EXPERT_PATH
```

**Аргументы:**

- `EXPERT_PATH` (обязательный, `pathlib.Path`) - Путь к файлу эксперта

**Опции:**

- `--calculate`, `-c` (`str`) - Риск-параметр (VaR, CVaR, max_drawdown, sharpe_ratio, sortino_ratio)
- `--timeframe`, `-t` (`str`, по умолчанию: "30d") - Временной горизонт (7d, 14d, 30d, 90d, 1y)
- `--confidence`, `-f` (`float`, по умолчанию: 0.95) - Уровень доверия для VaR
- `--report`, `-r` (флаг) - Полный отчет о рисках

**Примеры:**

```bash
metaexpert risk my_expert.py --calculate VaR --confidence 0.99
metaexpert risk my_expert.py --timeframe 90d --report
metaexpert risk my_expert.py --calculate "max_drawdown,sharpe_ratio"
```

---

### 4.18. `metaexpert sync`

**Назначение:** Синхронизация данных между источниками.

**Синтаксис:**

```bash
metaexpert sync [OPTIONS]
```

**Опции:**

- `--source`, `-s` (`str`) - Источник данных
- `--destination`, `-d` (`str`) - Место назначения
- `--data-type`, `-t` (`str`) - Тип данных (orders, positions, trades, balance)
- `--exchange`, `-x` (`str`) - Биржа

**Примеры:**

```bash
metaexpert sync --source binance --destination local --data-type positions
metaexpert sync --source local --destination bybit --data-type orders
metaexpert sync --exchange okx --data-type balance
```

---

### 4.19. `metaexpert replay`

**Назначение:** Воспроизведение исторических данных.

**Синтаксис:**

```bash
metaexpert replay [OPTIONS] EXPERT_PATH SYMBOL
```

**Аргументы:**

- `EXPERT_PATH` (обязательный, `pathlib.Path`) - Путь к файлу эксперта
- `SYMBOL` (обязательный, `str`) - Торговая пара

**Опции:**

- `--start-date`, `-s` (`str`, формат: YYYY-MM-DD) - Начальная дата
- `--end-date`, `-e` (`str`, формат: YYYY-MM-DD) - Конечная дата
- `--speed`, `-p` (`float`, по умолчанию: 1.0) - Скорость воспроизведения
- `--timeframe`, `-t` (`str`, по умолчанию: "1m") - Таймфрейм
- `--exchange`, `-x` (`str`) - Биржа

**Примеры:**

```bash
metaexpert replay my_expert.py BTCUSDT --start-date 2024-01-01 --end-date 2024-01-31
metaexpert replay my_expert.py ETHUSDT --speed 2.0 --timeframe 5m
metaexpert replay my_expert.py BTCUSDT --exchange binance --speed 0.5
```

---

### 4.20. `metaexpert model`

**Назначение:** Управление ML моделями.

**Синтаксис:**

```bash
metaexpert model [SUBCOMMAND]
```

#### Подкоманды

**`train`** - Обучение модели

```bash
metaexpert model train EXPERT_PATH [--data-source SOURCE] [--model-type TYPE] [--output FILE]
```

**`predict`** - Прогнозирование

```bash
metaexpert model predict MODEL_FILE [--input-data DATA] [--output FILE]
```

**`evaluate`** - Оценка модели

```bash
metaexpert model evaluate MODEL_FILE [--test-data DATA] [--metrics METRICS]
```

**`list`** - Список моделей

```bash
metaexpert model list [--format table|json]
```

**`delete`** - Удаление модели

```bash
metaexpert model delete <model_id>
```

---

## 5. Типы данных и валидация

### 5.1. Типы параметров

| Тип | Описание | Примеры |
|-----|----------|---------|
| `str` | Строковые значения | имена файлов, параметры |
| `int` | Целочисленные значения | ID, количество |
| `float` | Числа с плавающей точкой | капитал, проценты |
| `bool` | Логические значения | флаги |
| `pathlib.Path` | Пути к файлам | пути к экспертам |
| `datetime` | Даты | формат YYYY-MM-DD |
| `Enum` | Перечисления | TradeMode, LogLevel |

### 5.2. Кастомные валидаторы

```python
# src/metaexpert/cli/utils/validators.py

import typer
import pathlib
from datetime import datetime

def validate_date_format(date_string: str) -> str:
    """Проверяет, что строка соответствует формату YYYY-MM-DD."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter(f"Дата '{date_string}' должна быть в формате YYYY-MM-DD.")
    return date_string

def validate_positive_number(value: float) -> float:
    """Проверяет, что число является положительным."""
    if value <= 0:
        raise typer.BadParameter(f"Значение должно быть положительным, а не {value}.")
    return value

def validate_file_exists(path: pathlib.Path) -> pathlib.Path:
    """Проверяет, что файл по указанному пути существует."""
    if not path.is_file():
        raise typer.BadParameter(f"Файл не найден по пути: {path}")
    return path

def validate_project_name(name: str) -> str:
    """Проверяет корректность имени проекта."""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        raise typer.BadParameter(
            "Имя проекта должно начинаться с буквы и содержать только буквы, цифры, дефисы и подчеркивания."
        )
    return name
```

---

## 6. Обработка ошибок и коды выхода

### 6.1. Стандартные ошибки CLI

| Код | Описание | Пример |
|-----|----------|--------|
| `0` | Успешное выполнение | `metaexpert run` успешно завершен |
| `1` | Общая ошибка выполнения | Ошибка при подключении к бирже, ошибка в логике эксперта |
| `2` | Ошибка в параметрах команды | `metaexpert run --trade-mode=invalid_mode` |
| `10`| Прервано пользователем | Нажатие `Ctrl+C` |

### 6.2. Форматы сообщений об ошибках

Сообщения об ошибках должны быть информативными и предоставлять пользователю контекст для решения проблемы.

- **[ERROR]** - для критических ошибок, которые останавливают выполнение.
- **[WARNING]** - для некритических проблем.
- **[INFO]** - для информационных сообщений.

**Примеры:**

```
[ERROR] Ошибка аутентификации на бирже Binance: неверный API ключ.
Проверьте ваши ключи в файле .env или передайте их через опции --api-key и --api-secret.
```

```
[ERROR] Неверный параметр --trade-mode 'invalid'. Доступные значения: paper, live, backtest.
```

---

## 7. Вывод и форматирование

### 7.1. Стандартные форматы вывода

CLI должен поддерживать несколько форматов вывода для интеграции с другими инструментами.

- `table`: Человеко-читаемый формат (по умолчанию для большинства команд). Используется библиотека `rich`.
- `json`: Формат JSON для программной обработки.
- `yaml`: Формат YAML.
- `list`: Простой список, по одному элементу на строку.
- `chart`: ASCII-графики для визуализации данных (например, для `portfolio` или `market`).

### 7.2. Индикаторы прогресса

Для длительных операций (бэктестинг, оптимизация) должен использоваться индикатор прогресса.

```
Бэктестинг стратегии...
[████████████████████████████████████████] 100% | Готово
```

---

## 8. Тестирование

- Все команды CLI должны быть покрыты unit-тестами с использованием `pytest` и `Typer.testing.CliRunner`.
- Тесты должны проверять как успешное выполнение, так и обработку ошибок.
- Покрытие кода тестами для модуля `cli` должно быть не менее 90%.

---

## 9. Документация и справка

- Каждая команда и опция должны иметь `help`-текст.
- Справка генерируется автоматически библиотекой `Typer`.
- Основная документация по использованию CLI находится в `docs/guides/cli_usage.md`.

---
