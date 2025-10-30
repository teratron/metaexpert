"""Import command for CLI."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.output import OutputFormatter


def cmd_import(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input file",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ],
    project_path: Annotated[
        Path,
        typer.Option(
            "--project-path",
            "-p",
            help="Path to the project directory (default: current directory)",
        ),
    ] = Path("."),
    format: Annotated[
        str,
        typer.Option("--format", "-f", help="Import format (auto, json, csv, yaml)"),
    ] = "auto",
    overwrite: Annotated[
        bool, typer.Option("--overwrite", "-o", help="Overwrite existing files")
    ] = False,
) -> None:
    """
    Import project data.

    Args:
        input_file: Path to the input file.
        project_path: Path to the project directory.
        format: Import format.
        overwrite: Overwrite existing files.
    """
    output = OutputFormatter()

    # Determine format if auto
    if format == "auto":
        suffix = input_file.suffix.lower()
        if suffix == ".json":
            format = "json"
        elif suffix in (".csv",):
            format = "csv"
        elif suffix in (".yaml", ".yml"):
            format = "yaml"
        else:
            output.error(f"Cannot determine format for file: {input_file}")
            raise typer.Exit(code=1)

    # Ensure project directory exists
    project_path.mkdir(parents=True, exist_ok=True)

    # Import data
    try:
        imported_data = {}
        if format == "json":
            import json

            with open(input_file) as f:
                imported_data = json.load(f)
        elif format == "csv":
            import csv

            with open(input_file, newline="") as f:
                reader = csv.DictReader(f)
                imported_data = list(reader)
        elif format == "yaml":
            import yaml

            with open(input_file) as f:
                imported_data = yaml.safe_load(f)
        else:
            output.error(f"Unsupported import format: {format}")
            raise typer.Exit(code=1)

        # Process imported data
        if isinstance(imported_data, dict):
            # Handle dictionary data (JSON, YAML)
            if imported_data.get("config"):
                config_file = project_path / ".env"
                if config_file.exists() and not overwrite:
                    output.warning(
                        f"Config file {config_file} already exists. Use --overwrite to replace."
                    )
                else:
                    with open(config_file, "w") as f:
                        f.write(imported_data["config"])
                    output.success(f"Config imported to {config_file}")

            if imported_data.get("logs"):
                log_dir = project_path / "logs"
                log_dir.mkdir(exist_ok=True)
                for log_name, log_content in imported_data["logs"].items():
                    log_file = log_dir / log_name
                    if log_file.exists() and not overwrite:
                        output.warning(
                            f"Log file {log_file} already exists. Use --overwrite to replace."
                        )
                    else:
                        with open(log_file, "w") as f:
                            f.write(log_content)
                        output.success(f"Log imported to {log_file}")

        elif isinstance(imported_data, list):
            # Handle list data (CSV)
            # For CSV, we'll create a generic import file
            import_file = project_path / f"{input_file.stem}_import.csv"
            if import_file.exists() and not overwrite:
                output.warning(
                    f"Import file {import_file} already exists. Use --overwrite to replace."
                )
            else:
                import csv

                with open(import_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    if imported_data:
                        writer.writerow(imported_data[0].keys())
                        for row in imported_data:
                            writer.writerow(row.values())
                output.success(f"Data imported to {import_file}")

        output.success(f"Data imported from {input_file}")
    except Exception as e:
        output.error(f"Failed to import data: {e}")
        raise typer.Exit(code=1)
