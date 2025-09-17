"""Module for creating new expert files from template."""

import os
import shutil


def create_expert_from_template(file_path: str) -> str:
    """
    Create a new expert file from template.

    Args:
        file_path: Path to the new expert file (with or without extension)

    Returns:
        Path to the created file
    """
    # Get the absolute path to the template file
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "template.py"
    )

    # Split the path into directory and filename
    output_dir, filename = os.path.split(file_path)

    # If no directory specified, use current directory
    if not output_dir:
        output_dir = "."

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Add .py extension if not provided
    if not filename.endswith(".py"):
        filename = f"{filename}.py"

    # Create the output file path
    output_path = os.path.join(output_dir, filename)

    # Copy the template file to the output path
    shutil.copy2(template_path, output_path)

    print(f"Created new expert file: {output_path}")
    return output_path
