# 🔍 Анализ и Рекомендации по Улучшению MetaExpert CLI

## 1. 🔴 Критические Проблемы

### 1.1. Импорты в `validators.py`

**Проблема:**

```python
from src.metaexpert.cli.core.exceptions import ValidationError  # ❌ НЕПРАВИЛЬНО
```

**Решение:**

```python
from metaexpert.cli.core.exceptions import ValidationError  # ✅ ПРАВИЛЬНО
```

**Почему:** При установке пакета, путь `src/` не существует. Используйте относительные импорты.

---

### 1.2. Отсутствие ProcessInfo.display_table в `list.py`

**Проблема:**

```python
output.display_table(data, title="Running Experts", columns=[...])
# ❌ Метод display_table не определен в OutputFormatter
```

**Решение:**

```python
output.custom_table(data, columns=["Name", "PID", "Status", "CPU %", "Memory (MB)", "Started"], title="Running Experts")
```

---

### 1.3. OutputFormatter требует методов

**Проблема:** В `list.py` используются методы:

- `display_table()` → не существует
- `display_json()` → не существует  
- `display_yaml()` → не существует

**Решение:** Добавьте методы в `core/output.py`:

```python
def display_table(self, data: list[dict], columns: list[str], title: str | None = None) -> None:
    """Display data as table."""
    self.custom_table(data, columns=columns)

def display_json(self, data: Any) -> None:
    """Display data as JSON."""
    self.json_output(data)

def display_yaml(self, data: Any) -> None:
    """Display data as YAML."""
    import yaml
    from rich.syntax import Syntax
    syntax = Syntax(yaml.dump(data), "yaml", theme="monokai")
    self.console.print(syntax)
```

---

### 1.4. ProcessManager не использует Pydantic нормально

**Проблема:**

```python
# ProcessInfo использует psutil, но не импортирует его
info.cpu_percent  # ❌ ProcessInfo не имеет это поле
info.memory_mb    # ❌ ProcessInfo не имеет это поле
```

**Решение:** Обновите ProcessInfo:

```python
class ProcessInfo(BaseModel):
    """Информация о процессе."""
    pid: int
    command: str
    start_time: float
    status: str
    working_directory: str
    environment: dict[str, str] = Field(default_factory=dict)
    cpu_percent: float = Field(default=0.0)  # ✅ Добавить
    memory_mb: float = Field(default=0.0)    # ✅ Добавить
```

---

### 1.5. Отсутствует TemplateGenerator в app.py

**Проблема:** В `new.py` импортируется TemplateGenerator, но нет валидации шаблонов.

**Решение:** Обновите `new.py`:

```python
def cmd_new(...):
    # Проверка существования шаблонов
    generator = TemplateGenerator()
    templates = generator.list_available_templates()
    if not templates:
        output.error("No templates found. Please reinstall MetaExpert.")
        raise typer.Exit(code=1)
```

---

## 2. 🟠 Важные Проблемы

### 2.1. ProcessManager не отслеживает процессы правильно

**Проблема:** Нет метода для получения информации о конкретном процессе с CPU/Memory:

```python
# Текущая реализация только хранит базовую информацию
# но commands/list.py ожидает cpu_percent и memory_mb
```

**Решение:**

```python
import psutil

def get_info(self, project_path: Path) -> ProcessInfo | None:
    """Get detailed process information including CPU and memory."""
    pid_file = self._get_pid_file(project_path)
    if not pid_file.exists():
        return None
    
    pid = self._read_pid(pid_file)
    if pid not in self.processes:
        return None
    
    try:
        process = psutil.Process(pid)
        self.processes[pid].cpu_percent = process.cpu_percent(interval=1)
        self.processes[pid].memory_mb = process.memory_info().rss / 1024 / 1024
        return self.processes[pid]
    except psutil.NoSuchProcess:
        self._cleanup_process(pid)
        return None
```

---

### 2.2. Недостаточная обработка ошибок в `new.py`

**Проблема:**

```python
validate_project_name(project_name)
# ❌ Валидация выбрасывает ValueError, но catch ValidationError
```

**Решение:**

```python
try:
    validate_project_name(project_name)
except ValidationError as e:
    output.error(f"Invalid project name: {e}")
    raise typer.Exit(code=1)
```

---

### 2.3. Шаблоны используют переменные, которых нет в контексте

**Проблема в `pyproject.toml.j2`:**

```jinja2
version = "{{ version }}"
author_name = "{{ author_name }}"
author_email = "{{ author_email }}"
additional_dependencies = "{{ additional_dependencies }}"
```

**Решение:** Обновите контекст в `new.py`:

