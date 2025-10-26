# 🚀 Путь к 10/10: Полное Руководство Совершенствования CLI

---

## 1. 📐 АРХИТЕКТУРА: 8/10 → 10/10

### Что Сейчас (8/10):
✅ Хорошее разделение на слои (commands, core, process, templates, utils)  
✅ Использование Pydantic для конфигурации  
✅ Модульная структура  
❌ Недостатки: Нет четкого паттерна для расширения, отсутствует middleware, нет DI контейнера

### Что Добавить для 10/10:

#### 1.1. Dependency Injection контейнер
```python
# src/metaexpert/cli/core/container.py
from typing import Any, Callable, Generic, TypeVar

T = TypeVar('T')

class DIContainer:
    """Simple DI container for CLI services."""
    
    def __init__(self):
        self._services: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}
        self._singletons: dict[type, Any] = {}
    
    def register(self, interface: type[T], factory: Callable[..., T], singleton: bool = True) -> None:
        """Register service factory."""
        if singleton:
            self._factories[interface] = factory
        else:
            self._services[interface] = factory
    
    def get(self, interface: type[T]) -> T:
        """Get service instance."""
        # Проверяем кэш синглтонов
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Создаем через фабрику
        factory = self._factories.get(interface)
        if factory:
            instance = factory()
            self._singletons[interface] = instance
            return instance
        
        raise ValueError(f"Service {interface.__name__} not registered")

# Глобальный контейнер
_container = DIContainer()

# Регистрация сервисов
_container.register(CLIConfig, lambda: CLIConfig.load(), singleton=True)
_container.register(OutputFormatter, lambda: OutputFormatter(), singleton=True)
_container.register(ProcessManager, lambda: ProcessManager(Path("/var/run/metaexpert")), singleton=True)
_container.register(TemplateGenerator, lambda: TemplateGenerator(), singleton=True)

def get_container() -> DIContainer:
    """Get DI container instance."""
    return _container
```

**Преимущества:**
- Легче тестировать (подменять зависимости)
- Централизованное управление зависимостями
- Упрощает добавление новых компонентов

#### 1.2. Middleware система
```python
# src/metaexpert/cli/core/middleware.py
from abc import ABC, abstractmethod
from typing import Callable, Any
import functools

class Middleware(ABC):
    """Base middleware for CLI commands."""
    
    @abstractmethod
    def before(self, command_name: str, **kwargs) -> None:
        """Execute before command."""
        pass
    
    @abstractmethod
    def after(self, command_name: str, result: Any) -> None:
        """Execute after command."""
        pass

class PerformanceMiddleware(Middleware):
    """Track command execution time."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def before(self, command_name: str, **kwargs) -> None:
        self.start_time = time.time()
        self.logger.debug(f"command started", command=command_name)
    
    def after(self, command_name: str, result: Any) -> None:
        duration = time.time() - self.start_time
        self.logger.info(
            f"command completed",
            command=command_name,
            duration_ms=round(duration * 1000),
        )

class ErrorRecoveryMiddleware(Middleware):
    """Handle errors gracefully."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def before(self, command_name: str, **kwargs) -> None:
        pass
    
    def after(self, command_name: str, result: Any) -> None:
        if isinstance(result, Exception):
            self.logger.error(
                f"command failed",
                command=command_name,
                error=str(result),
            )

class MiddlewareManager:
    """Manage middleware execution."""
    
    def __init__(self):
        self.middlewares: list[Middleware] = []
    
    def register(self, middleware: Middleware) -> None:
        """Register middleware."""
        self.middlewares.append(middleware)
    
    def command_decorator(self, command_name: str):
        """Decorator for commands."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for mw in self.middlewares:
                    mw.before(command_name, **kwargs)
                
                try:
                    result = func(*args, **kwargs)
                    for mw in self.middlewares:
                        mw.after(command_name, result)
                    return result
                except Exception as e:
                    for mw in self.middlewares:
                        mw.after(command_name, e)
                    raise
            
            return wrapper
        return decorator

# В app.py
_middleware_manager = MiddlewareManager()
_middleware_manager.register(PerformanceMiddleware())
_middleware_manager.register(ErrorRecoveryMiddleware())

@app.command()
@_middleware_manager.command_decorator("new")
def cmd_new(...):
    pass
```

**Преимущества:**
- Кросс-категориальная логика (логирование, метрики, кэширование)
- Не загромождает команды
- Легко добавлять/удалять функциональность

#### 1.3. Plugin система
```python
# src/metaexpert/cli/core/plugins.py
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path

class CliPlugin(ABC):
    """Base class for CLI plugins."""
    
    name: str
    version: str
    description: str
    
    @abstractmethod
    def register_commands(self, app: typer.Typer) -> None:
        """Register custom commands."""
        pass
    
    @abstractmethod
    def register_middleware(self, manager: MiddlewareManager) -> None:
        """Register middleware."""
        pass

class PluginManager:
    """Manage CLI plugins."""
    
    def __init__(self):
        self.plugins: dict[str, CliPlugin] = {}
        self.logger = get_logger(__name__)
    
    def load_plugins(self, plugin_dir: Path) -> None:
        """Load plugins from directory."""
        if not plugin_dir.exists():
            return
        
        for plugin_file in plugin_dir.glob("*.py"):
            try:
                module = import_module(f"metaexpert.cli.plugins.{plugin_file.stem}")
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, CliPlugin) and 
                        attr is not CliPlugin):
                        
                        plugin = attr()
                        self.plugins[plugin.name] = plugin
                        self.logger.info(f"loaded plugin", name=plugin.name, version=plugin.version)
            
            except Exception as e:
                self.logger.error(f"failed to load plugin", file=plugin_file.name, error=str(e))
    
    def register_all(self, app: typer.Typer, middleware: MiddlewareManager) -> None:
        """Register all plugins."""
        for plugin in self.plugins.values():
            plugin.register_commands(app)
            plugin.register_middleware(middleware)
```

