"""Export command for CLI."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.output import OutputFormatter


def cmd_export(
    project_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the project directory",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
    output_file: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output file path (default: project_name_export.<format>)",
        ),
    ] = None,
    format: Annotated[
        str,
        typer.Option("--format", "-f", help="Export format (json, csv, yaml)"),
    ] = "json",
    include_logs: Annotated[
        bool, typer.Option("--include-logs", "-l", help="Include log files")
    ] = False,
    include_config: Annotated[
        bool, typer.Option("--include-config", "-c", help="Include config files")
    ] = True,
) -> None:
    """
    Export project data.

    Args:
        project_path: Path to the project directory.
        output_file: Output file path.
        format: Export format.
        include_logs: Include log files.
        include_config: Include config files.
    """
    output = OutputFormatter()

    # Determine output file name
    if output_file is None:
        output_file = project_path / f"{project_path.name}_export.{format}"
    else:
        # Ensure output file has correct extension
        if not output_file.suffix:
            output_file = output_file.with_suffix(f".{format}")

    # Collect data to export
    export_data = {
        "project_name": project_path.name,
        "export_timestamp": __import__("datetime").datetime.now().isoformat(),
    }

    if include_config:
        config_file = project_path / ".env"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    export_data["config"] = f.read()
            except Exception as e:
                output.error(f"Failed to read config file: {e}")

    if include_logs:
        log_dir = project_path / "logs"
        if log_dir.exists():
            export_data["logs"] = {}
            for log_file in log_dir.glob("*.log"):
                try:
                    with open(log_file) as f:
                        export_data["logs"][log_file.name] = f.read()
                except Exception as e:
                    output.error(f"Failed to read log file {log_file}: {e}")

    # Export data
    try:
        if format == "json":
            import json

            with open(output_file, "w") as f:
                json.dump(export_data, f, indent=2)
        elif format == "csv":
            import csv

            # Flatten data for CSV export
            flat_data = []
            for key, value in export_data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flat_data.append([f"{key}.{sub_key}", str(sub_value)])
                else:
                    flat_data.append([key, str(value)])

            with open(output_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Key", "Value"])
                writer.writerows(flat_data)
        elif format == "yaml":
            import yaml

            with open(output_file, "w") as f:
                yaml.dump(export_data, f, default_flow_style=False)
        else:
            output.error(f"Unsupported export format: {format}")
            raise typer.Exit(code=1)

        output.success(f"Data exported to {output_file}")
    except Exception as e:
        output.error(f"Failed to export data: {e}")
        raise typer.Exit(code=1)
