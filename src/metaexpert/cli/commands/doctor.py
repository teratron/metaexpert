"""Doctor command for CLI."""

from typing import Annotated, List, Tuple

import typer

from metaexpert.cli.core.dependencies import check_dependencies
from metaexpert.cli.core.output import OutputFormatter


def cmd_doctor() -> None:
    """Diagnose CLI environment."""
    output = OutputFormatter()

    # Check dependencies
    deps_ok = check_dependencies()

    # Check configuration
    from metaexpert.cli.core.config import CLIConfig

    try:
        config = CLIConfig.load()
        config_ok = True
        config_msg = "OK"
    except Exception as e:
        config_ok = False
        config_msg = str(e)

    # Check directories
    import os
    from pathlib import Path

    try:
        pid_dir = Path(config.pid_dir) if config_ok else Path.cwd()
        pid_dir_ok = pid_dir.exists() and os.access(pid_dir, os.W_OK)
        pid_dir_msg = "OK" if pid_dir_ok else f"Cannot write to {pid_dir}"
    except Exception as e:
        pid_dir_ok = False
        pid_dir_msg = str(e)

    try:
        log_dir = Path(config.log_dir) if config_ok else Path("logs")
        log_dir_ok = log_dir.exists() or log_dir.parent.exists()
        log_dir_msg = "OK" if log_dir_ok else f"Cannot access {log_dir}"
    except Exception as e:
        log_dir_ok = False
        log_dir_msg = str(e)

    # Check Python version
    import sys

    python_version = sys.version_info
    python_ok = python_version >= (3, 12)
    python_msg = (
        f"OK ({python_version.major}.{python_version.minor}.{python_version.micro})"
        if python_ok
        else f"Outdated ({python_version.major}.{python_version.minor}.{python_version.micro} < 3.12)"
    )

    # Collect all checks
    checks: List[Tuple[str, bool, str]] = [
        ("Dependencies", deps_ok, "Check dependencies" if not deps_ok else "OK"),
        ("Configuration", config_ok, config_msg),
        ("PID Directory", pid_dir_ok, pid_dir_msg),
        ("Log Directory", log_dir_ok, log_dir_msg),
        ("Python Version", python_ok, python_msg),
    ]

    # Display results
    data = [
        {
            "Check": name,
            "Status": "✅ OK" if status else "❌ FAIL",
            "Message": message,
        }
        for name, status, message in checks
    ]

    output.custom_table(
        data,
        columns=["Check", "Status", "Message"],
        title="Environment Diagnosis",
    )

    # Overall status
    if all(status for _, status, _ in checks):
        output.success("All checks passed!")
    else:
        output.error("Some checks failed. Please review the table above.")
        raise typer.Exit(code=1)