**Пример пользовательского плагина:**
```python
# plugins/my_plugin.py
from metaexpert.cli.core.plugins import CliPlugin

class MyCustomPlugin(CliPlugin):
    name = "my-custom"
    version = "1.0.0"
    description = "My custom plugin"
    
    def register_commands(self, app):
        @app.command()
        def custom_command():
            """My custom command."""
            print("Hello from plugin!")
    
    def register_middleware(self, manager):
        # Register custom middleware
        pass
```

#### 1.4. Event system
```python
# src/metaexpert/cli/core/events.py
from dataclasses import dataclass
from typing import Callable, Any
from enum import Enum

class EventType(str, Enum):
    """CLI event types."""
    COMMAND_START = "command:start"
    COMMAND_END = "command:end"
    COMMAND_ERROR = "command:error"
    PROCESS_START = "process:start"
    PROCESS_STOP = "process:stop"
    CONFIG_CHANGED = "config:changed"

@dataclass
class Event:
    """CLI event."""
    type: EventType
    data: dict[str, Any]
    timestamp: float = None

class EventBus:
    """Central event bus for CLI."""
    
    def __init__(self):
        self._subscribers: dict[EventType, list[Callable]] = {}
        self.logger = get_logger(__name__)
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """Subscribe to event."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def publish(self, event: Event) -> None:
        """Publish event."""
        handlers = self._subscribers.get(event.type, [])
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self.logger.error(
                    "event handler failed",
                    event_type=event.type,
                    error=str(e),
                )

# Глобальный Event Bus
_event_bus = EventBus()

# Подписка на события
_event_bus.subscribe(EventType.COMMAND_END, lambda e: print(f"Command completed: {e.data}"))
```

### Итоговая Архитектура (10/10):
```
cli/
├── core/
│   ├── container.py          # 🆕 DI контейнер
│   ├── middleware.py         # 🆕 Middleware система
│   ├── events.py            # 🆕 Event Bus
│   ├── plugins.py           # 🆕 Plugin система
│   ├── config.py
│   ├── exceptions.py
│   └── output.py
├── commands/
│   ├── decorators.py        # 🆕 Декораторы для команд
│   └── ... (остальные)
└── plugins/                 # 🆕 Директория плагинов
    └── __init__.py
```

---

## 2. 💻 ФУНКЦИОНАЛЬНОСТЬ: 7/10 → 10/10

### Что Сейчас (7/10):
✅ Основные команды (new, run, stop, list, logs)  
✅ Работает с процессами  
❌ Недостатки: Нет некоторых команд, ограниченный функционал

### Что Добавить для 10/10:

#### 2.1. Реализовать все основные команды
```python
# src/metaexpert/cli/commands/__init__.py

COMMANDS = [
    "new",      # ✅ создание проекта
    "run",      # ✅ запуск эксперта
    "stop",     # ✅ остановка
    "list",     # ✅ список запущенных
    "logs",     # ✅ просмотр логов
    "status",   # ✅ статус эксперта
    "backtest", # ⚠️ требует доделки
    "config",   # 🆕 управление конфигом
    "init",     # 🆕 инициализация окружения
    "export",   # 🆕 экспорт данных
    "import",   # 🆕 импорт данных
    "doctor",   # 🆕 диагностика окружения
    "version",  # 🆕 информация о версии
    "clean",    # 🆕 очистка кэша/временных файлов
]
```

#### 2.2. Расширенные возможности команды `run`
```python
# src/metaexpert/cli/commands/run.py
def cmd_run(
    project_path: Annotated[...] = None,
    detach: Annotated[bool, typer.Option()] = True,
    script: Annotated[str, typer.Option()] = "main.py",
    env_file: Annotated[Path | None, typer.Option()] = None,  # 🆕
    docker: Annotated[bool, typer.Option()] = False,           # 🆕 Docker поддержка
    notify: Annotated[bool, typer.Option()] = True,            # 🆕 Уведомления
    restart_on_error: Annotated[bool, typer.Option()] = False, # 🆕 Автоперезагрузка
    max_restarts: Annotated[int, typer.Option()] = 5,          # 🆕
) -> None:
    """Run expert with advanced options."""
    output = OutputFormatter()
    
    if docker:
        pid = _run_in_docker(project_path, script)
    else:
        pid = _run_native(project_path, script, env_file)
    
    if notify:
        _send_notification(f"Expert started: PID {pid}")
    
    if restart_on_error:
        _setup_restart_policy(pid, max_restarts)
```

