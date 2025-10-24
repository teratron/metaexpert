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
            if manager.is_running(project
```
