# CLI + Logger Integration Guide

## 🔗 Integrating CLI with MetaExpert Logger

### Overview

The CLI module should integrate seamlessly with the MetaExpert logger (`logger`) for consistent logging across the entire application.

---

## 1. Logger Setup in CLI

### Main Application Logger

```python
# src/metaexpert/cli/app.py
import structlog
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Initialize CLI logger
def _setup_cli_logging(verbose: bool = False) -> None:
    """Setup logging for CLI operations."""
    config = LoggerConfig(
        log_level="DEBUG" if verbose else "INFO",
        log_to_console=True,
        log_to_file=False,  # CLI doesn't need file logging
        use_colors=True,
        json_logs=False,
    )
    setup_logging(config)

# Get CLI logger
cli_logger = get_logger("metaexpert.cli")

@app.callback()
def main(verbose: bool = False) -> None:
    """Setup CLI environment."""
    _setup_cli_logging(verbose)
    cli_logger.info("cli started", verbose=verbose)
```

### Command-Level Logging

```python
# src/metaexpert/cli/commands/new.py
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__)

def cmd_new(project_name: str, exchange: str) -> None:
    """Create new project with structured logging."""
    
    # Bind permanent context
    cmd_logger = logger.bind(
        command="new",
        project_name=project_name,
        exchange=exchange,
    )
    
    cmd_logger.info("creating project")
    
    try:
        # Use context for temporary data
        with log_context(template="default", output_dir=str(output_dir)):
            generator.generate_project(...)
            cmd_logger.info("project created successfully")
    
    except TemplateError as e:
        cmd_logger.error("project creation failed", error=str(e), exc_info=True)
        raise typer.Exit(code=1)
```

---

## 2. Process Management Logging

### Enhanced ProcessManager with Logging

```python
# src/metaexpert/cli/process/manager.py
from metaexpert.logger import get_logger, log_context

class ProcessManager:
    """Process manager with integrated logging."""
    
    def __init__(self, pid_dir: Path):
        self.pid_dir = pid_dir
        self.logger = get_logger(__name__).bind(
            component="ProcessManager",
            pid_dir=str(pid_dir),
        )
    
    def start(self, project_path: Path, script: str, detach: bool) -> int:
        """Start process with detailed logging."""
        
        with log_context(
            project=project_path.name,
            script=script,
            mode="detached" if detach else "attached",
        ):
            self.logger.info("starting process")
            
            # Check if already running
            if self.is_running(project_path):
                self.logger.warning(
                    "process already running",
                    existing_pid=self._read_pid(self._get_pid_file(project_path)),
                )
                raise ProcessError("Already running")
            
            try:
                # Start process
                if detach:
                    pid = self._start_detached(command, project_path)
                else:
                    pid = self._start_attached(command, project_path)
                
                self.logger.info(
                    "process started successfully",
                    pid=pid,
                    command=" ".join(command),
                )
                
                return pid
            
            except Exception as e:
                self.logger.error(
                    "process start failed",
                    error=str(e),
                    exc_info=True,
                )
                raise
    
    def stop(self, project_path: Path, timeout: int, force: bool) -> None:
        """Stop process with logging."""
        
        with log_context(
            project=project_path.name,
            timeout=timeout,
            force=force,
        ):
            pid = self._read_pid(self._get_pid_file(project_path))
            
            self.logger.info("stopping process", pid=pid)
            
            try:
                process = psutil.Process(pid)
                
                if not force:
                    self.logger.debug("sending SIGTERM", pid=pid)
                    process.terminate()
                    
                    try:
                        process.wait(timeout=timeout)
                        self.logger.info("process terminated gracefully", pid=pid)
                    except psutil.TimeoutExpired:
                        if force:
                            self.logger.warning("timeout expired, killing process", pid=pid)
                            process.kill()
                        else:
                            raise
                else:
                    self.logger.warning("force killing process", pid=pid)
                    process.kill()
                
                self.logger.info("process stopped successfully", pid=pid)
            
            except Exception as e:
                self.logger.error(
                    "failed to stop process",
                    pid=pid,
                    error=str(e),
                    exc_info=True,
                )
                raise
```