#### 2.3. Новая команда `doctor` для диагностики
```python
# src/metaexpert/cli/commands/doctor.py
def cmd_doctor() -> None:
    """Diagnose MetaExpert CLI environment."""
    output = OutputFormatter()
    
    checks = [
        ("Python версия", _check_python_version),
        ("Зависимости", _check_dependencies),
        ("Конфигурация", _check_configuration),
        ("Дисковое пространство", _check_disk_space),
        ("Разрешения", _check_permissions),
        ("Сетевое подключение", _check_network),
        ("Docker (опционально)", _check_docker),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = "✅ OK" if result else "❌ FAIL"
        except Exception as e:
            results[check_name] = f"⚠️ ERROR: {e}"
    
    output.display_table(
        [{"Check": k, "Status": v} for k, v in results.items()],
        title="Environment Diagnostics",
    )
    
    if all("✅" in v for v in results.values()):
        output.success("All checks passed!")
    else:
        output.warning("Some checks failed. Please review above.")

def _check_python_version() -> bool:
    """Check Python version >= 3.12."""
    import sys
    version = sys.version_info
    return version.major > 3 or (version.major == 3 and version.minor >= 12)

def _check_dependencies() -> bool:
    """Check all required dependencies."""
    required = ["typer", "rich", "pydantic", "psutil", "jinja2"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0

def _check_disk_space() -> bool:
    """Check available disk space."""
    import shutil
    total, used, free = shutil.disk_usage("/")
    return free > 1_000_000_000  # > 1GB

def _check_permissions() -> bool:
    """Check if we can write to required directories."""
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            pass
        return True
    except:
        return False
```

#### 2.4. Новая команда `config` для управления конфигом
```python
# src/metaexpert/cli/commands/config.py
@app.group()
def config():
    """Manage CLI configuration."""
    pass

@config.command()
def show(format: str = "table") -> None:
    """Show current configuration."""
    output = OutputFormatter()
    conf = CLIConfig.load()
    
    data = {
        "default_exchange": conf.default_exchange,
        "default_strategy": conf.default_strategy,
        "pid_dir": str(conf.pid_dir),
        "log_dir": str(conf.log_dir),
        "log_level": conf.log_level,
        "verbose": conf.verbose,
    }
    
    if format == "json":
        output.json_output(data)
    else:
        output.display_key_value_pairs(data)

@config.command()
def set(key: str, value: str) -> None:
    """Set configuration value."""
    output = OutputFormatter()
    conf = CLIConfig.load()
    
    if hasattr(conf, key):
        setattr(conf, key, value)
        conf.save()
        output.success(f"Config updated: {key} = {value}")
    else:
        output.error(f"Unknown config key: {key}")

@config.command()
def reset(confirm: bool = False) -> None:
    """Reset configuration to defaults."""
    output = OutputFormatter()
    
    if not confirm:
        if not typer.confirm("Reset all configuration to defaults?"):
            return
    
    config_file = Path.home() / ".metaexpert" / "config"
    config_file.unlink(missing_ok=True)
    output.success("Configuration reset to defaults")
```

#### 2.5. Расширенный backtest
```python
# src/metaexpert/cli/commands/backtest.py (улучшенная версия)
def cmd_backtest(
    expert_path: Annotated[Path, typer.Argument()],
    start_date: Annotated[str, typer.Option()] = None,
    end_date: Annotated[str, typer.Option()] = None,
    capital: Annotated[float, typer.Option()] = 10000,
    symbol: Annotated[str | None, typer.Option()] = None,
    timeframe: Annotated[str | None, typer.Option()] = None,
    optimize: Annotated[bool, typer.Option()] = False,  # 🆕
    optimize_params: Annotated[str | None, typer.Option()] = None,  # 🆕
    compare: Annotated[bool, typer.Option()] = False,  # 🆕
    report_format: Annotated[str, typer.Option()] = "html",
    output_dir: Annotated[Path, typer.Option()] = Path("./backtest_results"),
) -> None:
    """
    Backtest a strategy with advanced options.
    
    Examples:
        metaexpert backtest main.py
        metaexpert backtest main.py --optimize --optimize-params "period:10,20,30"
        metaexpert backtest main.py --compare --report-format html
    """
    output = OutputFormatter()
    
    if optimize:
        _run_optimization(expert_path, optimize_params)
    
    if compare:
        _run_comparison(expert_path)
    
    _run_backtest(
        expert_path,
        start_date,
        end_date,
        capital,
        symbol,
        timeframe,
        output_dir,
        report_format,
    )
```

### Итоговый функционал (10/10):
```
Основные команды (100%):
├── new          ✅ Создание проекта
├── run          ✅ Запуск (с Docker)
├── stop         ✅ Остановка
├── list         ✅ Список процессов
├── logs         ✅ Просмотр логов
├── status       ✅ Статус
├── config       ✅ Управление конфигом
├── backtest     ✅ Бэктестинг (с оптимизацией)
├── export       ✅ Экспорт данных
├── import       ✅ Импорт данных
├── doctor       ✅ Диагностика
├── clean        ✅ Очистка
├── version      ✅ Информация о версии
└── init         ✅ Инициализация
```

---

