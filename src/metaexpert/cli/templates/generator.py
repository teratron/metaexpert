"""Template generator for creating new MetaExpert projects from templates."""

import shutil
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, UndefinedError

from metaexpert.logger import get_logger as metaexpert_get_logger


class TemplateGenerator:
    """
    A class for generating projects from templates using Jinja2.

    This class handles the loading of templates, rendering them with context,
    copying static files, and creating project directory structures.
    """

    def __init__(self, template_dir: str = "src/metaexpert/cli/templates/files"):
        """
        Initialize the TemplateGenerator.

        Args:
            template_dir: Directory containing the template files.
        """
        self.logger = metaexpert_get_logger("metaexpert.cli.templates.generator")
        self.template_dir = Path(template_dir)
        self.environment = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_project(
        self,
        project_name: str,
        output_dir: str,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Generate a new project from templates.

        Args:
            project_name: Name of the project to create.
            output_dir: Directory where the project will be created.
            context: Context data to render the templates with.

        Returns:
            True if project generation was successful, False otherwise.
        """
        if context is None:
            context = {}

        # Add project name to context
        context["project_name"] = project_name

        output_path = Path(output_dir) / project_name

        try:
            self.logger.info(
                "Starting project generation",
                project=project_name,
                output_dir=str(output_path),
            )

            # Create output directory
            output_path.mkdir(parents=True, exist_ok=True)

            # Process template files
            success = self._process_templates(output_path, context)

            if success:
                self.logger.info(
                    "Project generation completed successfully", project=project_name
                )
                return True
            else:
                self.logger.error(
                    "Project generation failed during template processing",
                    project=project_name,
                )
                return False

        except Exception as e:
            self.logger.error(
                "Unexpected error during project generation",
                project=project_name,
                error=str(e),
                exc_info=True,
            )
            return False

    def _process_templates(self, output_path: Path, context: dict[str, Any]) -> bool:
        """
        Process all template files and render them to the output directory.

        Args:
            output_path: Path to the output directory.
            context: Context data for rendering templates.

        Returns:
            True if all templates were processed successfully, False otherwise.
        """
        try:
            # Get all template files
            template_files = list(self.template_dir.glob("**/*.j2"))

            for template_file in template_files:
                # Calculate relative path from template directory
                relative_path = template_file.relative_to(self.template_dir)

                # Remove .j2 extension for output file
                output_file_path = output_path / relative_path.with_suffix("")

                # Ensure parent directories exist
                output_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Render and write template
                success = self._render_template_to_file(
                    template_file, output_file_path, context
                )
                if not success:
                    return False

            # Copy any non-template static files if they exist
            self._copy_static_files(output_path)

            return True

        except Exception as e:
            self.logger.error("Error processing templates", error=str(e), exc_info=True)
            return False

    def _render_template_to_file(
        self, template_path: Path, output_path: Path, context: dict[str, Any]
    ) -> bool:
        """
        Render a single template file and write it to the output path.

        Args:
            template_path: Path to the template file.
            output_path: Path where the rendered file will be written.
            context: Context data for rendering the template.

        Returns:
            True if rendering was successful, False otherwise.
        """
        try:
            # Load the template
            template_name = str(template_path.relative_to(self.template_dir))
            template = self.environment.get_template(template_name)

            # Render the template with context
            rendered_content = template.render(**context)

            # Write the rendered content to the output file
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(rendered_content)

            self.logger.debug(
                "Rendered template", template=template_name, output=str(output_path)
            )

            return True

        except TemplateNotFound as e:
            self.logger.error("Template not found", template=str(e))
            return False

        except UndefinedError as e:
            self.logger.error(
                "Undefined variable in template",
                template=str(template_path),
                error=str(e),
            )
            return False

        except Exception as e:
            self.logger.error(
                "Error rendering template",
                template=str(template_path),
                output=str(output_path),
                error=str(e),
                exc_info=True,
            )
            return False

    def _copy_static_files(self, output_path: Path) -> bool:
        """
        Copy any static files that are not templates to the output directory.

        Args:
            output_path: Path to the output directory.

        Returns:
            True if copying was successful, False otherwise.
        """
        try:
            # Look for any non-template files in the template directory
            for item in self.template_dir.iterdir():
                if item.is_file() and not item.name.endswith(".j2"):
                    dest_path = output_path / item.name
                    shutil.copy2(item, dest_path)
                    self.logger.debug(
                        "Copied static file", file=item.name, destination=str(dest_path)
                    )

            # Also handle subdirectories that don't contain templates
            for subdir in self.template_dir.iterdir():
                if subdir.is_dir():
                    # Check if this subdirectory has any non-template files
                    non_template_files = [
                        f
                        for f in subdir.rglob("*")
                        if f.is_file() and not f.name.endswith(".j2")
                    ]
                    if non_template_files:
                        dest_subdir = output_path / subdir.name
                        dest_subdir.mkdir(exist_ok=True)
                        for file_path in non_template_files:
                            rel_path = file_path.relative_to(subdir)
                            dest_file_path = dest_subdir / rel_path
                            dest_file_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file_path, dest_file_path)
                            self.logger.debug(
                                "Copied static file from subdirectory",
                                file=str(rel_path),
                                destination=str(dest_file_path),
                            )

            return True

        except Exception as e:
            self.logger.error("Error copying static files", error=str(e), exc_info=True)
            return False

    def validate_template_exists(self, template_name: str) -> bool:
        """
        Check if a template exists.

        Args:
            template_name: Name of the template to check.

        Returns:
            True if template exists, False otherwise.
        """
        try:
            self.environment.get_template(template_name)
            return True
        except TemplateNotFound:
            return False

    def list_available_templates(self) -> list:
        """
        List all available templates.

        Returns:
            List of available template names.
        """
        try:
            # Find all .j2 files in the template directory
            templates = list(self.template_dir.glob("**/*.j2"))
            return [str(t.relative_to(self.template_dir)) for t in templates]
        except Exception as e:
            self.logger.error("Error listing templates", error=str(e), exc_info=True)
            return []