---

## 3. Template Generator Logging

```python
# src/metaexpert/cli/templates/generator.py
from metaexpert.logger import get_logger, log_context

class TemplateGenerator:
    """Template generator with comprehensive logging."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or self._get_default_dir()
        self.logger = get_logger(__name__).bind(
            component="TemplateGenerator",
            template_dir=str(self.template_dir),
        )
        
        self.logger.debug("template generator initialized")
    
    def generate_project(
        self,
        output_dir: Path,
        project_name: str,
        context: Dict[str, Any],
        force: bool,
    ) -> None:
        """Generate project with detailed logging."""
        
        project_path = output_dir / project_name
        
        with log_context(
            project_name=project_name,
            output_dir=str(output_dir),
            force=force,
        ):
            self.logger.info("generating project", context_keys=list(context.keys()))
            
            # Validation
            if project_path.exists() and not force:
                self.logger.warning("project directory exists", path=str(project_path))
                raise TemplateError("Directory exists")
            
            try:
                # Generate files
                self.logger.debug("generating main.py")
                self._generate_main_file(project_path, context)
                
                self.logger.debug("generating .env.example")
                self._generate_env_file(project_path, context)
                
                self.logger.debug("generating .gitignore")
                self._generate_gitignore(project_path)
                
                self.logger.debug("generating README.md")
                self._generate_readme(project_path, context)
                
                self.logger.debug("generating pyproject.toml")
                self._generate_pyproject_toml(project_path, context)
                
                self.logger.info(
                    "project generated successfully",
                    files_created=5,
                    project_path=str(project_path),
                )
            
            except Exception as e:
                self.logger.error(
                    "project generation failed",
                    error=str(e),
                    exc_info=True,
                )
                
                # Cleanup
                if project_path.exists():
                    self.logger.debug("cleaning up failed generation", path=str(project_path))
                    shutil.rmtree(project_path)
                
                raise TemplateError(f"Generation failed: {e}") from e
```

---

## 4. Command-Specific Logging Patterns

### New Command

```python
# src/metaexpert/cli/commands/new.py
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__)

def cmd_new(project_name: str, **kwargs) -> None:
    """Create new project."""
    
    # Create command-specific logger
    cmd_logger = logger.bind(
        command="new",
        project_name=project_name,
    )
    
    cmd_logger.info("command started", kwargs=kwargs)
    
    # Validation phase
    with log_context(phase="validation"):
        cmd_logger.debug("validating inputs")
        validate_project_name(project_name)
        validate_exchange(kwargs["exchange"])
        cmd_logger.debug("validation passed")
    
    # Generation phase
    with log_context(phase="generation"):
        cmd_logger.debug("preparing template context")
        context = _prepare_context(kwargs)
        
        cmd_logger.debug("generating project files")
        generator.generate_project(...)
    
    # Completion
    cmd_logger.info(
        "command completed successfully",
        duration_ms=...,
    )
```

### Run Command