## 3. 📚 ДОКУМЕНТАЦИЯ: 8/10 → 10/10

### Что Сейчас (8/10):
✅ Хорошие комментарии в коде  
✅ Примеры использования  
❌ Недостатки: Нет интерактивного руководства, нет видео, ограниченная документация по расширению

### Что Добавить для 10/10:

#### 3.1. Интерактивная справка
```python
# src/metaexpert/cli/commands/help.py
def cmd_help(topic: str | None = None) -> None:
    """Interactive help system."""
    output = OutputFormatter()
    
    help_topics = {
        "getting-started": _help_getting_started,
        "commands": _help_commands,
        "strategies": _help_strategies,
        "troubleshooting": _help_troubleshooting,
        "examples": _help_examples,
        "extensions": _help_extensions,
    }
    
    if topic is None:
        output.panel("""
Available help topics:
  • getting-started    - Quick start guide
  • commands          - Available commands
  • strategies        - Strategy development
  • troubleshooting   - Common issues
  • examples          - Code examples
  • extensions        - Creating plugins

Usage: metaexpert help <topic>
        """, title="MetaExpert Help")
        return
    
    handler = help_topics.get(topic)
    if handler:
        handler(output)
    else:
        output.error(f"Unknown help topic: {topic}")

def _help_getting_started(output):
    """Getting started guide."""
    guide = """
GETTING STARTED WITH METAEXPERT CLI
====================================

1. Initialize Environment:
   $ metaexpert init
   
2. Create Your First Project:
   $ metaexpert new my-first-bot --exchange binance
   
3. Configure API Keys:
   $ cd my-first-bot
   $ cp .env.example .env
   $ # Edit .env with your API credentials
   
4. Start Trading (Paper Mode):
   $ metaexpert run
   
5. Check Logs:
   $ metaexpert logs my-first-bot
   
6. Stop Expert:
   $ metaexpert stop my-first-bot

For more: metaexpert help commands
    """
    output.panel(guide, title="Getting Started", border_style="green")
```

#### 3.2. Встроенная документация
```python
# src/metaexpert/cli/docs/

docs/
├── CLI_GUIDE.md              # Полное руководство
├── COMMAND_REFERENCE.md      # Справочник команд
├── EXTENDING_CLI.md          # Расширение функциональности
├── TROUBLESHOOTING.md        # Решение проблем
├── EXAMPLES/
│   ├── basic_strategy.md
│   ├── advanced_strategy.md
│   ├── backtesting.md
│   └── optimization.md
└── API/
    ├── ProcessManager.md
    ├── TemplateGenerator.md
    ├── OutputFormatter.md
    └── CLIConfig.md
```

#### 3.3. Генерация документации из кода
```python
# src/metaexpert/cli/commands/docs.py
def cmd_docs(output_dir: Path = Path("./docs")) -> None:
    """Generate documentation from docstrings."""
    
    generator = DocumentationGenerator()
    
    # Генерируем документацию для всех команд
    commands = _get_all_commands()
    for cmd in commands:
        generator.generate_command_doc(cmd, output_dir)
    
    # Генерируем API документацию
    modules = [
        "metaexpert.cli.process.manager",
        "metaexpert.cli.templates.generator",
        "metaexpert.cli.core.output",
    ]
    for module_name in modules:
        generator.generate_module_doc(module_name, output_dir)
    
    print(f"Documentation generated in {output_dir}")
```

#### 3.4. Markdown файлы с примерами
```markdown
# CLI Architecture

## Layers

### 1. Commands Layer
Обработка пользовательского ввода

### 2. Core Layer
Основная функциональность

### 3. Utils Layer
Вспомогательные функции

## Extending CLI

### Adding New Command

1. Create `src/metaexpert/cli/commands/my_command.py`
2. Define function with Typer decorators
3. Register in `app.py`
4. Add tests in `tests/cli/test_my_command.py`
5. Update documentation

### Example

\`\`\`python
from metaexpert.cli.commands import register_command

@register_command("my-command", "My custom command")
def cmd_my_command(
    arg: Annotated[str, typer.Argument()],
    opt: Annotated[str, typer.Option()] = "default",
) -> None:
    \"\"\"Description of my command.\"\"\"
    print(f"Arg: {arg}, Option: {opt}")
\`\`\`
```

### Итоговая документация (10/10):
```
docs/
├── README.md                      # Главная страница
├── INSTALLATION.md                # Установка
├── QUICK_START.md                 # Быстрый старт
├── CLI_GUIDE.md                   # Полное руководство
├── COMMAND_REFERENCE.md           # Справочник команд
├── ARCHITECTURE.md                # Архитектура
├── EXTENDING_CLI.md               # Расширение
├── TROUBLESHOOTING.md             # Проблемы
├── API_REFERENCE.md               # API документация
├── EXAMPLES/                      # Примеры
│   ├── 01_getting_started.py
│   ├── 02_basic_strategy.py
│   ├── 03_advanced_strategy.py
│   ├── 04_backtesting.py
│   └── 05_optimization.py
├── TUTORIALS/                     # Видеоуроки (README)
│   ├── 01_installation.md
│   ├── 02_first_project.md
│   └── 03_live_trading.md
└── CHANGELOG.md                   # История изменений
```

