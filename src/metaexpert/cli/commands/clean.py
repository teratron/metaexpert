"""Clean command for CLI."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.output import OutputFormatter


def cmd_clean(
    project_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the project directory",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    logs: Annotated[bool, typer.Option("--logs", "-l", help="Clean log files")] = True,
    cache: Annotated[
        bool, typer.Option("--cache", "-c", help="Clean cache files")
    ] = True,
    all_files: Annotated[
        bool, typer.Option("--all", "-a", help="Clean all files including outputs")
    ] = False,
) -> None:
    """
    Clean project files.

    Args:
        project_path: Path to the project directory.
        logs: Clean log files.
        cache: Clean cache files.
        all_files: Clean all files including outputs.
    """
    output = OutputFormatter()

    cleaned_files = []

    # Clean log files
    if logs:
        log_dir = project_path / "logs"
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                try:
                    log_file.unlink()
                    cleaned_files.append(str(log_file))
                except Exception as e:
                    output.error(f"Failed to delete {log_file}: {e}")

    # Clean cache files
    if cache:
        cache_files = [
            ".metaexpert_cache",
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*~",
            ".DS_Store",
        ]
        for pattern in cache_files:
            for cache_file in project_path.rglob(pattern):
                try:
                    if cache_file.is_file():
                        cache_file.unlink()
                        cleaned_files.append(str(cache_file))
                    elif cache_file.is_dir():
                        # Recursively remove directory
                        import shutil

                        shutil.rmtree(cache_file)
                        cleaned_files.append(str(cache_file))
                except Exception as e:
                    output.error(f"Failed to delete {cache_file}: {e}")

    # Clean all files (outputs, etc.)
    if all_files:
        # Define patterns for output files
        output_patterns = [
            "*.csv",
            "*.json",
            "*.txt",
            "results/*",
            "output/*",
            "backtest_*",
        ]
        for pattern in output_patterns:
            for output_file in project_path.rglob(pattern):
                try:
                    if output_file.is_file():
                        output_file.unlink()
                        cleaned_files.append(str(output_file))
                    elif output_file.is_dir():
                        # Recursively remove directory
                        import shutil

                        shutil.rmtree(output_file)
                        cleaned_files.append(str(output_file))
                except Exception as e:
                    output.error(f"Failed to delete {output_file}: {e}")

    # Report results
    if cleaned_files:
        output.success(f"Cleaned {len(cleaned_files)} files/directories:")
        for file in cleaned_files:
            output.info(f"  - {file}")
    else:
        output.info("No files to clean.")
