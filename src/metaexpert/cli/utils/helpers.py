"""General helper utilities."""

import sys
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Get the root directory of the current project."""
    cwd = Path.cwd()

    # Look for project markers
    markers = ["pyproject.toml", "setup.py", ".git", "main.py"]

    current = cwd
    while current != current.parent:
        if any((current / marker).exists() for marker in markers):
            return current
        current = current.parent

    return cwd


def find_expert_file(directory: Path) -> Optional[Path]:
    """Find the main expert file in a directory."""
    candidates = ["main.py", "expert.py", "bot.py"]

    for candidate in candidates:
        file_path = directory / candidate
        if file_path.exists():
            return file_path

    return None


def is_venv_active() -> bool:
    """Check if running in a virtual environment."""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    required = ["typer", "rich", "pydantic", "psutil"]
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        from metaexpert.cli.core.output import error_console

        error_console.print(f"[red]Missing dependencies:[/] {', '.join(missing)}")
        error_console.print("\n[yellow]Install with:[/] pip install metaexpert[cli]")
        return False

    return True


def ensure_directory(path: Path, create: bool = True) -> Path:
    """Ensure directory exists, optionally create it."""
    if not path.exists() and create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def safe_read_file(path: Path, default: str = "") -> str:
    """Safely read file content with fallback."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return default


def safe_write_file(path: Path, content: str) -> bool:
    """Safely write file content."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except (PermissionError, OSError):
        return False