---

## 4. ⚠️ ОБРАБОТКА ОШИБОК: 6.5/10 → 10/10

### Что Сейчас (6.5/10):
✅ Пользовательские исключения  
✅ Базовая обработка  
❌ Недостатки: Нет восстановления после ошибок, ограниченный контекст ошибок

### Что Добавить для 10/10:

#### 4.1. Расширенная система обработки ошибок
```python
# src/metaexpert/cli/core/error_handler.py
from typing import Callable, Any
from dataclasses import dataclass
from enum import Enum

class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ErrorContext:
    """Detailed error context."""
    exception: Exception
    command: str
    args: dict[str, Any]
    timestamp: float
    severity: ErrorSeverity
    traceback: str
    suggestions: list[str] = None
    recovery_actions: list[Callable] = None

class ErrorHandler:
    """Centralized error handling."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.handlers: dict[type, Callable] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """Register handlers for common exceptions."""
        self.handlers[ValidationError] = self._handle_validation_error
        self.handlers[ProcessError] = self._handle_process_error
        self.handlers[TemplateError] = self._handle_template_error
        self.handlers[FileNotFoundError] = self._handle_file_not_found
        self.handlers[PermissionError] = self._handle_permission_error
    
    def handle(
        self,
        exception: Exception,
        command: str,
        args: dict[str, Any],
    ) -> ErrorContext:
        """Handle exception with context."""
        
        ctx = ErrorContext(
            exception=exception,
            command=command,
            args=args,
            timestamp=time.time(),
            severity=self._determine_severity(exception),
            traceback=traceback.format_exc(),
            suggestions=[],
            recovery_actions=[],
        )
        
        # Найти обработчик
        handler = self.handlers.get(type(exception))
        if handler:
            handler(ctx)
        else:
            self._handle_generic_error(ctx)
        
        # Логировать ошибку
        self._log_error(ctx)
        
        return ctx
    
    def _handle_validation_error(self, ctx: ErrorContext) -> None:
        """Handle validation errors."""
        ctx.suggestions = [
            "Check your input parameters",
            "Use 'metaexpert help' for syntax",
            "Validate using 'metaexpert doctor'",
        ]
        ctx.severity = ErrorSeverity.WARNING
    
    def _handle_process_error(self, ctx: ErrorContext) -> None:
        """Handle process errors."""
        ctx.suggestions = [
            "Check if process is already running",
            "Verify project directory exists",
            "Check system resources",
        ]
        ctx.recovery_actions = [
            self._cleanup_stale_processes,
            self._free_system_resources,
        ]
    
    def _handle_template_error(self, ctx: ErrorContext) -> None:
        """Handle template errors."""
        ctx.suggestions = [
            "Reinstall MetaExpert package",
            "Check template files exist",
            "Verify Jinja2 is installed",
        ]
        ctx.recovery_actions = [self._reinstall_templates]
    
    def _handle_file_not_found(self, ctx: ErrorContext) -> None:
        """Handle file not found errors."""
        ctx.suggestions = [
            "Check file path exists",
            "Verify file permissions",
            "Use absolute path if needed",
        ]
    
    def _handle_permission_error(self, ctx: ErrorContext) -> None:
        """Handle permission errors."""
        ctx.suggestions = [
            "Check directory permissions",
            "Try running with sudo (not recommended)",
            "Change working directory",
        ]
    
    def _handle_generic_error(self, ctx: ErrorContext) -> None:
        """Handle generic errors."""
        ctx.suggestions = [
            f"Report issue at https://github.com/teratron/metaexpert/issues",
            "Include error message and traceback",
            "Run with --debug flag for more info",
        ]
    
    def _determine_severity(self, exception: Exception) -> ErrorSeverity:
        """Determine error severity."""
        if isinstance(exception, (ValidationError, FileNotFoundError)):
            return ErrorSeverity.WARNING
        elif isinstance(exception, (ProcessError, PermissionError)):
            return ErrorSeverity.ERROR
        else:
            return ErrorSeverity.CRITICAL
    
    def _log_error(self, ctx: ErrorContext) -> None:
        """Log error with context."""
        self.logger.error(
            f"{ctx.severity.value}: {ctx.command}",
            error=str(ctx.exception),
            exc_info=ctx.traceback,
            args=ctx.args,
        )
    
    def _cleanup_stale_processes(self) -> bool:
        """Cleanup stale processes."""
        try:
            manager = ProcessManager()
            manager.cleanup_stopped_processes()
            return True
        except:
            return False
    
    def _free_system_resources(self) -> bool:
        """Try to free system resources."""
        try:
            import gc
            gc.collect()
            return True
        except:
            return False
    
    def _reinstall_templates(self) -> bool:
        """Attempt to reinstall templates."""
        try:
            # Logic to reinstall
            return True
        except:
            return False

# Глобальный обработчик ошибок
_error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Get error handler instance."""
    return _error_handler
```