```python
context = {
    "exchange": exchange.lower(),
    "strategy": strategy.lower(),
    "market_type": market_type.lower(),
    "contract_type": "linear",
    "margin_mode": "isolated",
    "position_mode": "hedge",
    "requires_passphrase": exchange.lower() in ["okx", "kucoin"],
    "leverage": 10,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0,
    "size_value": 1.5,
    # ✅ Добавить недостающие переменные
    "version": "0.1.0",
    "author_name": os.getenv("GIT_AUTHOR_NAME", "Unknown"),
    "author_email": os.getenv("GIT_AUTHOR_EMAIL", "user@example.com"),
    "description": f"{strategy.upper()} strategy on {exchange.upper()}",
    "additional_dependencies": [],
}
```

---

### 2.4. TemplateGenerator не имеет обработки ошибок шаблонов

**Проблема:** Если Jinja2 выбросит исключение, нет информативного сообщения об ошибке.

**Решение:** Уже в коде есть обработка (хорошо!), но улучшьте логирование:

```python
except UndefinedError as e:
    self.logger.error(
        "undefined variable in template",
        template=str(template_path),
        error=str(e),
        variable=str(e).split("'")[1] if "'" in str(e) else "unknown",  # ✅ Улучшено
    )
```

---

### 2.5. `__init__.py` экспортирует не все необходимое

**Проблема:**

```python
__all__ = [...]
# ❌ Отсутствуют OutputFormatter и другие полезные классы
```

**Решение:**

```python
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.utils.validators import (
    validate_project_name,
    validate_exchange_name,
)

__all__ = [
    "app",
    "main",
    "CLIConfig",
    "OutputFormatter",
    "ProcessManager",
    "TemplateGenerator",
    "ValidationError",
    "ProcessError",
    "TemplateError",
    "ProjectError",
    "validate_project_name",
    "validate_exchange_name",
]
```

---

## 3. 🟡 Рекомендации по Улучшению

### 3.1. Добавить кэширование в ProcessManager

```python
from functools import lru_cache
from datetime import datetime, timedelta

class ProcessManager:
    def __init__(self, ...):
        self._info_cache: dict[int, tuple[ProcessInfo, datetime]] = {}
        self._cache_ttl = timedelta(seconds=5)
    
    def get_info(self, project_path: Path, use_cache: bool = True) -> ProcessInfo | None:
        """Get process info with optional caching."""
        pid = self._get_pid(project_path)
        
        if use_cache and pid in self._info_cache:
            info, timestamp = self._info_cache[pid]
            if datetime.now() - timestamp < self._cache_ttl:
                return info
        
        # Fetch fresh info
        info = self._get_info_fresh(pid)
        if info:
            self._info_cache[pid] = (info, datetime.now())
        
        return info
```

**Почему:** Избегает многократных вызовов psutil для одного процесса.

---

### 3.2. Добавить поддержку профилей в CLIConfig

```python
class CLIConfig(BaseSettings):
    profile: str = Field(default="default")
    
    @classmethod
    def load(cls, profile: str | None = None) -> "CLIConfig":
        """Load config for specific profile."""
        profile_name = profile or os.getenv("METAEXPERT_PROFILE", "default")
        config_file = Path.home() / ".metaexpert" / f"{profile_name}.env"
        
        if config_file.exists():
            return cls(_env_file=config_file)
        return cls()
```

**Почему:** Позволяет разные конфигурации для разных сценариев (dev, prod, testing).

---

### 3.3. Добавить команду `metaexpert init`

```python
# src/metaexpert/cli/commands/init.py
def cmd_init(
    interactive: Annotated[
        bool,
        typer.Option("--interactive", "-i", help="Interactive setup"),
    ] = True,
) -> None:
    """Initialize MetaExpert CLI environment."""
    output = OutputFormatter()
    
    config = CLIConfig.load()
    
    if interactive:
        # Интерактивная настройка
        exchange = typer.prompt(
            "Default exchange",
            default=config.default_exchange,
        )
        # ... остальные параметры
    
    config.save()
    output.success("CLI initialized successfully")
```

---

### 3.4. Улучшить логирование в ProcessManager

```python
from metaexpert.logger import log_context

def start_process(...):
    with log_context(
        phase="startup",
        command=" ".join(command),
        working_dir=str(cwd),
    ):
        self.logger.info("starting process")
        try:
            process = subprocess.Popen(...)
            self.logger.info("process started", pid=process.pid)
        except Exception as e:
            self.logger.error("failed to start", error=str(e), exc_info=True)
            raise
```

---

### 3.5. Добавить валидацию зависимостей

```python
# src/metaexpert/cli/core/dependencies.py
def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    required = {
        "typer": ">=0.12.0",
        "rich": ">=13.0.0",
        "pydantic": ">=2.0.0",
        "psutil": ">=5.9.0",
        "jinja2": ">=3.1.0",
    }
    
    missing = []
    for package, version_spec in required.items():
        try:
            import importlib
            mod = importlib.import_module(package)
            # Проверка версии
        except ImportError:
            missing.append(f"{package}{version_spec}")
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    return True

# В app.py
@app.callback()
def main(...):
    if not check_dependencies():
        raise typer.Exit(code=1)
```

---

### 3.6. Добавить поддержку конфигурационных файлов

