# Модуль CLI (Интерфейс командной строки)

## Описание

Модуль CLI (Command Line Interface) предоставляет интерфейс командной строки для настройки и управления торговым ботом. Он включает в себя парсер аргументов, валидацию, генерацию справки и команды для управления шаблонами.

## Структура модуля

### [`__init__.py`](__init__.py)

Основной интерфейс модуля CLI. Предоставляет функции для парсинга аргументов командной строки и добавления команд шаблонов.

#### Функции (`__init__.py`)

- `add_template_commands(parser)` - Добавляет команды, связанные с шаблонами, в парсер аргументов
- `parse_arguments()` - Парсит аргументы командной строки и возвращает распарсенные аргументы
- `parse_cli_arguments(request)` - Точка входа для парсинга аргументов командной строки через HTTP

### [`argument_group_manager.py`](argument_group_manager.py)

Менеджер групп аргументов для организации аргументов командной строки.

#### Классы и структуры

- `ArgumentGroup` - Представляет логическую группу связанных аргументов командной строки
- `CommandLineArgument` - Представляет один аргумент командной строки со своими свойствами
- `ArgumentGroupManager` - Управляет логической группировкой аргументов командной строки для лучшей организации

#### Методы (`ArgumentGroupManager`)

- `add_group(name, description, order)` - Добавляет новую группу аргументов
- `add_argument(arg)` - Добавляет аргумент командной строки в менеджер
- `get_group_arguments(group_name)` - Получает все аргументы, принадлежащие определенной группе
- `get_groups()` - Получает все группы аргументов, отсортированные по порядку
- `get_argument(name)` - Получает определенный аргумент по имени

### [`argument_parser.py`](argument_parser.py)

Парсер аргументов командной строки для торгового бота.

#### Функции (`argument_parser.py`)

- `parse_arguments()` - Парсит аргументы командной строки

### [`argument_validation.py`](argument_validation.py)

Утилиты валидации аргументов для аргументов командной строки.

#### Исключения и утилиты

- `ArgumentValidationError` - Исключение, возникающее при ошибках валидации аргументов
- `ArgumentValidationUtils` - Утилиты для валидации значений аргументов командной строки

#### Методы (`ArgumentValidationUtils`)

- `validate_exchange(exchange, valid_exchanges)` - Валидирует значение биржи
- `validate_percentage(value, min_value, max_value)` - Валидирует процентное значение
- `validate_positive_float(value)` - Валидирует, что значение с плавающей точкой положительное
- `validate_date_format(date_str)` - Валидирует формат даты (ГГГГ-ММ-ДД)
- `validate_trading_pair(pair)` - Валидирует формат торговой пары
- `validate_timeframe(timeframe)` - Валидирует формат таймфрейма
- `validate_log_level(level)` - Валидирует уровень логирования
- `validate_trade_mode(mode)` - Валидирует режим торговли
- `validate_market_type(market_type)` - Валидирует тип рынка

### [`endpoint.py`](endpoint.py)

Точка входа CLI для парсинга аргументов командной строки.

#### Функции (`endpoint.py`)

- `parse_cli_arguments(request)` - Парсит аргументы командной строки и возвращает распарсенные аргументы

### [`help_generator.py`](help_generator.py)

Генератор справочной документации для аргументов командной строки.

#### Классы

- `HelpDocumentationGenerator` - Генерирует пользовательскую документацию для опций командной строки и использования

#### Методы (`HelpDocumentationGenerator`)

- `generate_help_text(program_name, description)` - Генерирует исчерпывающий текст справки для всех аргументов
- `generate_group_help(group_name)` - Генерирует текст справки для определенной группы аргументов
- `generate_usage_examples()` - Генерирует примеры использования для распространенных сценариев

### [`template_commands.py`](template_commands.py)

Команды CLI для создания и управления шаблонами.

#### Функции (`template_commands.py`)

- `create_template(args)` - Создает новый шаблон торговой стратегии
- `list_exchanges(args)` - Перечисляет поддерживаемые биржи
- `list_parameters(args)` - Перечисляет настраиваемые параметры шаблона
- `validate_config(args)` - Валидирует параметры конфигурации
- `add_template_commands(parser)` - Добавляет команды, связанные с шаблонами, в парсер аргументов

## Использование

### Базовое использование

```bash
# Запуск торгового бота с базовыми параметрами
python template.py --exchange binance --pair BTCUSDT --timeframe 1h

# Запуск в разных режимах
python template.py --trade-mode paper
python template.py --trade-mode backtest --start-date 2024-01-01 --end-date 2024-12-31
python template.py --trade-mode live --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET

# Настройка управления рисками
python template.py --stop-loss 2.0 --take-profit 4.0 --size 0.1
```

### Создание шаблонов

```bash
# Создание нового шаблона торговой стратегии
python -m metaexpert --new my_trading_strategy

# Использование команд шаблонов
python template.py create my_strategy ./strategies
python template.py exchanges
python template.py parameters
python template.py validate param1=value1 param2=value2
```

## Группы аргументов

Аргументы командной строки организованы в логические группы для лучшей навигации:

1. **Core Configuration** - Основные настройки для торговой системы
2. **Trading Parameters** - Параметры рынка и торговли
3. **Risk Management** - Управление позициями и контроль рисков
4. **Backtesting** - Параметры для бэктестинга стратегий
5. **Authentication** - Учетные данные API и настройки безопасности
6. **Template Management** - Опции для создания и управления экспертными шаблонами