#### 4.2. Display ошибок с рекомендациями
```python
# src/metaexpert/cli/core/error_display.py
class ErrorDisplay:
    """Display errors with helpful suggestions."""
    
    def __init__(self, output: OutputFormatter):
        self.output = output
    
    def show_error(self, ctx: ErrorContext) -> None:
        """Display error with all context."""
        
        # 1. Основная ошибка
        self.output.error(
            f"{ctx.command}: {str(ctx.exception)}",
            title=f"{ctx.severity.value.upper()}"
        )
        
        # 2. Рекомендации
        if ctx.suggestions:
            suggestions_text = "\n".join(
                f"  • {s}" for s in ctx.suggestions
            )
            self.output.panel(
                suggestions_text,
                title="💡 Suggestions",
                border_style="yellow"
            )
        
        # 3. Действия восстановления
        if ctx.recovery_actions:
            recovery_text = "\n".join(
                f"  • {action.__name__}"
                for action in ctx.recovery_actions
            )
            
            if self.output.console.is_interactive:
                if typer.confirm("Try recovery actions?"):
                    for action in ctx.recovery_actions:
                        try:
                            if action():
                                self.output.success(f"{action.__name__} completed")
                        except:
                            self.output.warning(f"{action.__name__} failed")
        
        # 4. Дополнительная информация
        if ctx.severity == ErrorSeverity.CRITICAL:
            self.output.panel(
                f"Traceback:\n{ctx.traceback}",
                title="📋 Technical Details",
                border_style="red"
            )
            
            self.output.panel(
                "Run with --debug flag for more information\n"
                "Report at: https://github.com/teratron/metaexpert/issues",
                title="🔗 Resources",
                border_style="blue"
            )

# Использование в команде
def cmd_example() -> None:
    try:
        # ... код команды
        pass
    except Exception as e:
        handler = get_error_handler()
        ctx = handler.handle(e, "example", {})
        
        display = ErrorDisplay(OutputFormatter())
        display.show_error(ctx)
        
        raise typer.Exit(code=1)
```

#### 4.3. Error recovery strategies
```python
# src/metaexpert/cli/core/recovery.py
class RecoveryStrategy:
    """Strategy for error recovery."""
    
    @staticmethod
    def retry_with_backoff(
        func: Callable,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        """Retry function with exponential backoff."""
        
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = (backoff_factor ** attempt)
                    time.sleep(wait_time)
                    continue
        
        raise last_exception
    
    @staticmethod
    def fallback(
        primary: Callable,
        fallback: Callable,
        exceptions: tuple = (Exception,),
    ):
        """Try primary, fallback to secondary."""
        
        try:
            return primary()
        except exceptions:
            return fallback()
    
    @staticmethod
    def timeout(
        func: Callable,
        timeout_seconds: float = 10.0,
    ):
        """Execute with timeout."""
        
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout_seconds}s")
        
        # Set signal handler
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout_seconds))
        
        try:
            result = func()
            signal.alarm(0)  # Cancel alarm
            return result
        except TimeoutError:
            raise

# Использование
def cmd_risky_operation() -> None:
    try:
        # Retry с backoff
        result = RecoveryStrategy.retry_with_backoff(
            lambda: perform_operation(),
            max_retries=3,
        )
    except Exception as e:
        output.error(f"Operation failed: {e}")
```

#### 4.4. Error logging с контекстом
```python
# Обновление логирования ошибок
class ErrorLogger:
    """Enhanced error logging."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def log_with_context(
        self,
        level: str,
        message: str,
        **context
    ) -> None:
        """Log with context information."""
        
        context_info = {
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
            "platform": sys.platform,
            **context,
        }
        
        getattr(self.logger, level)(message, **context_info)

# Использование
error_logger = ErrorLogger()
error_logger.log_with_context(
    "error",
    "Process failed",
    process_name="my-bot",
    pid=12345,
    exit_code=1,
)
```

### Итоговая обработка ошибок (10/10):
```
Error Handling:
├── ✅ Structured error context
├── ✅ Helpful suggestions
├── ✅ Recovery strategies
├── ✅ Detailed logging
├── ✅ User-friendly messages
├── ✅ Automatic recovery attempts
├── ✅ Error analytics
└── ✅ Issue reporting help
```

---

## 5. 🧪 ТЕСТИРУЕМОСТЬ: 7.5/10 → 10/10

### Что Сейчас (7.5/10):
✅ Примеры тестов предоставлены  
✅ CliRunner использование  
❌ Недостатки: Нет мокирования, недостаточное покрытие, нет test fixtures

### Что Добавить для 10/10:

