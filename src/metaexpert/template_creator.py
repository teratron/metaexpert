"""Module for creating new expert files from template."""

from typing import Any

from metaexpert.logger import get_logger
from metaexpert.services.template_service import TemplateCreationService

# Get the logger instance
logger = get_logger("metaexpert.template_creator")


def create_expert_from_template(
    file_path: str, parameters: dict[str, Any] | None = None
) -> str:
    """
    Create a new expert file from template.

    Args:
        file_path: Path to the new expert file (with or without extension)
        parameters: Optional dictionary of parameters to customize the template

    Returns:
        Path to the created file
    """
    # Split the path into directory and filename
    output_dir, filename = (
        file_path.rsplit("/", 1) if "/" in file_path else (".", file_path)
    )

    # Extract strategy name (remove .py extension if present)
    strategy_name = filename[:-3] if filename.endswith(".py") else filename

    # Create template service
    template_service = TemplateCreationService()

    # Create the template
    output_path = template_service.create_template(
        strategy_name=strategy_name,
        output_directory=output_dir,
        parameters=parameters
    )

    logger.info(f"Created new expert file: {output_path}")
    return output_path
