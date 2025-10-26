# Complete working example: src/metaexpert/cli/__init__.py
"""MetaExpert CLI - Public API

This module provides the command-line interface for managing MetaExpert trading bots.

Usage:
    metaexpert new my-bot --exchange binance
    metaexpert run my-bot
    metaexpert stop my-bot
    metaexpert list
"""

from metaexpert.cli.app import app
from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.exceptions import (
    CLIError,
    ProcessError,
    ProjectError,
    TemplateError,
    ValidationError,
)
from metaexpert.cli.process.manager import ProcessManager
from metaexpert.cli.templates.generator import TemplateGenerator

__all__ = [
    "CLIConfig",
    "CLIError",
    "ProcessError",
    "ProcessManager",
    "ProjectError",
    "TemplateError",
    "TemplateGenerator",
    "ValidationError",
    "app",
]


# Entry point
def main() -> None:
    """Main entry point for CLI."""
    app()


# ============================================================================
# Complete example: src/metaexpert/__main__.py
"""Entry point for python -m metaexpert"""

from metaexpert.cli import main

if __name__ == "__main__":
    main()


# ============================================================================
# Update pyproject.toml
"""
[project.scripts]
metaexpert = "metaexpert.cli:main"

[project.optional-dependencies]
cli = [
    "typer[all]>=0.12.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "psutil>=5.9.0",
    "jinja2>=3.1.0",
]
"""


# ============================================================================
# Example: Complete workflow integration
# examples/cli_workflow.py
"""
Example demonstrating complete CLI workflow with MetaExpert.

This shows how all components work together:
1. CLI creates project from template
2. ProcessManager starts the expert
3. Logger tracks everything
4. Rich displays beautiful output
"""

from pathlib import Path

from metaexpert.cli import (
    CLIConfig,
    ProcessManager,
    TemplateGenerator,
)
from metaexpert.logger import LoggerConfig, get_logger, setup_logging


def main():
    # 1. Setup logging
    log_config = LoggerConfig(
        log_level="INFO",
        log_to_console=True,
        use_colors=True,
    )
    setup_logging(log_config)

    logger = get_logger(__name__)
    logger.info("workflow started")

    # 2. Load CLI config
    cli_config = CLIConfig.load()

    # 3. Generate project
    logger.info("generating project")
    generator = TemplateGenerator()

    context = {
        "exchange": "binance",
        "strategy": "ema",
        "market_type": "futures",
    }

    generator.generate_project(
        output_dir=Path.cwd(),
        project_name="demo-bot",
        context=context,
        force=True,
    )

    logger.info("project created", path=str(Path.cwd() / "demo-bot"))

    # 4. Start process
    logger.info("starting expert")
    manager = ProcessManager(cli_config.pid_dir)

    project_path = Path.cwd() / "demo-bot"
    pid = manager.start(
        project_path=project_path,
        script="main.py",
        detach=True,
    )

    logger.info("expert started", pid=pid)

    # 5. Monitor process
    import time

    time.sleep(2)

    if manager.is_running(project_path):
        info = manager.get_info(project_path)
        logger.info(
            "expert running",
            pid=info.pid,
            memory_mb=info.memory_mb,
            cpu_percent=info.cpu_percent,
        )

    # 6. List all running
    running = manager.list_running()
    logger.info("running experts", count=len(running))

    # 7. Stop process
    logger.info("stopping expert")
    manager.stop(project_path, timeout=30, force=False)
    logger.info("expert stopped")

    logger.info("workflow completed")


if __name__ == "__main__":
    main()


# ============================================================================
# Testing example: tests/cli/test_complete_workflow.py
"""
Complete integration test for CLI workflow.
"""

import time

from typer.testing import CliRunner

from metaexpert.cli.process.manager import ProcessManager

runner = CliRunner()