#### 5.1. Полный набор fixtures
```python
# tests/cli/conftest.py
import pytest
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock

@pytest.fixture
def cli_runner() -> CliRunner:
    """CLI test runner."""
    return CliRunner()

@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create temporary project structure."""
    project = tmp_path / "test-bot"
    project.mkdir()
    (project / "main.py").write_text("print('test')")
    (project / ".env").write_text("API_KEY=test\n")
    return project

@pytest.fixture
def mock_process_manager():
    """Mock ProcessManager."""
    with patch("metaexpert.cli.process.manager.ProcessManager") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_cli_config():
    """Mock CLIConfig."""
    with patch("metaexpert.cli.core.config.CLIConfig") as mock:
        config = MagicMock()
        config.pid_dir = Path("/tmp/pids")
        config.log_dir = Path("/tmp/logs")
        config.default_exchange = "binance"
        mock.load.return_value = config
        yield mock

@pytest.fixture
def isolated_environment(monkeypatch, tmp_path):
    """Isolated test environment."""
    home = tmp_path / "home"
    home.mkdir()
    
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("METAEXPERT_CLI_PID_DIR", str(tmp_path / "pids"))
    monkeypatch.setenv("METAEXPERT_CLI_LOG_DIR", str(tmp_path / "logs"))
    
    return {
        "home": home,
        "tmp_path": tmp_path,
    }

@pytest.fixture
def capture_output(capsys):
    """Capture output for testing."""
    class OutputCapture:
        def __init__(self, capsys):
            self.capsys = capsys
        
        def get_stdout(self):
            return self.capsys.readouterr().out
        
        def get_stderr(self):
            return self.capsys.readouterr().err
        
        def contains(self, text: str, stream: str = "out") -> bool:
            output = self.get_stdout() if stream == "out" else self.get_stderr()
            return text in output
    
    return OutputCapture(capsys)

# CLI-specific fixtures
@pytest.fixture
def app():
    """Get CLI app."""
    from metaexpert.cli.app import app
    return app

@pytest.fixture
def db_session():
    """Database session for tests."""
    # Если используется БД
    pass
```

#### 5.2. Параметризованные тесты
```python
# tests/cli/commands/test_new_command.py
import pytest

class TestNewCommand:
    """Tests for 'new' command."""
    
    @pytest.mark.parametrize("exchange", ["binance", "bybit", "okx"])
    @pytest.mark.parametrize("strategy", ["ema", "rsi", "macd"])
    def test_new_with_exchanges_and_strategies(
        self,
        cli_runner,
        tmp_path,
        exchange,
        strategy,
    ):
        """Test creating projects with different exchanges and strategies."""
        result = cli_runner.invoke(
            app,
            ["new", "test-bot", "--exchange", exchange, "--strategy", strategy, "--output-dir", str(tmp_path)],
        )
        
        assert result.exit_code == 0
        assert (tmp_path / "test-bot").exists()
        assert exchange in (tmp_path / "test-bot" / "main.py").read_text()
    
    @pytest.mark.parametrize("invalid_name", ["123-bot", "-bot", "bot-", "_bot"])
    def test_invalid_project_names(self, cli_runner, tmp_path, invalid_name):
        """Test that invalid names are rejected."""
        result = cli_runner.invoke(
            app,
            ["new", invalid_name],
        )
        
        assert result.exit_code != 0
        assert "Invalid" in result.stdout or "Error" in result.stdout
    
    @pytest.mark.parametrize("option,value", [
        ("--market-type", "spot"),
        ("--market-type", "futures"),
        ("--market-type", "options"),
    ])
    def test_market_types(self, cli_runner, tmp_path, option, value):
        """Test different market types."""
        result = cli_runner.invoke(
            app,
            ["new", "test-bot", option, value],
        )
        
        assert result.exit_code == 0
        assert value in (tmp_path / "test-bot" / "main.py").read_text()
```

#### 5.3. Интеграционные тесты
```python
# tests/cli/test_integration_workflows.py
class TestIntegrationWorkflows:
    """Integration tests for complete workflows."""
    
    def test_complete_workflow_new_run_stop(
        self,
        cli_runner,
        tmp_path,
        mock_process_manager,
    ):
        """Test: create -> run -> stop workflow."""
        
        # 1. Create project
        result = cli_runner.invoke(
            app,
            ["new", "workflow-test", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0
        project_path = tmp_path / "workflow-test"
        assert project_path.exists()
        
        # 2. Run project
        mock_process_manager.start.return_value = 12345
        result = cli_runner.invoke(
            app,
            ["run", str(project_path)],
        )
        assert result.exit_code == 0
        mock_process_manager.start.assert_called()
        
        # 3. List running
        mock_process_manager.list_running.return_value = [
            ProcessInfo(pid=12345, name="workflow-test", status="running")
        ]
        result = cli_runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "workflow-test" in result.stdout
        
        # 4. Stop project
        result = cli_runner.invoke(
            app,
            ["stop", "workflow-test"],
        )
        assert result.exit_code == 0
        mock_process_manager.stop.assert_called()
    
    def test_error_recovery_workflow(
        self,
        cli_runner,
        tmp_path,
        mock_process_manager,
    ):
        """Test: error handling and recovery."""
        
        # First attempt fails
        mock_process_manager.start.side_effect = ProcessError("Failed")
        
        result = cli_runner.invoke(
            app,
            ["run", str(tmp_path / "test")],
        )
        assert result.exit_code != 0
        
        # Suggestions are shown
        assert "Suggestions" in result.stdout or "suggestion" in result.stdout.lower()
```

