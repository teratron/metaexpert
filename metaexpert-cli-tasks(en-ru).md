# MetaExpert CLI - Technical Specification & Implementation Tasks

**Project:** MetaExpert CLI  
**Version:** 1.0.0  
**Status:** Planning  
**Date:** 2025-10-19  
**Author:** Development Team

---

## Table of Contents / Содержание

1. [Executive Summary / Краткое резюме](#executive-summary)
2. [Architecture Overview / Обзор архитектуры](#architecture-overview)
3. [Technical Requirements / Технические требования](#technical-requirements)
4. [Implementation Phases / Фазы реализации](#implementation-phases)
5. [Detailed Task List / Детальный список задач](#detailed-task-list)
6. [Testing Strategy / Стратегия тестирования](#testing-strategy)
7. [Documentation Requirements / Требования к документации](#documentation-requirements)

---

## Executive Summary / Краткое резюме

### English
The MetaExpert CLI provides a comprehensive command-line interface for creating, managing, and running cryptocurrency trading bots. The system supports two operational modes: **Standalone Mode** for quick prototyping and **Workspace Mode** for professional development. An optional **Interactive Mode** enables real-time bot management with live log streaming and command execution.

### Русский
CLI MetaExpert предоставляет комплексный интерфейс командной строки для создания, управления и запуска криптовалютных торговых ботов. Система поддерживает два режима работы: **Standalone Mode** для быстрого прототипирования и **Workspace Mode** для профессиональной разработки. Опциональный **Interactive Mode** обеспечивает управление ботом в реальном времени с потоковым выводом логов и выполнением команд.

---

## Architecture Overview / Обзор архитектуры

### System Components / Компоненты системы

```
metaexpert-cli/
├── Core CLI Framework          # Typer-based command routing
├── Workspace Manager           # Multi-expert project management
├── Expert Lifecycle Manager    # Create, run, stop, monitor experts
├── Interactive Shell           # Real-time command execution
├── Process Manager             # Daemon mode & background processes
├── Configuration Manager       # YAML/ENV configuration handling
├── Logging & Monitoring        # Structured logging & metrics
└── Template Engine             # Expert project scaffolding
```

### Operational Modes / Режимы работы

#### 1. Standalone Mode / Автономный режим
```bash
# Quick start for single expert
metaexpert new my-bot
cd my-bot
metaexpert run
```

#### 2. Workspace Mode / Режим рабочего пространства
```bash
# Professional multi-expert environment
metaexpert workspace create trading-project
cd trading-project
metaexpert new strategy-1
metaexpert new strategy-2
metaexpert run strategy-1
```

#### 3. Interactive Mode / Интерактивный режим
```bash
# Real-time management with split-screen UI
metaexpert run my-bot --interactive

# Live logs + command input:
> status
> pause
> config leverage 5
> stop
```

---

## Technical Requirements / Технические требования

### Dependencies / Зависимости

```toml
[project.dependencies]
typer = ">=0.12.0"              # CLI framework
rich = ">=13.7.0"               # Terminal formatting
click = ">=8.1.0"               # CLI utilities (Typer dependency)
pydantic = ">=2.5.0"            # Configuration validation
pyyaml = ">=6.0.0"              # YAML config support
python-dotenv = ">=1.0.0"       # .env file support
psutil = ">=5.9.0"              # Process management
watchdog = ">=3.0.0"            # File system monitoring

# Optional for advanced features
textual = ">=0.50.0"            # TUI framework (interactive mode)
prompt-toolkit = ">=3.0.0"      # Advanced input handling
questionary = ">=2.0.0"         # Interactive prompts
```

### File Structure / Структура файлов

```
src/metaexpert/
└── cli/
    ├── __init__.py
    ├── main.py                     # Entry point
    ├── commands/                   # Command implementations
    │   ├── __init__.py
    │   ├── new.py                  # Create new expert
    │   ├── run.py                  # Run expert
    │   ├── stop.py                 # Stop expert
    │   ├── status.py               # Status monitoring
    │   ├── logs.py                 # Log viewing
    │   ├── backtest.py             # Backtesting
    │   ├── workspace/              # Workspace commands
    │   │   ├── __init__.py
    │   │   ├── create.py
    │   │   ├── list.py
    │   │   └── delete.py
    │   ├── config/                 # Configuration commands
    │   │   ├── __init__.py
    │   │   ├── show.py
    │   │   ├── set.py
    │   │   └── edit.py
    │   └── interactive/            # Interactive mode
    │       ├── __init__.py
    │       ├── shell.py
    │       └── commands.py
    ├── core/                       # Core functionality
    │   ├── __init__.py
    │   ├── workspace.py            # Workspace manager
    │   ├── expert_manager.py       # Expert lifecycle
    │   ├── process_manager.py      # Process control
    │   ├── config_manager.py       # Configuration handling
    │   └── template_engine.py      # Template generation
    ├── interactive/                # Interactive mode implementation
    │   ├── __init__.py
    │   ├── ui.py                   # UI components
    │   ├── command_handler.py      # Command processing
    │   └── log_streamer.py         # Real-time log display
    ├── utils/                      # Utilities
    │   ├── __init__.py
    │   ├── validators.py           # Input validation
    │   ├── formatters.py           # Output formatting
    │   ├── file_utils.py           # File operations
    │   └── process_utils.py        # Process utilities
    └── templates/                  # Project templates
        ├── __init__.py
        ├── standalone/             # Standalone project template
        │   ├── main.py.jinja2
        │   ├── .env.example.jinja2
        │   ├── README.md.jinja2
        │   └── pyproject.toml.jinja2
        └── workspace/              # Workspace template
            ├── .metaexpert/
            │   └── config.yaml.jinja2
            ├── README.md.jinja2
            └── pyproject.toml.jinja2
```

---

## Implementation Phases / Фазы реализации

### Phase 1: Core CLI Infrastructure (Week 1-2)
### Фаза 1: Базовая инфраструктура CLI (Неделя 1-2)

**Goal / Цель:** Establish foundational CLI architecture with basic commands / Создание базовой архитектуры CLI с основными командами

**Deliverables / Результаты:**
- ✅ Typer-based CLI application structure
- ✅ Command routing and argument parsing
- ✅ Basic error handling and validation
- ✅ Logging infrastructure

### Phase 2: Standalone Mode (Week 3-4)
### Фаза 2: Автономный режим (Неделя 3-4)

**Goal / Цель:** Implement standalone expert creation and execution / Реализация создания и запуска отдельных экспертов

**Deliverables / Результаты:**
- ✅ `metaexpert new` command with template generation
- ✅ `metaexpert run` command for expert execution
- ✅ `metaexpert stop` command for graceful shutdown
- ✅ `metaexpert status` command for monitoring
- ✅ `metaexpert logs` command for log viewing

### Phase 3: Workspace Mode (Week 5-6)
### Фаза 3: Режим рабочего пространства (Неделя 5-6)

**Goal / Цель:** Implement multi-expert workspace management / Реализация управления несколькими экспертами

**Deliverables / Результаты:**
- ✅ Workspace creation and initialization
- ✅ Multi-expert project structure
- ✅ Centralized configuration management
- ✅ Expert discovery and listing

### Phase 4: Interactive Mode (Week 7-8)
### Фаза 4: Интерактивный режим (Неделя 7-8)

**Goal / Цель:** Implement real-time interactive management interface / Реализация интерфейса управления в реальном времени

**Deliverables / Результаты:**
- ✅ Split-screen UI with live logs
- ✅ Command prompt with auto-completion
- ✅ Real-time expert control commands
- ✅ Live metrics display

### Phase 5: Advanced Features (Week 9-10)
### Фаза 5: Расширенные возможности (Неделя 9-10)

**Goal / Цель:** Implement advanced CLI capabilities / Реализация расширенных возможностей CLI

**Deliverables / Результаты:**
- ✅ Daemon mode (background execution)
- ✅ Hot-reload configuration
- ✅ Process attachment (`metaexpert attach`)
- ✅ Advanced monitoring and metrics

### Phase 6: Testing & Documentation (Week 11-12)
### Фаза 6: Тестирование и документация (Неделя 11-12)

**Goal / Цель:** Comprehensive testing and user documentation / Комплексное тестирование и документация

**Deliverables / Результаты:**
- ✅ Unit tests (85%+ coverage)
- ✅ Integration tests
- ✅ CLI usage documentation
- ✅ Tutorial videos/guides

---

## Detailed Task List / Детальный список задач

### Phase 1: Core CLI Infrastructure / Фаза 1: Базовая инфраструктура CLI

#### Task 1.1: Project Setup / Настройка проекта
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 4 hours / 4 часа

**English:**
- [ ] Create CLI module structure under `src/metaexpert/cli/`
- [ ] Configure Typer application in `main.py`
- [ ] Set up entry point in `pyproject.toml`
- [ ] Configure development dependencies

**Русский:**
- [ ] Создать структуру модуля CLI в `src/metaexpert/cli/`
- [ ] Настроить приложение Typer в `main.py`
- [ ] Настроить точку входа в `pyproject.toml`
- [ ] Настроить зависимости для разработки

**Acceptance Criteria / Критерии приемки:**
- `metaexpert --help` displays command list
- `metaexpert --version` shows library version
- All dependencies install correctly

---

#### Task 1.2: Command Router Implementation / Реализация маршрутизатора команд
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 6 hours / 6 часов

**English:**
- [ ] Implement command registration system
- [ ] Create base command class with common functionality
- [ ] Set up command groups (workspace, config, etc.)
- [ ] Implement global options (--log-level, --verbose, etc.)

**Русский:**
- [ ] Реализовать систему регистрации команд
- [ ] Создать базовый класс команды с общей функциональностью
- [ ] Настроить группы команд (workspace, config и т.д.)
- [ ] Реализовать глобальные опции (--log-level, --verbose и т.д.)

**Acceptance Criteria / Критерии приемки:**
- Commands are properly namespaced
- Help text auto-generates from docstrings
- Global options work across all commands

---

#### Task 1.3: Error Handling Framework / Фреймворк обработки ошибок
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 4 hours / 4 часа

**English:**
- [ ] Create custom CLI exception hierarchy
- [ ] Implement global exception handler
- [ ] Add user-friendly error messages with Rich formatting
- [ ] Set up error logging with stack traces

**Русский:**
- [ ] Создать иерархию пользовательских исключений CLI
- [ ] Реализовать глобальный обработчик исключений
- [ ] Добавить понятные сообщения об ошибках с форматированием Rich
- [ ] Настроить логирование ошибок с трассировкой стека

**Acceptance Criteria / Критерии приемки:**
- All exceptions display user-friendly messages
- Debug mode shows full stack traces
- Exit codes follow conventions (0=success, 1=error, 2=invalid usage)

---

#### Task 1.4: Logging Infrastructure / Инфраструктура логирования
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 4 hours / 4 часа

**English:**
- [ ] Integrate with existing MetaLogger
- [ ] Configure CLI-specific log formatting
- [ ] Implement log level filtering
- [ ] Add log file rotation

**Русский:**
- [ ] Интегрировать с существующим MetaLogger
- [ ] Настроить форматирование логов для CLI
- [ ] Реализовать фильтрацию уровней логов
- [ ] Добавить ротацию файлов логов

**Acceptance Criteria / Критерии приемки:**
- CLI logs separate from expert logs
- Log levels work correctly
- Log files don't grow unbounded

---

### Phase 2: Standalone Mode / Фаза 2: Автономный режим

#### Task 2.1: Template Engine / Движок шаблонов
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement Jinja2 template engine
- [ ] Create standalone project template structure
- [ ] Implement variable substitution (exchange, strategy, etc.)
- [ ] Add template validation

**Русский:**
- [ ] Реализовать движок шаблонов Jinja2
- [ ] Создать структуру шаблона автономного проекта
- [ ] Реализовать подстановку переменных (биржа, стратегия и т.д.)
- [ ] Добавить валидацию шаблонов

**Acceptance Criteria / Критерии приемки:**
- Templates render correctly with all variables
- Generated projects have valid structure
- Template validation catches errors

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/template_engine.py`
- `src/metaexpert/cli/templates/standalone/main.py.jinja2`
- `src/metaexpert/cli/templates/standalone/.env.example.jinja2`
- `src/metaexpert/cli/templates/standalone/README.md.jinja2`
- `src/metaexpert/cli/templates/standalone/pyproject.toml.jinja2`

---

#### Task 2.2: `metaexpert new` Command / Команда `metaexpert new`
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Implement project name validation
- [ ] Create directory structure generation
- [ ] Implement template file copying and rendering
- [ ] Add `--force` flag for overwriting existing projects
- [ ] Implement `--exchange`, `--strategy`, `--market-type` options
- [ ] Add post-creation instructions display

**Русский:**
- [ ] Реализовать валидацию имени проекта
- [ ] Создать генерацию структуры каталогов
- [ ] Реализовать копирование и рендеринг файлов шаблонов
- [ ] Добавить флаг `--force` для перезаписи существующих проектов
- [ ] Реализовать опции `--exchange`, `--strategy`, `--market-type`
- [ ] Добавить отображение инструкций после создания

**Acceptance Criteria / Критерии приемки:**
- Project creation succeeds with valid inputs
- `--force` flag overwrites existing projects correctly
- Generated projects are immediately runnable
- Post-creation instructions are clear and helpful

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/new.py`
- `src/metaexpert/cli/utils/validators.py` (project name validation)
- `src/metaexpert/cli/utils/file_utils.py` (file operations)

---

#### Task 2.3: Expert Lifecycle Manager / Менеджер жизненного цикла эксперта
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement expert loading and validation
- [ ] Create process spawning and management
- [ ] Add signal handling for graceful shutdown
- [ ] Implement PID file management
- [ ] Add expert state tracking (running, stopped, error)

**Русский:**
- [ ] Реализовать загрузку и валидацию эксперта
- [ ] Создать запуск и управление процессами
- [ ] Добавить обработку сигналов для корректной остановки
- [ ] Реализовать управление PID-файлами
- [ ] Добавить отслеживание состояния эксперта (работает, остановлен, ошибка)

**Acceptance Criteria / Критерии приемки:**
- Experts load correctly from Python files
- Process management handles all edge cases
- Graceful shutdown works reliably
- State tracking persists across CLI invocations

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/expert_manager.py`
- `src/metaexpert/cli/core/process_manager.py`
- `src/metaexpert/cli/utils/process_utils.py`

---

#### Task 2.4: `metaexpert run` Command / Команда `metaexpert run`
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Implement expert file loading
- [ ] Add trade mode selection (paper, live, backtest)
- [ ] Implement parameter overriding from CLI
- [ ] Add background execution (`--detach` flag)
- [ ] Implement process monitoring and restart on failure
- [ ] Add configuration file loading (`.env`)

**Русский:**
- [ ] Реализовать загрузку файла эксперта
- [ ] Добавить выбор режима торговли (paper, live, backtest)
- [ ] Реализовать переопределение параметров из CLI
- [ ] Добавить фоновое выполнение (флаг `--detach`)
- [ ] Реализовать мониторинг процесса и перезапуск при сбое
- [ ] Добавить загрузку файла конфигурации (`.env`)

**Acceptance Criteria / Критерии приемки:**
- Expert runs successfully in all trade modes
- CLI parameters override code parameters
- Background mode works correctly
- Process monitoring detects failures

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/run.py`

---

#### Task 2.5: `metaexpert stop` Command / Команда `metaexpert stop`
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 6 hours / 6 часов

**English:**
- [ ] Implement expert discovery by name/ID
- [ ] Add graceful shutdown with SIGTERM
- [ ] Implement force kill with SIGKILL (`--force` flag)
- [ ] Add timeout handling (`--timeout` option)
- [ ] Implement cleanup of PID files and state

**Русский:**
- [ ] Реализовать поиск эксперта по имени/ID
- [ ] Добавить корректную остановку с помощью SIGTERM
- [ ] Реализовать принудительное завершение с помощью SIGKILL (флаг `--force`)
- [ ] Добавить обработку таймаута (опция `--timeout`)
- [ ] Реализовать очистку PID-файлов и состояния

**Acceptance Criteria / Критерии приемки:**
- Experts stop gracefully within timeout
- Force kill works when graceful shutdown fails
- State files cleaned up correctly

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/stop.py`

---

#### Task 2.6: `metaexpert status` Command / Команда `metaexpert status`
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement running expert discovery
- [ ] Add status information collection (uptime, PnL, etc.)
- [ ] Implement table formatting with Rich
- [ ] Add JSON output format option
- [ ] Implement watch mode (`--watch` flag)
- [ ] Add filtering by expert name (`--expert` option)

**Русский:**
- [ ] Реализовать поиск работающих экспертов
- [ ] Добавить сбор информации о статусе (время работы, PnL и т.д.)
- [ ] Реализовать табличное форматирование с помощью Rich
- [ ] Добавить опцию вывода в формате JSON
- [ ] Реализовать режим наблюдения (флаг `--watch`)
- [ ] Добавить фильтрацию по имени эксперта (опция `--expert`)

**Acceptance Criteria / Критерии приемки:**
- Status displays all running experts
- Watch mode updates in real-time
- JSON output is valid and complete

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/status.py`
- `src/metaexpert/cli/utils/formatters.py` (table formatting)

---

#### Task 2.7: `metaexpert logs` Command / Команда `metaexpert logs`
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 6 hours / 6 часов

**English:**
- [ ] Implement log file discovery
- [ ] Add log level filtering (`--level` option)
- [ ] Implement line limiting (`--limit` option)
- [ ] Add follow mode (`--follow` flag) like `tail -f`
- [ ] Implement expert filtering (`--expert` option)
- [ ] Add timestamp formatting

**Русский:**
- [ ] Реализовать поиск файлов логов
- [ ] Добавить фильтрацию по уровню логов (опция `--level`)
- [ ] Реализовать ограничение количества строк (опция `--limit`)
- [ ] Добавить режим отслеживания (флаг `--follow`) как `tail -f`
- [ ] Реализовать фильтрацию по эксперту (опция `--expert`)
- [ ] Добавить форматирование временных меток

**Acceptance Criteria / Критерии приемки:**
- Logs display correctly with filtering
- Follow mode streams new log entries
- Performance is acceptable for large log files

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/logs.py`

---

#### Task 2.8: `metaexpert backtest` Command / Команда `metaexpert backtest`
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement date range parsing and validation
- [ ] Add backtest parameter configuration
- [ ] Implement results collection and display
- [ ] Add report generation (text, JSON, HTML formats)
- [ ] Implement results saving (`--save-results` option)
- [ ] Add performance metrics calculation

**Русский:**
- [ ] Реализовать разбор и валидацию диапазона дат
- [ ] Добавить конфигурацию параметров бэктестинга
- [ ] Реализовать сбор и отображение результатов
- [ ] Добавить генерацию отчетов (форматы text, JSON, HTML)
- [ ] Реализовать сохранение результатов (опция `--save-results`)
- [ ] Добавить расчет метрик производительности

**Acceptance Criteria / Критерии приемки:**
- Backtest runs successfully with date range
- Results display all relevant metrics
- Report formats are correctly generated

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/backtest.py`

---

### Phase 3: Workspace Mode / Фаза 3: Режим рабочего пространства

#### Task 3.1: Workspace Manager Implementation / Реализация менеджера рабочего пространства
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Implement workspace configuration schema (YAML)
- [ ] Create workspace initialization logic
- [ ] Add expert discovery within workspace
- [ ] Implement workspace state management
- [ ] Add workspace validation
- [ ] Implement configuration inheritance

**Русский:**
- [ ] Реализовать схему конфигурации рабочего пространства (YAML)
- [ ] Создать логику инициализации рабочего пространства
- [ ] Добавить поиск экспертов внутри рабочего пространства
- [ ] Реализовать управление состоянием рабочего пространства
- [ ] Добавить валидацию рабочего пространства
- [ ] Реализовать наследование конфигурации

**Acceptance Criteria / Критерии приемки:**
- Workspace creates valid directory structure
- Configuration loads and validates correctly
- Expert discovery finds all experts in workspace

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/workspace.py`
- `src/metaexpert/cli/templates/workspace/.metaexpert/config.yaml.jinja2`

---

#### Task 3.2: `metaexpert workspace create` Command / Команда `metaexpert workspace create`
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement workspace name validation
- [ ] Create workspace directory structure
- [ ] Generate workspace configuration files
- [ ] Initialize virtual environment
- [ ] Add post-creation instructions
- [ ] Implement `--force` flag for overwriting

**Русский:**
- [ ] Реализовать валидацию имени рабочего пространства
- [ ] Создать структуру каталогов рабочего пространства
- [ ] Сгенерировать файлы конфигурации рабочего пространства
- [ ] Инициализировать виртуальное окружение
- [ ] Добавить инструкции после создания
- [ ] Реализовать флаг `--force` для перезаписи

**Acceptance Criteria / Критерии приемки:**
- Workspace creates successfully
- All configuration files are valid
- Virtual environment is properly initialized

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/workspace/create.py`

---

#### Task 3.3: `metaexpert workspace list` Command / Команда `metaexpert workspace list`
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 4 hours / 4 часа

**English:**
- [ ] Implement workspace discovery
- [ ] Add workspace information collection
- [ ] Implement table formatting
- [ ] Add JSON output format option

**Русский:**
- [ ] Реализовать поиск рабочих пространств
- [ ] Добавить сбор информации о рабочих пространствах
- [ ] Реализовать табличное форматирование
- [ ] Добавить опцию вывода в формате JSON

**Acceptance Criteria / Критерии приемки:**
- All workspaces are discovered correctly
- Information displays in clear format

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/workspace/list.py`

---

#### Task 3.4: `metaexpert workspace delete` Command / Команда `metaexpert workspace delete`
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 4 hours / 4 часа

**English:**
- [ ] Implement workspace deletion with confirmation
- [ ] Add safety checks (running experts, etc.)
- [ ] Implement force deletion (`--force` flag)
- [ ] Add cleanup of all related files

**Русский:**
- [ ] Реализовать удаление рабочего пространства с подтверждением
- [ ] Добавить проверки безопасности (работающие эксперты и т.д.)
- [ ] Реализовать принудительное удаление (флаг `--force`)
- [ ] Добавить очистку всех связанных файлов

**Acceptance Criteria / Критерии приемки:**
- Deletion requires confirmation by default
- Running experts prevent deletion without force
- All files are properly cleaned up

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/workspace/delete.py`

---

#### Task 3.5: Context-Aware Command Execution / Контекстное выполнение команд
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement workspace context detection
- [ ] Add automatic workspace/standalone mode switching
- [ ] Implement relative path resolution
- [ ] Add workspace configuration loading

**Русский:**
- [ ] Реализовать определение контекста рабочего пространства
- [ ] Добавить автоматическое переключение режимов workspace/standalone
- [ ] Реализовать разрешение относительных путей
- [ ] Добавить загрузку конфигурации рабочего пространства

**Acceptance Criteria / Критерии приемки:**
- Commands detect workspace context automatically
- Path resolution works correctly in both modes
- Configuration inheritance works properly

**Files to Modify / Файлы для изменения:**
- `src/metaexpert/cli/core/workspace.py`
- `src/metaexpert/cli/commands/run.py`
- `src/metaexpert/cli/commands/new.py`

---

### Phase 4: Interactive Mode / Фаза 4: Интерактивный режим

#### Task 4.1: Interactive UI Framework / Фреймворк интерактивного интерфейса
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 16 hours / 16 часов

**English:**
- [ ] Implement split-screen layout with Textual
- [ ] Create log display panel with scrolling
- [ ] Implement command input area with prompt
- [ ] Add status bar with live metrics
- [ ] Implement keyboard shortcuts
- [ ] Add color scheme and theming

**Русский:**
- [ ] Реализовать разделенный экран с помощью Textual
- [ ] Создать панель отображения логов с прокруткой
- [ ] Реализовать область ввода команд с подсказкой
- [ ] Добавить строку состояния с метриками в реальном времени
- [ ] Реализовать горячие клавиши
- [ ] Добавить цветовую схему и темы

**Acceptance Criteria / Критерии приемки:**
- UI renders correctly in terminal
- Log panel scrolls smoothly
- Command input is responsive
- Status bar updates in real-time

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/interactive/ui.py`
- `src/metaexpert/cli/interactive/widgets.py`
- `src/metaexpert/cli/interactive/theme.py`

---

#### Task 4.2: Log Streaming Implementation / Реализация потоковой передачи логов
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement real-time log file monitoring
- [ ] Add log parsing and formatting
- [ ] Implement log level filtering
- [ ] Add automatic scrolling with scroll lock
- [ ] Implement log search functionality
- [ ] Add log export from interactive mode

**Русский:**
- [ ] Реализовать мониторинг файлов логов в реальном времени
- [ ] Добавить разбор и форматирование логов
- [ ] Реализовать фильтрацию по уровню логов
- [ ] Добавить автоматическую прокрутку с блокировкой прокрутки
- [ ] Реализовать функциональность поиска по логам
- [ ] Добавить экспорт логов из интерактивного режима

**Acceptance Criteria / Критерии приемки:**
- Logs stream in real-time with minimal delay
- Filtering works correctly
- Search finds relevant log entries
- Performance is acceptable for high log volume

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/interactive/log_streamer.py`
- `src/metaexpert/cli/interactive/log_parser.py`

---

#### Task 4.3: Interactive Command Handler / Обработчик интерактивных команд
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Implement command parser for interactive mode
- [ ] Add command auto-completion
- [ ] Implement command history with up/down arrows
- [ ] Add inline help for commands
- [ ] Implement command aliases
- [ ] Add command validation and error handling

**Русский:**
- [ ] Реализовать парсер команд для интерактивного режима
- [ ] Добавить автодополнение команд
- [ ] Реализовать историю команд со стрелками вверх/вниз
- [ ] Добавить встроенную справку по командам
- [ ] Реализовать псевдонимы команд
- [ ] Добавить валидацию команд и обработку ошибок

**Acceptance Criteria / Критерии приемки:**
- Command parsing works reliably
- Auto-completion suggests correct commands
- Command history persists between sessions
- Error messages are clear and helpful

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/interactive/command_handler.py`
- `src/metaexpert/cli/interactive/command_parser.py`
- `src/metaexpert/cli/interactive/completer.py`

---

#### Task 4.4: Real-Time Expert Control / Управление экспертом в реальном времени
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement `status` command (show current state)
- [ ] Implement `pause` command (pause trading)
- [ ] Implement `resume` command (resume trading)
- [ ] Implement `positions` command (show open positions)
- [ ] Implement `orders` command (show active orders)
- [ ] Implement `pnl` command (show profit/loss)
- [ ] Implement `config` command (change configuration on-the-fly)
- [ ] Implement `stop` command (graceful shutdown)

**Русский:**
- [ ] Реализовать команду `status` (показать текущее состояние)
- [ ] Реализовать команду `pause` (приостановить торговлю)
- [ ] Реализовать команду `resume` (возобновить торговлю)
- [ ] Реализовать команду `positions` (показать открытые позиции)
- [ ] Реализовать команду `orders` (показать активные ордера)
- [ ] Реализовать команду `pnl` (показать прибыль/убыток)
- [ ] Реализовать команду `config` (изменить конфигурацию на лету)
- [ ] Реализовать команду `stop` (корректная остановка)

**Acceptance Criteria / Критерии приемки:**
- All commands execute successfully
- Expert state changes are reflected immediately
- Configuration changes apply without restart
- Commands provide clear feedback

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/interactive/commands.py`
- `src/metaexpert/cli/interactive/expert_controller.py`

---

#### Task 4.5: Metrics Dashboard / Панель метрик
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement live metrics collection
- [ ] Add metrics display panel
- [ ] Implement sparkline graphs for key metrics
- [ ] Add customizable metrics selection
- [ ] Implement metrics export
- [ ] Add alerts for threshold breaches

**Русский:**
- [ ] Реализовать сбор метрик в реальном времени
- [ ] Добавить панель отображения метрик
- [ ] Реализовать графики sparkline для ключевых метрик
- [ ] Добавить настраиваемый выбор метрик
- [ ] Реализовать экспорт метрик
- [ ] Добавить оповещения при превышении порогов

**Acceptance Criteria / Критерии приемки:**
- Metrics update in real-time
- Graphs render correctly in terminal
- Alerts trigger at correct thresholds

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/interactive/metrics.py`
- `src/metaexpert/cli/interactive/metrics_display.py`

---

#### Task 4.6: Integration with `run` Command / Интеграция с командой `run`
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 6 hours / 6 часов

**English:**
- [ ] Add `--interactive` flag to `run` command
- [ ] Implement mode switching logic
- [ ] Add graceful fallback to non-interactive mode
- [ ] Implement session persistence
- [ ] Add configuration for default mode

**Русский:**
- [ ] Добавить флаг `--interactive` к команде `run`
- [ ] Реализовать логику переключения режимов
- [ ] Добавить корректный откат к неинтерактивному режиму
- [ ] Реализовать сохранение сессии
- [ ] Добавить конфигурацию режима по умолчанию

**Acceptance Criteria / Критерии приемки:**
- `--interactive` flag activates interactive mode
- Fallback works when Textual is not available
- Mode preference persists across sessions

**Files to Modify / Файлы для изменения:**
- `src/metaexpert/cli/commands/run.py`

---

### Phase 5: Advanced Features / Фаза 5: Расширенные возможности

#### Task 5.1: Daemon Mode Implementation / Реализация режима демона
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Implement process daemonization
- [ ] Add PID file management for daemons
- [ ] Implement daemon logging configuration
- [ ] Add daemon status checking
- [ ] Implement daemon restart functionality
- [ ] Add multiple daemon management

**Русский:**
- [ ] Реализовать демонизацию процесса
- [ ] Добавить управление PID-файлами для демонов
- [ ] Реализовать конфигурацию логирования демона
- [ ] Добавить проверку статуса демона
- [ ] Реализовать функциональность перезапуска демона
- [ ] Добавить управление несколькими демонами

**Acceptance Criteria / Критерии приемки:**
- Experts run reliably as daemons
- Daemon status is accurately reported
- Daemon logs are properly configured
- Multiple daemons can run simultaneously

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/daemon.py`
- `src/metaexpert/cli/commands/daemon.py`

---

#### Task 5.2: Process Attachment / Подключение к процессу
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement `metaexpert attach` command
- [ ] Add process discovery by name/PID
- [ ] Implement log streaming from running expert
- [ ] Add detach functionality (Ctrl+D)
- [ ] Implement signal forwarding to expert

**Русский:**
- [ ] Реализовать команду `metaexpert attach`
- [ ] Добавить поиск процесса по имени/PID
- [ ] Реализовать потоковую передачу логов от работающего эксперта
- [ ] Добавить функциональность отключения (Ctrl+D)
- [ ] Реализовать пересылку сигналов эксперту

**Acceptance Criteria / Критерии приемки:**
- Attach connects to running expert successfully
- Logs stream in real-time after attachment
- Detach doesn't stop the expert
- Signals are forwarded correctly

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/attach.py`

---

#### Task 5.3: Hot-Reload Configuration / Горячая перезагрузка конфигурации
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement configuration file watching
- [ ] Add configuration reload without restart
- [ ] Implement parameter validation on reload
- [ ] Add reload notifications
- [ ] Implement selective parameter reloading
- [ ] Add reload history and rollback

**Русский:**
- [ ] Реализовать отслеживание файлов конфигурации
- [ ] Добавить перезагрузку конфигурации без перезапуска
- [ ] Реализовать валидацию параметров при перезагрузке
- [ ] Добавить уведомления о перезагрузке
- [ ] Реализовать выборочную перезагрузку параметров
- [ ] Добавить историю перезагрузок и откат

**Acceptance Criteria / Критерии приемки:**
- Configuration reloads automatically on file change
- Invalid configurations are rejected
- Expert continues running during reload
- Rollback works correctly on errors

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/config_watcher.py`
- `src/metaexpert/cli/core/hot_reload.py`

---

#### Task 5.4: Advanced Monitoring / Расширенный мониторинг
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 10 hours / 10 часов

**English:**
- [ ] Implement performance metrics collection
- [ ] Add resource usage monitoring (CPU, memory)
- [ ] Implement trade statistics aggregation
- [ ] Add historical metrics storage
- [ ] Implement metrics export (Prometheus, JSON)
- [ ] Add alerting system for anomalies

**Русский:**
- [ ] Реализовать сбор метрик производительности
- [ ] Добавить мониторинг использования ресурсов (CPU, память)
- [ ] Реализовать агрегацию статистики торговли
- [ ] Добавить хранение исторических метрик
- [ ] Реализовать экспорт метрик (Prometheus, JSON)
- [ ] Добавить систему оповещений об аномалиях

**Acceptance Criteria / Критерии приемки:**
- Metrics are collected accurately
- Historical data is stored efficiently
- Export formats are standard-compliant
- Alerts trigger on anomalies

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/core/monitoring.py`
- `src/metaexpert/cli/core/metrics_collector.py`
- `src/metaexpert/cli/core/alerting.py`

---

#### Task 5.5: Configuration Management / Управление конфигурацией
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Implement `metaexpert config show` command
- [ ] Implement `metaexpert config set` command
- [ ] Implement `metaexpert config get` command
- [ ] Implement `metaexpert config edit` command (opens in editor)
- [ ] Add configuration validation
- [ ] Implement configuration templates

**Русский:**
- [ ] Реализовать команду `metaexpert config show`
- [ ] Реализовать команду `metaexpert config set`
- [ ] Реализовать команду `metaexpert config get`
- [ ] Реализовать команду `metaexpert config edit` (открывает в редакторе)
- [ ] Добавить валидацию конфигурации
- [ ] Реализовать шаблоны конфигурации

**Acceptance Criteria / Критерии приемки:**
- All config commands work correctly
- Validation catches invalid values
- Editor integration works smoothly

**Files to Create / Файлы для создания:**
- `src/metaexpert/cli/commands/config/show.py`
- `src/metaexpert/cli/commands/config/set.py`
- `src/metaexpert/cli/commands/config/get.py`
- `src/metaexpert/cli/commands/config/edit.py`

---

### Phase 6: Testing & Documentation / Фаза 6: Тестирование и документация

#### Task 6.1: Unit Tests / Модульные тесты
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 20 hours / 20 часов

**English:**
- [ ] Write tests for all CLI commands
- [ ] Write tests for template engine
- [ ] Write tests for workspace manager
- [ ] Write tests for expert manager
- [ ] Write tests for process manager
- [ ] Write tests for configuration manager
- [ ] Achieve 85%+ code coverage

**Русский:**
- [ ] Написать тесты для всех команд CLI
- [ ] Написать тесты для движка шаблонов
- [ ] Написать тесты для менеджера рабочего пространства
- [ ] Написать тесты для менеджера экспертов
- [ ] Написать тесты для менеджера процессов
- [ ] Написать тесты для менеджера конфигурации
- [ ] Достичь покрытия кода 85%+

**Acceptance Criteria / Критерии приемки:**
- All tests pass
- Code coverage meets 85% minimum
- Edge cases are covered

**Files to Create / Файлы для создания:**
- `tests/unit/cli/test_commands.py`
- `tests/unit/cli/test_template_engine.py`
- `tests/unit/cli/test_workspace.py`
- `tests/unit/cli/test_expert_manager.py`
- `tests/unit/cli/test_process_manager.py`

---

#### Task 6.2: Integration Tests / Интеграционные тесты
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 16 hours / 16 часов

**English:**
- [ ] Write end-to-end tests for project creation workflow
- [ ] Write tests for expert execution lifecycle
- [ ] Write tests for workspace management
- [ ] Write tests for interactive mode
- [ ] Write tests for daemon mode
- [ ] Test all command combinations

**Русский:**
- [ ] Написать сквозные тесты для рабочего процесса создания проекта
- [ ] Написать тесты для жизненного цикла выполнения эксперта
- [ ] Написать тесты для управления рабочим пространством
- [ ] Написать тесты для интерактивного режима
- [ ] Написать тесты для режима демона
- [ ] Протестировать все комбинации команд

**Acceptance Criteria / Критерии приемки:**
- All integration tests pass
- Workflows complete successfully
- Command interactions work correctly

**Files to Create / Файлы для создания:**
- `tests/integration/cli/test_workflows.py`
- `tests/integration/cli/test_expert_lifecycle.py`
- `tests/integration/cli/test_workspace_workflows.py`

---

#### Task 6.3: CLI User Guide / Руководство пользователя CLI
**Priority:** HIGH / ВЫСОКИЙ  
**Estimate:** 12 hours / 12 часов

**English:**
- [ ] Write getting started guide
- [ ] Document all commands with examples
- [ ] Create workflow tutorials
- [ ] Add troubleshooting section
- [ ] Create configuration reference
- [ ] Add FAQ section

**Русский:**
- [ ] Написать руководство по началу работы
- [ ] Документировать все команды с примерами
- [ ] Создать учебники по рабочим процессам
- [ ] Добавить раздел устранения неполадок
- [ ] Создать справочник конфигурации
- [ ] Добавить раздел FAQ

**Acceptance Criteria / Критерии приемки:**
- Documentation covers all commands
- Examples are clear and executable
- Troubleshooting addresses common issues

**Files to Create / Файлы для создания:**
- `docs/cli/getting-started.md`
- `docs/cli/commands-reference.md`
- `docs/cli/workflows.md`
- `docs/cli/troubleshooting.md`
- `docs/cli/configuration.md`
- `docs/cli/faq.md`

---

#### Task 6.4: Video Tutorials / Видеоуроки
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 16 hours / 16 часов

**English:**
- [ ] Create "Quick Start" video (5-10 min)
- [ ] Create "Creating Your First Expert" video (10-15 min)
- [ ] Create "Workspace Mode" video (10-15 min)
- [ ] Create "Interactive Mode" video (10-15 min)
- [ ] Create "Advanced Features" video (15-20 min)
- [ ] Upload to YouTube/documentation site

**Русский:**
- [ ] Создать видео "Быстрый старт" (5-10 мин)
- [ ] Создать видео "Создание первого эксперта" (10-15 мин)
- [ ] Создать видео "Режим рабочего пространства" (10-15 мин)
- [ ] Создать видео "Интерактивный режим" (10-15 мин)
- [ ] Создать видео "Расширенные возможности" (15-20 мин)
- [ ] Загрузить на YouTube/сайт документации

**Acceptance Criteria / Критерии приемки:**
- Videos are clear and well-paced
- All major features are covered
- Videos are accessible on documentation site

---

#### Task 6.5: API Documentation / Документация API
**Priority:** MEDIUM / СРЕДНИЙ  
**Estimate:** 8 hours / 8 часов

**English:**
- [ ] Document all public CLI classes
- [ ] Document all public methods
- [ ] Add docstring examples
- [ ] Generate API reference with Sphinx
- [ ] Add cross-references to user guide

**Русский:**
- [ ] Документировать все публичные классы CLI
- [ ] Документировать все публичные методы
- [ ] Добавить примеры в docstring
- [ ] Сгенерировать справочник API с помощью Sphinx
- [ ] Добавить перекрестные ссылки на руководство пользователя

**Acceptance Criteria / Критерии приемки:**
- All public APIs are documented
- Documentation builds without errors
- Examples are clear and executable

**Files to Create / Файлы для создания:**
- `docs/api/cli-reference.rst`

---

## Testing Strategy / Стратегия тестирования

### Test Coverage Requirements / Требования к покрытию тестами

**English:**
- Minimum 85% code coverage for CLI module
- 100% coverage for critical paths (expert lifecycle, process management)
- All commands must have integration tests
- Interactive mode requires manual QA testing

**Русский:**
- Минимум 85% покрытия кода для модуля CLI
- 100% покрытие критических путей (жизненный цикл эксперта, управление процессами)
- Все команды должны иметь интеграционные тесты
- Интерактивный режим требует ручного QA тестирования

### Test Types / Типы тестов

#### Unit Tests / Модульные тесты
- Test individual functions and methods
- Mock external dependencies
- Use pytest fixtures for test data
- Test edge cases and error conditions

#### Integration Tests / Интеграционные тесты
- Test command workflows end-to-end
- Use temporary directories for file operations
- Test inter-component communication
- Verify state persistence

#### Manual QA Tests / Ручные QA тесты
- Test interactive mode UI
- Verify keyboard shortcuts
- Test terminal compatibility (different terminals/OSes)
- Verify performance under load

### CI/CD Integration / Интеграция CI/CD

**English:**
- Run all tests on every commit
- Generate coverage reports
- Block merges on test failures
- Run linting (ruff) before tests

**Русский:**
- Запускать все тесты при каждом коммите
- Генерировать отчеты о покрытии
- Блокировать слияния при падении тестов
- Запускать линтинг (ruff) перед тестами

---

## Documentation Requirements / Требования к документации

### User Documentation / Пользовательская документация

1. **Getting Started Guide / Руководство по началу работы**
   - Installation instructions
   - First expert creation
   - Basic command usage

2. **Command Reference / Справочник команд**
   - All commands with syntax
   - All options and flags
   - Usage examples

3. **Tutorials / Учебники**
   - Standalone mode workflow
   - Workspace mode workflow
   - Interactive mode usage
   - Advanced features

4. **Troubleshooting / Устранение неполадок**
   - Common errors and solutions
   - Debug mode usage
   - Log analysis

### Developer Documentation / Документация для разработчиков

1. **Architecture Overview / Обзор архитектуры**
   - System components
   - Design decisions
   - Extension points

2. **API Reference / Справочник API**
   - All public classes and methods
   - Usage examples
   - Best practices

3. **Contributing Guide / Руководство по внесению вклада**
   - Development setup
   - Coding standards
   - Testing requirements
   - Pull request process

---

## Success Criteria / Критерии успеха

### English:
- [ ] All Phase 1-6 tasks completed
- [ ] 85%+ test coverage achieved
- [ ] Documentation complete and accurate
- [ ] All commands work reliably
- [ ] Interactive mode provides excellent UX
- [ ] Performance meets benchmarks (commands respond <200ms)
- [ ] No critical bugs in production

### Русский:
- [ ] Все задачи Фаз 1-6 выполнены
- [ ] Достигнуто покрытие тестами 85%+
- [ ] Документация полная и точная
- [ ] Все команды работают надежно
- [ ] Интерактивный режим обеспечивает отличный UX
- [ ] Производительность соответствует эталонам (команды отвечают <200мс)
- [ ] Отсутствуют критические ошибки в продакшене

---

## Timeline / Временные рамки

### Total Estimated Time / Общее расчетное время
- **Phase 1:** 18 hours / 18 часов
- **Phase 2:** 58 hours / 58 часов
- **Phase 3:** 36 hours / 36 часов
- **Phase 4:** 56 hours / 56 часов
- **Phase 5:** 48 hours / 48 часов
- **Phase 6:** 72 hours / 72 часов

**Total: 288 hours / ~36 working days / ~7-8 weeks for 1 developer**
**Всего: 288 часов / ~36 рабочих дней / ~7-8 недель для 1 разработчика**

### Recommended Team / Рекомендуемая команда
- 1 Senior Python Developer (CLI architecture, core features)
- 1 Python Developer (commands implementation, testing)
- 1 Technical Writer (documentation)
- 1 QA Engineer (testing, part-time)

**Timeline with team: 4-6 weeks**
**Временные рамки с командой: 4-6 недель**

---

## Risk Assessment / Оценка рисков

### High Risk / Высокий риск
1. **Interactive Mode Complexity / Сложность интерактивного режима**
   - Mitigation: Implement as optional feature, extensive testing
   
2. **Cross-Platform Compatibility / Кроссплатформенная совместимость**
   - Mitigation: Test on Windows, macOS, Linux early

3. **Process Management Edge Cases / Крайние случаи управления процессами**
   - Mitigation: Comprehensive integration tests, signal handling

### Medium Risk / Средний риск
1. **Performance Under Load / Производительность под нагрузкой**
   - Mitigation: Benchmark early, optimize hot paths

2. **Documentation Completeness / Полнота документации**
   - Mitigation: Write docs alongside code, peer review

### Low Risk / Низкий риск
1. **Template Engine Issues / Проблемы движка шаблонов**
   - Mitigation: Use proven library (Jinja2), validate templates

---

## Appendix: Command Examples / Приложение: Примеры команд

### Quick Reference / Быстрая справка

```bash
# Create new expert
metaexpert new my-bot --exchange binance --strategy ema

# Run expert
metaexpert run my-bot --mode paper

# Run in interactive mode
metaexpert run my-bot --interactive

# Run in background
metaexpert run my-bot --detach

# Check status
metaexpert status

# View logs
metaexpert logs my-bot --follow

# Stop expert
metaexpert stop my-bot

# Create workspace
metaexpert workspace create trading-project

# Backtest expert
metaexpert backtest my-bot --start-date 2024-01-01 --end-date 2024-12-31

# Attach to running expert
metaexpert attach my-bot

# Show configuration
metaexpert config show

# Set configuration value
metaexpert config set default_exchange binance
```
