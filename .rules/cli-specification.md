# CLI Specification for MetaExpert

## 1. Обзор

MetaExpert предоставляет командный интерфейс (CLI) для управления и запуска торговых экспертов. CLI реализован с использованием библиотеки Typer и соответствует принципу "библиотека-первичная архитектура", где каждый компонент доступен как через CLI, так и программно.

## 2. Структура CLI

### Основные команды:
- `metaexpert run` - запуск торгового эксперта
- `metaexpert new` - создание нового эксперта на основе шаблона
- `metaexpert backtest` - запуск бэктеста
- `metaexpert list` - список доступных экспертов
- `metaexpert config` - управление конфигурацией

### Структура команд:
```
metaexpert
├── run <expert_file> [OPTIONS]          # Запуск эксперта
├── new <expert_name> [OPTIONS]          # Создание нового эксперта
├── backtest <expert_file> [OPTIONS]     # Запуск бэктеста
├── list                                 # Список экспертов
├── config [SUBCOMMANDS]                 # Управление конфигурацией
│   ├── show                            # Показать текущую конфигурацию
│   ├── set <key> <value>               # Установить параметр
│   └── reset                           # Сбросить конфигурацию
└── --version, --help                   # Системная информация
```

## 3. Подробное описание команд

### 3.1. `metaexpert run`

Команда для запуска торгового эксперта.

**Синтаксис:**
```
metaexpert run <expert_file> [OPTIONS]
```

**Параметры:**
- `expert_file` (обязательный) - путь к файлу эксперта
- `--trade-mode`, `-t` (по умолчанию: "paper") - режим торговли ("paper", "live", "backtest")
- `--exchange` - биржа для торговли (например, "binance", "bybit", "okx")
- `--api-key` - API ключ (если не указан, будет использован из .env)
- `--api-secret` - API секрет (если не указан, будет использован из .env)
- `--testnet` - использовать тестовую сеть (по умолчанию: true)
- `--log-level` - уровень логирования (по умолчанию: "INFO")
- `--initial-capital` - начальный капитал для paper/backtest режимов

**Примеры:**
```
metaexpert run examples/expert_binance_ema/main.py
metaexpert run my_expert.py --trade-mode live --exchange binance
metaexpert run my_expert.py --trade-mode backtest --initial-capital 10000
```

### 3.2. `metaexpert new`

Команда для создания нового эксперта на основе шаблона.

**Синтаксис:**
```
metaexpert new <expert_name> [OPTIONS]
```

**Параметры:**
- `expert_name` (обязательный) - имя нового эксперта
- `--exchange`, `-e` (по умолчанию: "binance") - целевая биржа
- `--strategy`, `-s` (по умолчанию: "template") - тип стратегии (например, "ema", "rsi", "macd")
- `--output-dir`, `-o` (по умолчанию: текущая директория) - директория для создания эксперта
- `--market-type` (по умолчанию: "futures") - тип рынка ("spot", "futures", "options")

**Примеры:**
```
metaexpert new my_ema_strategy
metaexpert new rsi_bybit --exchange bybit --strategy rsi
metaexpert new macd_okx --exchange okx --output-dir ./my_experts
```

### 3.3. `metaexpert backtest`

Команда для запуска бэктеста эксперта.

**Синтаксис:**
```
metaexpert backtest <expert_file> [OPTIONS]
```

**Параметры:**
- `expert_file` (обязательный) - путь к файлу эксперта
- `--start-date`, `-s` - начальная дата бэктеста (формат: YYYY-MM-DD)
- `--end-date`, `-e` - конечная дата бэктеста (формат: YYYY-MM-DD)
- `--initial-capital`, `-c` (по умолчанию: 1000) - начальный капитал
- `--symbol` - торговая пара (если отличается от заданной в эксперте)
- `--timeframe` - таймфрейм (если отличается от заданного в эксперте)
- `--report-format` (по умолчанию: "text") - формат отчета ("text", "json", "html")

**Примеры:**
```
metaexpert backtest examples/expert_binance_ema/main.py
metaexpert backtest my_expert.py --start-date 2024-01-01 --end-date 2024-12-31
metaexpert backtest my_expert.py --report-format json --initial-capital 50000
```

### 3.4. `metaexpert list`

Команда для отображения списка доступных экспертов.

**Синтаксис:**
```
metaexpert list [OPTIONS]
```

**Параметры:**
- `--path`, `-p` (по умолчанию: ./examples) - директория для поиска экспертов
- `--format`, `-f` (по умолчанию: "table") - формат вывода ("table", "json", "list")

**Примеры:**
```
metaexpert list
metaexpert list --path ./my_experts --format json
```

### 3.5. `metaexpert config`

Команда для управления конфигурацией.

**Синтаксис:**
```
metaexpert config [SUBCOMMAND]
```

#### 3.5.1. `metaexpert config show`

Показать текущую конфигурацию.

**Пример:**
```
metaexpert config show
```

#### 3.5.2. `metaexpert config set`

Установить параметр конфигурации.

**Синтаксис:**
```
metaexpert config set <key> <value>
```

**Примеры:**
```
metaexpert config set default_exchange binance
metaexpert config set log_level DEBUG
```

#### 3.5.3. `metaexpert config reset`

Сбросить конфигурацию до значений по умолчанию.

**Пример:**
```
metaexpert config reset
```

## 4. Обработка ошибок и сообщения

### 4.1. Обработка ошибок
CLI должен корректно обрабатывать следующие типы ошибок:
- Неверные параметры командной строки
- Отсутствующие файлы экспертов
- Ошибки аутентификации API
- Ошибки подключения к бирже
- Ошибки во время выполнения эксперта

### 4.2. Форматы вывода
- В случае успеха: краткое сообщение о статусе операции
- В случае ошибки: понятное сообщение об ошибке и код выхода != 0
- Для JSON формата: структурированный вывод ошибки с деталями

## 5. Требования к реализации

### 5.1. Архитектурные требования
- CLI должен быть реализован в модуле `src/metaexpert/cli/`
- Использовать библиотеку Typer для парсинга команд
- Следовать принципу "библиотека-первичной архитектуры" - каждая функция CLI должна быть доступна также как программный API
- Поддерживать JSON и человеко-читаемые форматы вывода

### 5.2. Тестирование
- Минимум 85% покрытия тестами для CLI компонентов
- Unit-тесты для каждой команды
- Integration-тесты для проверки взаимодействия с основной библиотекой
- Тесты должны использовать pytest

### 5.3. Совместимость
- Поддержка Python 3.12+
- Кроссплатформенность (Windows, macOS, Linux)
- Поддержка различных форматов конфигурации (.env, .json, .yaml)

## 6. Примеры использования

### Простой запуск эксперта:
```
metaexpert run examples/expert_binance_ema/main.py
```

### Создание нового эксперта:
```
metaexpert new my_rsi_strategy --exchange bybit --strategy rsi
```

### Запуск бэктеста:
```
metaexpert backtest my_expert.py --start-date 2024-01-01 --end-date 2024-12-31 --initial-capital 25000
```

### Управление конфигурацией:
```
metaexpert config set default_exchange okx
metaexpert config show