#### 5.4. Performance tests
```python
# tests/cli/test_performance.py
import pytest
import time

class TestPerformance:
    """Performance tests."""
    
    @pytest.mark.benchmark
    def test_command_startup_time(self, cli_runner, benchmark):
        """Test CLI startup performance."""
        
        def run_command():
            result = cli_runner.invoke(app, ["--help"])
            assert result.exit_code == 0
        
        result = benchmark(run_command)
        assert result < 0.5  # < 500ms
    
    @pytest.mark.benchmark
    def test_project_creation_time(self, cli_runner, tmp_path, benchmark):
        """Test project creation performance."""
        
        def create_project():
            result = cli_runner.invoke(
                app,
                ["new", "perf-test", "--output-dir", str(tmp_path)],
            )
            assert result.exit_code == 0
        
        result = benchmark(create_project)
        assert result < 2.0  # < 2 seconds
    
    @pytest.mark.benchmark
    def test_process_list_time(self, cli_runner, mock_process_manager, benchmark):
        """Test listing processes performance."""
        
        # Create many processes
        processes = [
            ProcessInfo(pid=i, name=f"bot-{i}", status="running")
            for i in range(100)
        ]
        mock_process_manager.list_running.return_value = processes
        
        def list_processes():
            result = cli_runner.invoke(app, ["list"])
            assert result.exit_code == 0
        
        result = benchmark(list_processes)
        assert result < 1.0  # < 1 second
```

#### 5.5. Coverage configuration
```python
# pyproject.toml
[tool.coverage.run]
source = ["src/metaexpert/cli"]
omit = [
    "*/tests/*",
    "*/test_*.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
precision = 2
skip_covered = false

[tool.coverage.html]
directory = "htmlcov"

# pytest configuration
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=src/metaexpert/cli",
    "--cov-report=html",
    "--cov-report=term-missing:skip-covered",
    "--cov-branch",
]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
markers = [
    "integration: Integration tests",
    "benchmark: Performance tests",
    "slow: Slow running tests",
]
```

### Итоговая тестируемость (10/10):
```
Testing:
├── ✅ Unit tests (>95% coverage)
├── ✅ Integration tests (complete workflows)
├── ✅ Performance tests (benchmarks)
├── ✅ Parametrized tests (multiple scenarios)
├── ✅ Fixtures (reusable test components)
├── ✅ Mocking strategies
├── ✅ Error scenario tests
└── ✅ CI/CD integration
```

---

## 📊 Итоговая Таблица: От 7.5 к 10/10

| Категория | Текущий Уровень | К-во Изменений | Сложность | Время |
|-----------|-----------------|----------------|-----------|-------|
| **Архитектура** | 8/10 | 4 крупных | Средняя | 2-3 дня |
| **Функциональность** | 7/10 | +7 команд | Средняя | 3-4 дня |
| **Документация** | 8/10 | Полное переписывание | Низкая | 2-3 дня |
| **Обработка ошибок** | 6.5/10 | Переделка системы | Средняя | 2 дня |
| **Тестируемость** | 7.5/10 | Расширение набора | Низкая | 2 дня |

**Итого:** ~12-15 дней работы на одного разработчика

---

## 🎯 Приоритезованный Путь к 10/10

### Фаза 1: Критичные (Дни 1-3)
1. ✅ Исправить импорты
2. ✅ Добавить недостающие методы в OutputFormatter
3. ✅ Реализовать полноценный ProcessManager
4. ✅ Валидация шаблонов

### Фаза 2: Архитектура (Дни 4-6)
1. ✅ DI контейнер
2. ✅ Middleware система
3. ✅ Event Bus
4. ✅ Plugin система

### Фаза 3: Функциональность (Дни 7-10)
1. ✅ Команда `init`
2. ✅ Команда `config`
3. ✅ Команда `doctor`
4. ✅ Улучшенный `backtest`

### Фаза 4: Документация (Дни 11-12)
1. ✅ Встроенная справка
2. ✅ Примеры кода
3. ✅ API документация

### Фаза 5: Полирование (Дни 13-15)
1. ✅ Расширенная обработка ошибок
2. ✅ Полное тестовое покрытие
3. ✅ Performance тесты

---

## ✅ Финальный Чек-лист для 10/10

### Архитектура ✓
- [ ] DI контейнер реализован
- [ ] Middleware система работает
- [ ] Event Bus интегрирован
- [ ] Plugin система функциональна

### Функциональность ✓
- [ ] Все 14 команд реализованы
- [ ] Docker поддержка
- [ ] Расширенный backtest
- [ ] Optimization работает

### Документация ✓
- [ ] Встроенная справка
- [ ] 50+ примеров кода
- [ ] API документация 100%
- [ ] Видеоуроки (ссылки)

### Обработка ошибок ✓
- [ ] Контекстная информация об ошибках
- [ ] 10+ типов обработчиков
- [ ] Recovery strategies
- [ ] User-friendly messages

### Тесты ✓
- [ ] Unit tests >95% coverage
- [ ] Integration tests
- [ ] Performance benchmarks
- [ ] Параметризованные тесты

---

## 🚀 Заключение

Путь от **7.5/10 к 10/10** требует:

1. **Архитектурных улучшений** - DI, middleware, plugins
2. **Расширения функциональности** - +7 новых команд
3. **Полной документации** - примеры, справка, уроки
4. **Надежной обработки ошибок** - контекст, восстановление, suggestions
5. **Комплексного тестирования** - >95% покрытие

**Результат:** Production-ready CLI инструмент уровня enterprise с отличным UX и полной документацией.

Начните с **Фазы 1** (критичные исправления), затем переходите к остальным. Каждая фаза добавляет ~0.5 баллов к оценке! 🎉