```python
# src/metaexpert/cli/config_file.py
from configparser import ConfigParser
from pathlib import Path

class ProjectConfig:
    """Configuration for specific project."""
    
    def __init__(self, project_path: Path):
        self.config_file = project_path / ".metaexpert.ini"
        self.config = ConfigParser()
        if self.config_file.exists():
            self.config.read(self.config_file)
    
    def get(self, section: str, key: str, default: str | None = None) -> str | None:
        """Get config value."""
        try:
            return self.config.get(section, key)
        except:
            return default
    
    def set(self, section: str, key: str, value: str) -> None:
        """Set config value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save()
    
    def save(self) -> None:
        """Save config to file."""
        with open(self.config_file, "w") as f:
            self.config.write(f)
```

---

### 3.7. Улучшить обработку сигналов

```python
# src/metaexpert/cli/process/signal_handler.py
import signal
from typing import Callable

class SignalHandler:
    """Handle system signals gracefully."""
    
    def __init__(self):
        self.handlers: dict[int, list[Callable]] = {}
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Setup signal handlers."""
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
    
    def _handle_signal(self, signum: int, frame) -> None:
        """Handle received signal."""
        logger = get_logger(__name__)
        logger.warning("signal received", signal=signal.Signals(signum).name)
        
        # Execute registered handlers
        for handler in self.handlers.get(signum, []):
            handler()
    
    def register(self, signum: int, handler: Callable) -> None:
        """Register handler for signal."""
        if signum not in self.handlers:
            self.handlers[signum] = []
        self.handlers[signum].append(handler)
```

---

## 4. 🟢 Что Хорошо

### ✅ Положительные моменты

1. **Структура проекта** - Хорошо организована с ясным разделением ответственности
2. **Использование Pydantic** - Валидация конфигурации на уровне типов
3. **Jinja2 шаблоны** - Гибкая система создания проектов
4. **Rich интеграция** - Красивый вывод в терминал
5. **Логирование** - Структурированное логирование везде
6. **Исключения** - Собственные исключения для разных сценариев
7. **Документация** - Подробные комментарии и примеры
8. **Тесты** - Примеры тестов в структуре

---

## 5. 📋 Чек-лист Исправлений

### Приоритет 1 (Критичные)

- [ ] Исправить импорты `src/metaexpert` → `metaexpert`
- [ ] Реализовать `display_table()`, `display_json()`, `display_yaml()`
- [ ] Добавить `cpu_percent` и `memory_mb` в ProcessInfo
- [ ] Обновить контекст шаблонов со всеми переменными
- [ ] Реализовать полноценный `get_info()` с psutil

### Приоритет 2 (Важные)

- [ ] Добавить методы для отслеживания PID файлов
- [ ] Улучшить обработку ошибок в команд
- [ ] Расширить экспорт `__init__.py`
- [ ] Добавить кэширование в ProcessManager

### Приоритет 3 (Улучшения)

- [ ] Добавить команду `init`
- [ ] Добавить поддержку профилей
- [ ] Реализовать валидацию зависимостей
- [ ] Добавить конфигурационные файлы проектов
- [ ] Обработка системных сигналов

---

## 6. 🔧 Примеры Кода для Исправления

### Исправленный `list.py`

```python
def cmd_list(
    search_path: Annotated[Path | None, typer.Option("--path", "-p")] = None,
    format: Annotated[str, typer.Option("--format", "-f")] = "table",
) -> None:
    """List all running experts."""
    config = get_config()
    output = OutputFormatter()

    if search_path is None:
        search_path = Path.cwd()

    manager = ProcessManager(config.pid_dir)
    running = manager.list_running(search_path)

    if not running:
        output.info("No running experts found")
        return

    data = [
        {
            "Name": info.name,
            "PID": str(info.pid),
            "Status": info.status,
            "CPU %": f"{info.cpu_percent:.1f}",
            "Memory (MB)": f"{info.memory_mb:.1f}",
            "Started": info.started_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for info in running
    ]

    if format == "json":
        output.json_output(data)
    elif format == "yaml":
        output.display_yaml(data)
    else:
        output.custom_table(
            data,
            columns=["Name", "PID", "Status", "CPU %", "Memory (MB)", "Started"],
        )
```

---

## 7. 📚 Рекомендуемые Улучшения Документации

1. **CONTRIBUTING.md** - Как добавлять новые команды
2. **CLI_ARCHITECTURE.md** - Подробное описание архитектуры
3. **EXAMPLES.md** - Примеры использования всех команд
4. **TROUBLESHOOTING.md** - Решение частых проблем

---

## Заключение

Код CLI находится в **хорошем состоянии**, но требует нескольких исправлений импортов и недостающих методов. Предложенные улучшения сделают его более надежным и удобным для пользователей.

**Общая оценка:** 7.5/10 ✅

- Архитектура: 8/10
- Функциональность: 7/10  
- Документация: 8/10
- Обработка ошибок: 6.5/10
- Тестируемость: 7.5/10