```python
# src/metaexpert/cli/commands/run.py
from metaexpert.logger import get_logger, log_context

logger = get_logger(__name__)

def cmd_run(project_path: Path, **kwargs) -> None:
    """Run expert."""
    
    cmd_logger = logger.bind(
        command="run",
        project=project_path.name,
    )
    
    cmd_logger.info("starting expert", detach=kwargs["detach"])
    
    try:
        # Pre-flight checks
        with log_context(phase="preflight"):
            cmd_logger.debug("checking project structure")
            _validate_project(project_path)
            
            cmd_logger.debug("checking for existing process")
            if manager.is_running(project_path):
                cmd_logger.warning("expert already running")
                raise ProcessError("Already running")
        
        # Start process
        with log_context(phase="startup"):
            pid = manager.start(project_path, **kwargs)
            cmd_logger.info("expert started", pid=pid)
        
        # Post-startup monitoring
        with log_context(phase="monitoring"):
            cmd_logger.debug("waiting for process initialization")
            time.sleep(2)
            
            if manager.is_running(project_path):
                info = manager.get_info(project_path)
                cmd_logger.info(
                    "process verified running",
                    pid=pid,
                    memory_mb=info.memory_mb,
                    cpu_percent=info.cpu_percent,
                )
            else:
                cmd_logger.error("process died immediately after start")
                raise ProcessError("Failed to start")
    
    except Exception as e:
        cmd_logger.error("command failed", error=str(e), exc_info=True)
        raise typer.Exit(code=1)
```

### Stop Command

```python
# src/metaexpert/cli/commands/stop.py
from metaexpert.logger import get_logger, log_context, bind_contextvars

logger = get_logger(__name__)

def cmd_stop(project_name: str, **kwargs) -> None:
    """Stop expert with comprehensive logging."""
    
    # Bind context for entire command
    bind_contextvars(
        command="stop",
        project=project_name,
        force=kwargs.get("force", False),
        timeout=kwargs.get("timeout", 30),
    )
    
    logger.info("stopping expert")
    
    project_path = Path.cwd() / project_name
    
    try:
        # Validate project exists
        with log_context(phase="validation"):
            logger.debug("checking project path", path=str(project_path))
            
            if not manager.is_running(project_path):
                logger.warning("expert not running")
                raise ProcessError("Not running")
            
            info = manager.get_info(project_path)
            logger.info(
                "expert found",
                pid=info.pid,
                uptime=...,
            )
        
        # Stop process
        with log_context(phase="shutdown"):
            logger.info("initiating shutdown")
            manager.stop(project_path, **kwargs)
            logger.info("expert stopped successfully")
    
    except Exception as e:
        logger.error("failed to stop expert", error=str(e), exc_info=True)
        raise typer.Exit(code=1)
```

---

## 5. Output Integration

### Combining Rich Output with Logging

```python
# src/metaexpert/cli/core/output.py
from metaexpert.logger import get_logger
from rich.console import Console

console = Console()
logger = get_logger(__name__)

class OutputFormatter:
    """Output formatter with integrated logging."""
    
    def success(self, message: str, **extra) -> None:
        """Display success and log."""
        console.print(f"[green]✓[/] {message}")
        logger.info(message, level="success", **extra)
    
    def error(self, message: str, **extra) -> None:
        """Display error and log."""
        console.print(f"[red]✗[/] {message}", file=sys.stderr)
        logger.error(message, level="error", **extra)
    
    def warning(self, message: str, **extra) -> None:
        """Display warning and log."""
        console.print(f"[yellow]⚠[/] {message}")
        logger.warning(message, level="warning", **extra)
    
    def display_table(self, data: List[Dict], **kwargs) -> None:
        """Display table and log summary."""
        # Display rich table
        table = Table(...)
        console.print(table)
        
        # Log summary
        logger.info(
            "displayed table",
            rows=len(data),
            columns=len(data[0]) if data else 0,
            **kwargs,
        )
```

---

## 6. Testing with Logger

### Test Setup

```python
# tests/cli/conftest.py
import pytest
from metaexpert.logger import setup_logging, LoggerConfig
from pathlib import Path
import tempfile

@pytest.fixture(scope="session")
def cli_logging():
    """Setup CLI logging for tests."""
    config = LoggerConfig(
        log_level="DEBUG",
        log_to_console=False,
        log_to_file=True,
        log_dir=Path(tempfile.gettempdir()) / "metaexpert_cli_tests",
    )
    setup_logging(config)

@pytest.fixture
def capture_logs(caplog):
    """Capture logs in tests."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog
```

### Test with Log Assertions

