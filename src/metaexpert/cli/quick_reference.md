# MetaExpert CLI - Quick Reference Card

## 🚀 Common Commands

```bash
# Create new project
metaexpert new my-bot --exchange binance --strategy ema

# Run expert (background)
metaexpert run my-bot

# Run expert (foreground)
metaexpert run my-bot --no-detach

# Stop expert
metaexpert stop my-bot

# List running experts
metaexpert list

# View logs
metaexpert logs my-bot --follow

# Backtest strategy
metaexpert backtest main.py --start-date 2024-01-01

# Show version
metaexpert --version

# Show help
metaexpert --help
```

---

## 📂 Key Module Structure

```python
# Import CLI components
from metaexpert.cli import (
    CLIConfig,              # Configuration management
    ProcessManager,          # Process lifecycle
    TemplateGenerator,       # Project generation
    app,                     # Main Typer app
)

# Import logger
from metaexpert.logger import (
    setup_logging,
    get_logger,
    log_context,
)

# Import exceptions
from metaexpert.cli.core.exceptions import (
    CLIError,
    ProcessError,
    TemplateError,
    ValidationError,
)
```

---

## 🔧 Configuration

### Environment Variables

```bash
export METAEXPERT_CLI_DEFAULT_EXCHANGE=binance
export METAEXPERT_CLI_PID_DIR=/var/run/metaexpert
export METAEXPERT_CLI_LOG_DIR=/var/log/metaexpert
export METAEXPERT_CLI_VERBOSE=true
```

### Config File (.metaexpert)

```ini
METAEXPERT_CLI_DEFAULT_EXCHANGE=binance
METAEXPERT_CLI_DEFAULT_STRATEGY=ema
METAEXPERT_CLI_PID_DIR=/var/run/metaexpert
```

---

## 💻 Programmatic Usage

### Process Management

```python
from pathlib import Path
from metaexpert.cli import ProcessManager

manager = ProcessManager(pid_dir=Path("/var/run"))

# Start
pid = manager.start(
    project_path=Path("./my-bot"),
    script="main.py",
    detach=True,
)

# Check status
if manager.is_running(Path("./my-bot")):
    info = manager.get_info(Path("./my-bot"))
    print(f"PID: {info.pid}, CPU: {info.cpu_percent}%")

# Stop
manager.stop(Path("./my-bot"), timeout=30, force=False)
```

### Template Generation

```python
from pathlib import Path
from metaexpert.cli import TemplateGenerator

generator = TemplateGenerator()

generator.generate_project(
    output_dir=Path.cwd(),
    project_name="my-bot",
    context={
        "exchange": "binance",
        "strategy": "ema",
        "market_type": "futures",
    },
    force=False,
)
```

### Logging Integration

```python
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__).bind(
    command="new",
    project="my-bot",
)

with log_context(phase="generation"):
    logger.info("creating project")
    # ... do work ...
    logger.info("project created successfully")
```

---

## 🧪 Testing

### Basic Test

```python
from typer.testing import CliRunner
from metaexpert.cli.app import app

runner = CliRunner()

def test_new_command():
    result = runner.invoke(app, ["new", "test-bot"])
    assert result.exit_code == 0
    assert "created" in result.stdout.lower()
```

### With Temporary Directory

```python
def test_with_tmpdir(tmp_path):
    result = runner.invoke(
        app,
        ["new", "test-bot", "--output-dir", str(tmp_path)],
    )
    assert (tmp_path / "test-bot" / "main.py").exists()
```

---

## 📝 Adding New Command

```python
# src/metaexpert/cli/commands/status.py
from typing import Annotated
import typer
from metaexpert.logger import get_logger

logger = get_logger(__name__)

def cmd_status(
    project_name: Annotated[
        str,
        typer.Argument(help="Project name"),
    ],
) -> None:
    """Show expert status."""
    logger.info("showing status", project=project_name)
    # Implementation...

# Register in app.py
from metaexpert.cli.commands import status
app.command(name="status")(status.cmd_status)
```

---

## 🎨 Output Formatting

```python
from metaexpert.cli.core.output import OutputFormatter

output = OutputFormatter()

# Messages
output.success("Operation completed")
output.error("Something failed")
output.warning("Be careful")
output.info("FYI")

# Table
data = [{"Name": "Bot1", "Status": "Running"}]
output.display_table(data, title="Experts")

# JSON
output.display_json({"status": "ok"})

# Tree
tree_data = {"project": {"files": ["main.py"]}}
output.display_tree(tree_data)
```

---

## 🔍 Debugging

```bash
# Enable debug mode
metaexpert --debug new my-bot

# Run with verbose output
metaexpert --verbose list

# Check logs
tail -f logs/cli.log

# Run with Python debugger
python -m pdb -m metaexpert new my-bot
```

---

## ⚡ Performance Tips

1. **Use detached mode** for background processes
2. **Cache logger instances** at module level
3. **Bind permanent context** to avoid repetition
4. **Use log_context** for temporary context
5. **Validate early** to fail fast
6. **Batch operations** when possible

---

## 🐛 Common Issues

### Issue: Permission denied

```bash
# Solution: Check directory permissions
chmod +x /var/run/metaexpert
```

### Issue: Process already running

```bash
# Solution: Stop existing process first
metaexpert stop my-bot
```

### Issue: Template not found

```bash
# Solution: Reinstall package
pip install --force-reinstall metaexpert[cli]
```

---

## 📚 Key Files

| File | Purpose | Lines |
|------|---------|-------|
| `cli/app.py` | Main Typer app | 120 |
| `cli/core/config.py` | Configuration | 100 |
| `cli/process/manager.py` | Process management | 200 |
| `cli/templates/generator.py` | Template engine | 150 |
| `cli/commands/new.py` | New command | 80 |
| `cli/commands/run.py` | Run command | 60 |

---

## 🔗 Links

- **Docs:** <https://teratron.github.io/metaexpert>
- **GitHub:** <https://github.com/teratron/metaexpert>
- **PyPI:** <https://pypi.org/project/metaexpert/>

---

**Version:** 2.0  
**Updated:** 2025-10-25
