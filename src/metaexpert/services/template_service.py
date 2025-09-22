"""Template creation service for generating new trading strategy templates."""

import os
import shutil
from datetime import datetime
from typing import Any

from metaexpert.models.configuration_parameter import ConfigurationParameter
from metaexpert.models.template_file import TemplateFile


class TemplateCreationService:
    """Service for creating and managing trading strategy templates."""

    def __init__(self, template_path: str | None = None) -> None:
        """Initialize the template creation service.

        Args:
            template_path: Path to the template file. If None, uses default.
        """
        if template_path is None:
            # Get the absolute path to the template file
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "template.py"
            )

        self.template_path = template_path
        self._template_file: TemplateFile | None = None

    def load_template(self) -> TemplateFile:
        """Load the template file.

        Returns:
            TemplateFile object representing the loaded template

        Raises:
            FileNotFoundError: If the template file doesn't exist
            OSError: If there's an error reading the template file
        """
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found: {self.template_path}")

        try:
            with open(self.template_path, encoding='utf-8') as f:
                content = f.read()

            # Get file modification time
            mod_time = os.path.getmtime(self.template_path)
            last_modified = datetime.fromtimestamp(mod_time)

            # Extract version from template (simplified - in reality would parse file)
            version = "1.0.0"  # Default version

            self._template_file = TemplateFile(
                path=self.template_path,
                content=content,
                version=version,
                last_modified=last_modified
            )

            return self._template_file
        except Exception as e:
            raise OSError(f"Error reading template file: {e}") from e

    def create_template(
        self,
        strategy_name: str,
        output_directory: str,
        parameters: dict[str, Any] | None = None
    ) -> str:
        """Create a new trading strategy template.

        Args:
            strategy_name: Name of the strategy
            output_directory: Directory where the template should be created
            parameters: Optional dictionary of parameters to customize the template

        Returns:
            Path to the created template file

        Raises:
            ValueError: If strategy_name is empty
            OSError: If there's an error creating the template
        """
        if not strategy_name:
            raise ValueError("Strategy name cannot be empty")

        # Load template if not already loaded
        if self._template_file is None:
            self.load_template()

        # Make sure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Create the output file path
        output_filename = f"{strategy_name}.py"
        output_path = os.path.join(output_directory, output_filename)

        try:
            # Copy the template file to the output path
            shutil.copy2(self.template_path, output_path)

            # If parameters were provided, customize the template
            if parameters:
                self._customize_template(output_path, parameters)

            return output_path
        except Exception as e:
            raise OSError(f"Error creating template: {e}") from e

    def _customize_template(self, template_path: str, parameters: dict[str, Any]) -> None:
        """Customize a template file with the provided parameters.

        Args:
            template_path: Path to the template file to customize
            parameters: Dictionary of parameters to apply
        """
        # This is a simplified implementation
        # In reality, this would parse the template and replace parameters
        pass

    def get_supported_exchanges(self) -> list:
        """Get a list of supported exchanges.

        Returns:
            List of supported exchange names
        """
        # Return a static list for now
        # In reality, this would be dynamically determined
        return ["binance", "bybit", "okx", "bitget", "kucoin"]

    def get_template_parameters(self) -> list:
        """Get a list of configurable template parameters.

        Returns:
            List of ConfigurationParameter objects
        """
        # Return a static list for now
        # In reality, this would parse the template to extract parameters
        return [
            ConfigurationParameter(
                name="exchange",
                description="Supported exchange for trading",
                default_value="binance",
                category="core",
                required=True,
                env_var_name="DEFAULT_EXCHANGE",
                cli_arg_name="--exchange"
            ),
            ConfigurationParameter(
                name="symbol",
                description="Trading pair symbol",
                default_value="BTCUSDT",
                category="core",
                required=True,
                env_var_name="DEFAULT_SYMBOL",
                cli_arg_name="--symbol"
            ),
            ConfigurationParameter(
                name="timeframe",
                description="Trading timeframe",
                default_value="1h",
                category="core",
                required=True,
                env_var_name="DEFAULT_TIMEFRAME",
                cli_arg_name="--timeframe"
            )
        ]
