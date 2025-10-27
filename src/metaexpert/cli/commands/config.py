"""Config command for CLI."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.output import OutputFormatter


def cmd_config(
    key: Annotated[
        Optional[str],
        typer.Argument(help="Configuration key to get/set"),
    ] = None,
    value: Annotated[
        Optional[str],
        typer.Option("--set", "-s", help="Value to set for the key"),
    ] = None,
    profile: Annotated[
        Optional[str],
        typer.Option("--profile", "-p", help="Profile to use"),
    ] = None,
) -> None:
    """
    Manage CLI configuration.

    Args:
        key: Configuration key to get/set.
        value: Value to set for the key.
        profile: Profile to use.
    """
    output = OutputFormatter()
    config = CLIConfig.load(profile=profile)

    if key is None:
        # Display all configuration
        data = []
        for field_name, field_info in CLIConfig.model_fields.items():
            data.append(
                {
                    "Key": field_name,
                    "Value": str(getattr(config, field_name)),
                    "Description": field_info.description or "",
                }
            )

        output.custom_table(
            data,
            columns=["Key", "Value", "Description"],
            title=f"CLI Configuration (Profile: {config.profile})",
        )
    elif value is None:
        # Display specific key
        if hasattr(config, key):
            output.info(f"{key}: {getattr(config, key)}")
        else:
            output.error(f"Unknown configuration key: {key}")
            raise typer.Exit(code=1)
    else:
        # Set key-value pair
        if hasattr(config, key):
            # Convert value to the correct type
            field_info = CLIConfig.model_fields[key]
            try:
                if field_info.annotation == bool:
                    converted_value = value.lower() in ("true", "1", "yes", "on")
                elif field_info.annotation == int:
                    converted_value = int(value)
                elif field_info.annotation == float:
                    converted_value = float(value)
                elif field_info.annotation == Path:
                    converted_value = Path(value)
                else:
                    converted_value = value

                setattr(config, key, converted_value)
                config.save()
                output.success(f"Configuration updated: {key} = {converted_value}")
            except ValueError as e:
                output.error(f"Invalid value for {key}: {e}")
                raise typer.Exit(code=1)
        else:
            output.error(f"Unknown configuration key: {key}")
            raise typer.Exit(code=1)