```python
# tests/cli/test_new_command.py
def test_new_command_logs(cli_logging, capture_logs):
    """Test that new command logs appropriately."""
    from metaexpert.cli.commands.new import cmd_new
    
    # Run command
    cmd_new(
        project_name="test-bot",
        exchange="binance",
        strategy="ema",
    )
    
    # Assert log messages
    assert "command started" in capture_logs.text
    assert "validating inputs" in capture_logs.text
    assert "generating project" in capture_logs.text
    assert "command completed successfully" in capture_logs.text
    
    # Assert structured data logged
    records = [r for r in capture_logs.records if r.name.startswith("metaexpert.cli")]
    assert len(records) > 0
    
    # Check specific log record
    start_record = next(r for r in records if "command started" in r.message)
    assert start_record.project_name == "test-bot"
    assert start_record.exchange == "binance"
```

---

## 7. Production Logging Configuration

### CLI in Production

```python
# src/metaexpert/cli/app.py
import os
from pathlib import Path

def _get_production_log_config() -> LoggerConfig:
    """Get logging config for production CLI."""
    
    # Use system directories in production
    if os.getenv("METAEXPERT_ENV") == "production":
        return LoggerConfig(
            log_level="WARNING",
            log_to_console=True,
            log_to_file=True,
            log_dir=Path("/var/log/metaexpert/cli"),
            json_logs=True,  # Structured logs for parsing
            use_colors=False,
        )
    
    # Development config
    return LoggerConfig(
        log_level="DEBUG",
        log_to_console=True,
        log_to_file=False,
        use_colors=True,
        json_logs=False,
    )

@app.callback()
def main(verbose: bool = False) -> None:
    """Setup CLI with environment-aware logging."""
    config = _get_production_log_config()
    
    if verbose:
        config.log_level = "DEBUG"
    
    setup_logging(config)
```

### Systemd Integration

```ini
# /etc/systemd/system/metaexpert-cli.service
[Unit]
Description=MetaExpert CLI Service
After=network.target

[Service]
Type=simple
User=metaexpert
Environment="METAEXPERT_ENV=production"
Environment="METAEXPERT_CLI_PID_DIR=/var/run/metaexpert"
Environment="METAEXPERT_CLI_LOG_DIR=/var/log/metaexpert"
ExecStart=/usr/local/bin/metaexpert run /opt/metaexpert/bots/production-bot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 8. Debug Mode

### Enhanced Debug Output

```python
# src/metaexpert/cli/app.py
@app.callback()
def main(
    verbose: bool = False,
    debug: bool = False,  # New debug flag
) -> None:
    """CLI with debug mode."""
    
    if debug:
        # Enable detailed logging
        config = LoggerConfig(
            log_level="DEBUG",
            log_to_console=True,
            log_to_file=True,
            log_dir=Path("./debug_logs"),
            json_logs=False,
        )
        setup_logging(config)
        
        # Log environment
        logger = get_logger(__name__)
        logger.debug("debug mode enabled")
        logger.debug("python version", version=sys.version)
        logger.debug("platform", platform=sys.platform)
        logger.debug("cwd", cwd=str(Path.cwd()))
        logger.debug("environment", env=dict(os.environ))
    
    elif verbose:
        # Just verbose, not debug
        config = LoggerConfig(log_level="INFO", ...)
        setup_logging(config)

# Usage:
# metaexpert --debug new my-bot
```

---

## 9. Performance Monitoring

### Command Execution Metrics

```python
# src/metaexpert/cli/core/metrics.py
import time
from functools import wraps
from metaexpert.logger import get_logger

logger = get_logger(__name__)

