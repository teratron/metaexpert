# MetaExpert CLI - Usage Guide & Best Practices

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Installation & Setup](#installation--setup)
3. [Command Reference](#command-reference)
4. [Integration Patterns](#integration-patterns)
5. [Best Practices](#best-practices)
6. [Testing](#testing)
7. [Migration Guide](#migration-guide)

---

## 🏗️ Architecture Overview

### New Structure

```
src/metaexpert/cli/
├── __init__.py         # Public API exports
├── app.py              # Main Typer application
├── commands/           # Command handlers (one file per command)
│   ├── new.py
│   ├── run.py
│   ├── stop.py
│   ├── list.py
│   ├── logs.py
│   └── backtest.py
├── core/               # Core functionality
│   ├── config.py       # CLI configuration with Pydantic
│   ├── exceptions.py   # CLI-specific exceptions
│   └── output.py       # Rich-based output formatting
├── process/            # Process lifecycle management
│   ├── manager.py      # ProcessManager class
│   └── pid_lock.py     # Cross-platform PID locking
├── templates/          # Jinja2 template system
│   ├── generator.py    # TemplateGenerator class
│   └── files/          # Template files (.j2)
└── utils/              # Utilities
    ├── validators.py   # Input validation
    ├── formatters.py   # Output formatting
    └── helpers.py      # General helpers
```

### Key Improvements

1. **Proper Typer Integration**: Full use of decorators, type hints, and Rich integration
2. **Process Management**: Robust cross-platform process handling with psutil
3. **Template System**: Jinja2-based templates with validation
4. **Configuration**: Pydantic-based config with environment support
5. **Output**: Rich library for beautiful terminal output
6. **Error Handling**: Structured exceptions with proper exit codes

---

## 🚀 Installation & Setup

### Dependencies

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
cli = [
    "typer[all]>=0.12.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "psutil>=5.9.0",
    "jinja2>=3.1.0",
]
```

### Installation

```bash
# Install with CLI support
pip install metaexpert[cli]

# Or with uv
uv pip install "metaexpert[cli]"
```

---

## 📚 Command Reference

### `metaexpert new`

Create a new expert project from template.

```bash
# Basic usage
metaexpert new my-bot

# With options
metaexpert new my-bot \
  --exchange binance \
  --strategy ema \
  --market-type futures \
  --output-dir ./projects

# Available strategies
metaexpert new my-bot --strategy ema    # EMA crossover
metaexpert new my-bot --strategy rsi    # RSI oscillator
metaexpert new my-bot --strategy macd   # MACD
```

**Features:**

- ✅ Jinja2 template rendering
- ✅ Strategy-specific code hints
- ✅ Proper .gitignore and .env.example
- ✅ Exchange-specific configuration
- ✅ Validates project names

### `metaexpert run`

Run an expert in background or foreground.

```bash
# Run in current directory (detached by default)
metaexpert run

# Run specific project
metaexpert run ./my-bot

# Run in foreground (attached to terminal)
metaexpert run --no-detach

# Custom script
metaexpert run --script custom.py
```

**Features:**

- ✅ Cross-platform process management
- ✅ PID file locking
- ✅ Detached/attached modes
- ✅ Automatic duplicate detection

### `metaexpert stop`

Stop a running expert gracefully or forcefully.

```bash
# Graceful stop (30s timeout)
metaexpert stop my-bot

# Force kill
metaexpert stop my-bot --force

# Custom timeout
metaexpert stop my-bot --timeout 60
```

**Features:**

- ✅ Graceful SIGTERM shutdown
- ✅ Force kill with --force
- ✅ Configurable timeout
- ✅ Automatic cleanup

### `metaexpert list`

List all running experts with resource usage.

```bash
# Table view (default)
metaexpert list

# JSON output
metaexpert list --format json

# YAML output
metaexpert list --format yaml

# Search in specific path
metaexpert list --path ./projects
```

**Output includes:**

- Name, PID, Status
- CPU and Memory usage
- Start time
- Project path

### `metaexpert logs`

View expert logs in real-time.

```bash
# Show last 50 lines
metaexpert logs my-bot

# Follow logs (tail -f)
metaexpert logs my-bot --follow

# Show more lines
metaexpert logs my-bot --lines 100

# Filter by level
metaexpert logs my-bot --level ERROR
```

### `metaexpert backtest`

Backtest a strategy (planned feature).

```bash
metaexpert backtest main.py \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --capital 10000
```

---

## 🔧 Integration Patterns

### 1. Using CLI Configuration

```python
# src/metaexpert/cli/app.py
from metaexpert.cli.core.config import CLIConfig

# Global config instance
config = CLIConfig.load()

# Access in commands
def cmd_new(...):
    config = get_config()
    exchange = config.default_exchange
    verbose = config.verbose
```

**Environment Variables:**

```bash
# .metaexpert file or environment
export METAEXPERT_CLI_DEFAULT_EXCHANGE=binance
export METAEXPERT_CLI_DEFAULT_STRATEGY=ema
export METAEXPERT_CLI_PID_DIR=/var/run/metaexpert
export METAEXPERT_CLI_LOG_DIR=/var/log/metaexpert
```

### 2. Adding New Commands

```python
# src/metaexpert/cli/commands/status.py
from typing import Annotated
import typer
from metaexpert.cli.core.output import OutputFormatter

def cmd_status(
    project_name: Annotated[
        str,
        typer.Argument(help="Project name"),
    ],
    detailed: Annotated[
        bool,
        typer.Option("--detailed", "-d", help="Show detailed info"),
    ] = False,
) -> None:
    """
    Show detailed status of an expert.
    
    Example:
        metaexpert status my-bot --detailed
    """
    output = OutputFormatter()
    
    # Implementation
    ...
    
    output.success("Status retrieved")

# Register in app.py
from metaexpert.cli.commands import status
app.command(name="status")(status.cmd_status)
```

### 3. Process Management Integration

```python
from metaexpert.cli.process.manager import ProcessManager
from pathlib import Path

manager = ProcessManager(pid_dir=Path("/var/run"))

# Start process
pid = manager.start(
    project_path=Path("./my-bot"),
    script="main.py",
    detach=True,
)

# Check status
if manager.is_running(Path("./my-bot")):
    info = manager.get_info(Path("./my-bot"))
    print(f"CPU: {info.cpu_percent}%")
    print(f"Memory: {info.memory_mb} MB")

# Stop process
manager.stop(
    project_path=Path("./my-bot"),
    timeout=30,
    force=False,
)

# List all running
running = manager.list_running(Path.cwd())
for info in running:
    print(f"{info.name}: PID {info.pid}")
```

### 4. Template Customization

```python
from metaexpert.cli.templates.generator import TemplateGenerator
from pathlib import Path

# Use custom templates
generator = TemplateGenerator(
    template_dir=Path("/custom/templates")
)

# Generate project
context = {
    "exchange": "binance",
    "strategy": "ema",
    "custom_field": "value",
}

generator.generate_project(
    output_dir=Path.cwd(),
    project_name="my-bot",
    context=context,
    force=False,
)

# Add custom template file
# /custom/templates/main.py.j2
```

### 5. Output Formatting

```python
from metaexpert.cli.core.output import OutputFormatter, console

output = OutputFormatter()

# Success/Error/Warning/Info
output.success("Operation completed")
output.error("Something went wrong")
output.warning("Be careful")
output.info("FYI")

# Tables
data = [
    {"Name": "Bot1", "Status": "Running", "PID": 12345},
    {"Name": "Bot2", "Status": "Stopped", "PID": None},
]
output.display_table(data, title="Experts")

# JSON
output.display_json({"status": "ok", "data": [1, 2, 3]})

# Tree structure
tree_data = {
    "project": {
        "name": "my-bot",
        "files": ["main.py", "config.json"],
    }
}
output.display_tree(tree_data, root_label="Project")

# Panels
output.panel(
    "This is important information",
    title="Notice"
)

# Progress
from metaexpert.cli.core.output import progress_context

with progress_context("Processing...") as progress:
    task = progress.add_task("Working", total=100)
    for i in range(100):
        progress.update(task, advance=1)
```

---

## ✅ Best Practices

### 1. Command Design

```python
# ✅ GOOD: Clear, typed, documented
def cmd_run(
    project_path: Annotated[
        Path,
        typer.Argument(
            help="Path to expert project",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    detach: Annotated[
        bool,
        typer.Option("--detach", "-d", help="Run in background"),
    ] = True,
) -> None:
    """
    Run a trading expert.
    
    This command starts the expert process and manages its lifecycle.
    Use --detach to run in background (default).
    
    Example:
        metaexpert run my-bot
        metaexpert run my-bot --no-detach
    """
    ...

# ❌ BAD: No types, unclear
def cmd_run(project, detach=True):
    """Run expert."""
    ...
```

### 2. Error Handling

```python
# ✅ GOOD: Structured exceptions
from metaexpert.cli.core.exceptions import ProcessError, ValidationError

def cmd_stop(project_name: str) -> None:
    try:
        validate_project_name(project_name)
        manager.stop(project_path)
    except ValidationError as e:
        output.error(f"Invalid project name: {e}")
        raise typer.Exit(code=1)
    except ProcessError as e:
        output.error(f"Failed to stop: {e}")
        raise typer.Exit(code=1)

# ❌ BAD: Generic exceptions
def cmd_stop(project_name):
    try:
        manager.stop(project_name)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
```

### 3. Configuration Management

```python
# ✅ GOOD: Pydantic config
from metaexpert.cli.core.config import CLIConfig

config = CLIConfig(
    default_exchange="binance",
    pid_dir=Path("/var/run/metaexpert"),
    verbose=True,
)
config.save()  # Persists to .metaexpert

# ❌ BAD: Global variables
DEFAULT_EXCHANGE = "binance"
PID_DIR = "/var/run/metaexpert"
```

### 4. Validation

```python
# ✅ GOOD: Comprehensive validation
from metaexpert.cli.utils.validators import (
    validate_project_name,
    validate_exchange,
    validate_date_format,
)

def cmd_new(project_name: str, exchange: str) -> None:
    validate_project_name(project_name)
    validate_exchange(exchange)
    
    # Proceed with valid data

# ❌ BAD: No validation or weak validation
def cmd_new(project_name, exchange):
    if not project_name:
        print("Invalid name")
        return
```

### 5. Testing Commands

```python
# tests/cli/test_new_command.py
import pytest
from typer.testing import CliRunner
from metaexpert.cli.app import app

runner = CliRunner()

def test_new_command_success(tmp_path):
    """Test successful project creation."""
    result = runner.invoke(
        app,
        ["new", "test-bot", "--output-dir", str(tmp_path)],
    )
    
    assert result.exit_code == 0
    assert "Project created" in result.stdout
    assert (tmp_path / "test-bot" / "main.py").exists()

def test_new_command_duplicate():
    """Test error when project exists."""
    result = runner.invoke(app, ["new", "existing-bot"])
    
    assert result.exit_code == 1
    assert "already exists" in result.stdout

def test_new_command_invalid_name():
    """Test validation of project name."""
    result = runner.invoke(app, ["new", "123-invalid"])
    
    assert result.exit_code == 1
    assert "Invalid" in result.stdout
```

---

## 🧪 Testing

### Unit Tests

```python
# tests/cli/test_process_manager.py
import pytest
from metaexpert.cli.process.manager import ProcessManager

def test_process_start(tmp_path):
    manager = ProcessManager(pid_dir=tmp_path)
    
    # Start process
    pid = manager.start(
        project_path=Path("./test-bot"),
        script="main.py",
        detach=True,
    )
    
    assert pid > 0
    assert manager.is_running(Path("./test-bot"))

def test_process_stop(tmp_path):
    manager = ProcessManager(pid_dir=tmp_path)
    pid = manager.start(...)
    
    manager.stop(Path("./test-bot"))
    assert not manager.is_running(Path("./test-bot"))
```

### Integration Tests

```python
# tests/cli/test_integration.py
def test_full_workflow(tmp_path):
    """Test complete workflow: new -> run -> stop."""
    runner = CliRunner()
    
    # Create project
    result = runner.invoke(
        app,
        ["new", "test-bot", "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0
    
    # Run project
    result = runner.invoke(
        app,
        ["run", str(tmp_path / "test-bot")],
    )
    assert result.exit_code == 0
    
    # Check status
    result = runner.invoke(app, ["list"])
    assert "test-bot" in result.stdout
    
    # Stop project
    result = runner.invoke(app, ["stop", "test-bot"])
    assert result.exit_code == 0
```

---

## 🔄 Migration Guide

### From Old CLI to New CLI

#### 1. Update Imports

```python
# OLD
from metaexpert.cli.main import app
from metaexpert.cli.commands.new import cmd_new

# NEW
from metaexpert.cli.app import app
from metaexpert.cli.commands.new import cmd_new
```

#### 2. Update Command Registration

```python
# OLD
app.add_typer(commands_app, name="commands")

# NEW
# Commands auto-registered in app.py
from metaexpert.cli.commands import new, run
app.command(name="new")(new.cmd_new)
app.command(name="run")(run.cmd_run)
```

#### 3. Update Process Management

```python
# OLD
from metaexpert.cli.pid_lock import PidFileLock
with PidFileLock(pid_file):
    # Start process manually

# NEW
from metaexpert.cli.process.manager import ProcessManager
manager = ProcessManager(pid_dir=Path("/var/run"))
pid = manager.start(project_path, detach=True)
```

#### 4. Update Output

```python
# OLD
print(f"[SUCCESS] Project created")
typer.secho("Error", fg="red")

# NEW
from metaexpert.cli.core.output import OutputFormatter
output = OutputFormatter()
output.success("Project created")
output.error("Error occurred")
```

---

## 📝 Summary

### Key Features

1. ✅ **Type-safe commands** with Typer decorators
2. ✅ **Rich output** with tables, colors, progress bars
3. ✅ **Robust process management** with psutil
4. ✅ **Jinja2 templates** for flexible project generation
5. ✅ **Pydantic configuration** with environment support
6. ✅ **Comprehensive validation** at every step
7. ✅ **Cross-platform** PID file locking
8. ✅ **Structured exceptions** with proper exit codes
9. ✅ **Testable** with CliRunner
10. ✅ **Well-documented** with examples

### Performance Optimizations

- Lazy imports for faster startup
- psutil for efficient process monitoring
- Cached configuration
- Minimal dependencies

### Next Steps

1. Implement remaining commands (backtest, config, etc.)
2. Add shell completion scripts
3. Create comprehensive test suite
4. Add performance benchmarks
5. Write user documentation
6. Create video tutorials

---

**Documentation:** <https://teratron.github.io/metaexpert>  
**Repository:** <https://github.com/teratron/metaexpert>  
**Issues:** <https://github.com/teratron/metaexpert/issues>