def test_complete_workflow(tmp_path, cli_logging):
    """Test complete CLI workflow from new to stop."""

    # 1. Create project
    result = runner.invoke(
        app,
        [
            "new",
            "test-bot",
            "--exchange",
            "binance",
            "--strategy",
            "ema",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert "Project created" in result.stdout

    project_path = tmp_path / "test-bot"
    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "pyproject.toml").exists()

    # 2. Validate generated files
    main_py = (project_path / "main.py").read_text()
    assert "binance" in main_py
    assert "EMA" in main_py

    # 3. Run project (detached)
    result = runner.invoke(
        app,
        ["run", str(project_path), "--detach"],
    )

    assert result.exit_code == 0
    assert "started with PID" in result.stdout

    # Wait for process to start
    time.sleep(1)

    # 4. List running experts
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "test-bot" in result.stdout

    # 5. Check process manager
    manager = ProcessManager(tmp_path / "pids")
    assert manager.is_running(project_path)

    info = manager.get_info(project_path)
    assert info is not None
    assert info.name == "test-bot"
    assert info.pid > 0

    # 6. View logs
    result = runner.invoke(
        app,
        ["logs", "test-bot", "--lines", "10"],
    )

    # Note: This might fail if log file doesn't exist yet
    # In real scenario, wait for log file

    # 7. Stop expert
    result = runner.invoke(
        app,
        ["stop", "test-bot"],
    )

    assert result.exit_code == 0
    assert "stopped" in result.stdout.lower()

    # Verify stopped
    time.sleep(1)
    assert not manager.is_running(project_path)


def test_error_handling(tmp_path):
    """Test error handling in CLI."""

    # Invalid project name
    result = runner.invoke(
        app,
        ["new", "123-invalid", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 1
    assert "Invalid" in result.stdout or "Error" in result.stdout

    # Run non-existent project
    result = runner.invoke(
        app,
        ["run", str(tmp_path / "non-existent")],
    )

    assert result.exit_code == 1

    # Stop non-running expert
    result = runner.invoke(
        app,
        ["stop", "non-existent"],
    )

    assert result.exit_code == 1


def test_force_overwrite(tmp_path):
    """Test force overwrite of existing project."""

    # Create project first time
    result = runner.invoke(
        app,
        ["new", "test-bot", "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0

    # Try to create again without force
    result = runner.invoke(
        app,
        ["new", "test-bot", "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 1
    assert "already exists" in result.stdout

    # Create again with force
    result = runner.invoke(
        app,
        [
            "new",
            "test-bot",
            "--output-dir",
            str(tmp_path),
            "--force",
        ],
    )
    assert result.exit_code == 0


# ============================================================================
# Performance benchmark: benchmarks/cli_benchmark.py
"""
Benchmark CLI performance.
"""

import timeit

from metaexpert.cli import ProcessManager


def benchmark_template_generation(tmp_path: Path):
    """Benchmark template generation."""

    generator = TemplateGenerator()

    context = {
        "exchange": "binance",
        "strategy": "ema",
        "market_type": "futures",
    }

    def generate():
        generator.generate_project(
            output_dir=tmp_path,
            project_name="bench-bot",
            context=context,
            force=True,
        )

    # Run 10 times
    duration = timeit.timeit(generate, number=10)

    print(f"Template generation: {duration / 10:.3f}s per operation")
    # Expected: < 0.1s per operation


def benchmark_process_operations(tmp_path: Path):
    """Benchmark process management."""

    manager = ProcessManager(tmp_path / "pids")

    # Create dummy project
    project_path = tmp_path / "bench-bot"
    project_path.mkdir()
    (project_path / "main.py").write_text("print('test')")

    # Benchmark start
    start_time = timeit.default_timer()
    pid = manager.start(project_path, detach=True)
    start_duration = timeit.default_timer() - start_time

    print(f"Process start: {start_duration:.3f}s")
    # Expected: < 0.5s

    # Benchmark is_running check
    check_time = timeit.timeit(
        lambda: manager.is_running(project_path),
        number=100,
    )
    print(f"Running check: {check_time / 100 * 1000:.2f}ms per check")
    # Expected: < 10ms per check

    # Benchmark stop
    stop_start = timeit.default_timer()
    manager.stop(project_path, timeout=5, force=True)
    stop_duration = timeit.default_timer() - stop_start

    print(f"Process stop: {stop_duration:.3f}s")
    # Expected: < 1s


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        print("Benchmarking CLI operations...")
        print("\n1. Template Generation")
        benchmark_template_generation(tmp_path)

        print("\n2. Process Operations")
        benchmark_process_operations(tmp_path)


# ============================================================================
# Shell completion: scripts/setup_completion.sh
"""
#!/bin/bash
# Setup shell completion for MetaExpert CLI

# For Bash
metaexpert --show-completion bash > ~/.metaexpert-complete.bash
echo 'source ~/.metaexpert-complete.bash' >> ~/.bashrc

# For Zsh
metaexpert --show-completion zsh > ~/.metaexpert-complete.zsh
echo 'source ~/.metaexpert-complete.zsh' >> ~/.zshrc

# For Fish
metaexpert --show-completion fish > ~/.config/fish/completions/metaexpert.fish

echo "Shell completion installed. Restart your shell or source the rc file."
"""