def track_command_execution(func):
    """Decorator to track command execution time."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        command_name = func.__name__.replace("cmd_", "")
        
        logger.info(
            "command execution started",
            command=command_name,
        )
        
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            logger.info(
                "command execution completed",
                command=command_name,
                duration_seconds=round(duration, 3),
                status="success",
            )
            
            return result
        
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "command execution failed",
                command=command_name,
                duration_seconds=round(duration, 3),
                status="error",
                error=str(e),
                exc_info=True,
            )
            raise
    
    return wrapper

# Usage in commands:
@track_command_execution
def cmd_new(project_name: str, **kwargs) -> None:
    """Create new project."""
    ...
```

---

## 10. Best Practices Summary

### ✅ DO

1. **Use structured logging everywhere**

   ```python
   logger.info("process started", pid=12345, mode="detached")
   ```

2. **Bind permanent context**

   ```python
   cmd_logger = logger.bind(command="new", project="my-bot")
   ```

3. **Use log_context for temporary context**

   ```python
   with log_context(phase="validation"):
       logger.debug("validating")
   ```

4. **Log at appropriate levels**
   - DEBUG: Detailed diagnostic info
   - INFO: Important events (command start/end)
   - WARNING: Unusual but not error (already running)
   - ERROR: Error conditions with exc_info=True

5. **Include relevant metadata**

   ```python
   logger.info("file created", path=str(file_path), size_bytes=1024)
   ```

### ❌ DON'T

1. **Don't use print() statements**

   ```python
   # Bad
   print(f"Creating project {name}")
   
   # Good
   logger.info("creating project", project_name=name)
   ```

2. **Don't log sensitive data**

   ```python
   # Bad
   logger.info("api configured", api_key=api_key)
   
   # Good
   logger.info("api configured", api_key_prefix=api_key[:8]+"...")
   ```

3. **Don't repeat context in every call**

   ```python
   # Bad
   logger.info("step 1", project="bot1")
   logger.info("step 2", project="bot1")
   
   # Good
   logger = logger.bind(project="bot1")
   logger.info("step 1")
   logger.info("step 2")
   ```

4. **Don't ignore exceptions**

   ```python
   # Bad
   try:
       ...
   except Exception:
       pass
   
   # Good
   try:
       ...
   except Exception as e:
       logger.error("operation failed", exc_info=True)
       raise
   ```

---

## 📊 Monitoring & Analytics

### Aggregate CLI Usage

```python
# scripts/analyze_cli_logs.py
"""Analyze CLI usage from structured logs."""

import json
from pathlib import Path
from collections import Counter

def analyze_logs(log_dir: Path):
    """Analyze CLI command usage."""
    
    commands = Counter()
    errors = []
    durations = []
    
    for log_file in log_dir.glob("*.log"):
        with open(log_file) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    # Count commands
                    if entry.get("event") == "command execution started":
                        commands[entry["command"]] += 1
                    
                    # Track errors
                    if entry.get("level") == "error":
                        errors.append(entry)
                    
                    # Track durations
                    if "duration_seconds" in entry:
                        durations.append({
                            "command": entry["command"],
                            "duration": entry["duration_seconds"],
                        })
                
                except json.JSONDecodeError:
                    continue
    
    print("Command Usage:")
    for cmd, count in commands.most_common():
        print(f"  {cmd}: {count}")
    
    print(f"\nTotal Errors: {len(errors)}")
    
    if durations:
        avg_duration = sum(d["duration"] for d in durations) / len(durations)
        print(f"\nAverage Duration: {avg_duration:.2f}s")
```

---

## 🎯 Summary

The integrated CLI with logger provides:

1. ✅ **Consistent logging** across all CLI operations
2. ✅ **Structured data** for easy parsing and analysis
3. ✅ **Context management** for related log entries
4. ✅ **Performance tracking** with execution metrics
5. ✅ **Error tracking** with full stack traces
6. ✅ **Production-ready** with environment-aware config
7. ✅ **Testable** with log assertions
8. ✅ **Debuggable** with enhanced debug mode
9. ✅ **Monitorable** with aggregated analytics
10. ✅ **Maintainable** with clear patterns and practices
