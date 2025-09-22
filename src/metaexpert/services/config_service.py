"""Configuration management service for handling template parameters."""

import argparse
import os
from typing import Any

from metaexpert.models.configuration_parameter import ConfigurationParameter
from metaexpert.models.configuration_source import ConfigurationSource


class ConfigurationManagementService:
    """Service for managing configuration parameters across different sources."""

    def __init__(self, cli_args: argparse.Namespace | None = None) -> None:
        """Initialize the configuration management service.

        Args:
            cli_args: Optional parsed CLI arguments
        """
        self.sources: list[ConfigurationSource] = [
            ConfigurationSource(
                type="default",
                priority=0,
                description="Default values from template"
            ),
            ConfigurationSource(
                type="environment",
                priority=1,
                description="Environment variables"
            ),
            ConfigurationSource(
                type="cli",
                priority=2,
                description="Command-line arguments"
            )
        ]
        self.cli_args = cli_args

    def get_configuration_parameters(
        self,
        category: str | None = None,
        exchange: str | None = None
    ) -> list[ConfigurationParameter]:
        """Get configuration parameters, optionally filtered by category or exchange.

        Args:
            category: Optional category to filter by
            exchange: Optional exchange to filter by

        Returns:
            List of ConfigurationParameter objects
        """
        # Return a static list for now
        # In reality, this would be dynamically determined based on filters
        parameters = [
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
            ),
            ConfigurationParameter(
                name="api_key",
                description="API key for exchange authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="API_KEY",
                cli_arg_name="--api-key"
            ),
            ConfigurationParameter(
                name="api_secret",
                description="API secret for exchange authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="API_SECRET",
                cli_arg_name="--api-secret"
            ),
            ConfigurationParameter(
                name="binance_api_key",
                description="Binance API key for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="BINANCE_API_KEY",
                cli_arg_name="--binance-api-key"
            ),
            ConfigurationParameter(
                name="binance_api_secret",
                description="Binance API secret for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="BINANCE_API_SECRET",
                cli_arg_name="--binance-api-secret"
            ),
            ConfigurationParameter(
                name="bybit_api_key",
                description="Bybit API key for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="BYBIT_API_KEY",
                cli_arg_name="--bybit-api-key"
            ),
            ConfigurationParameter(
                name="bybit_api_secret",
                description="Bybit API secret for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="BYBIT_API_SECRET",
                cli_arg_name="--bybit-api-secret"
            ),
            ConfigurationParameter(
                name="okx_api_key",
                description="OKX API key for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="OKX_API_KEY",
                cli_arg_name="--okx-api-key"
            ),
            ConfigurationParameter(
                name="okx_api_secret",
                description="OKX API secret for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="OKX_API_SECRET",
                cli_arg_name="--okx-api-secret"
            ),
            ConfigurationParameter(
                name="okx_api_passphrase",
                description="OKX API passphrase for authentication",
                default_value="",
                category="api",
                required=False,
                env_var_name="OKX_API_PASSPHRASE",
                cli_arg_name="--okx-api-passphrase"
            )
        ]

        # Apply filters if provided
        if category:
            parameters = [p for p in parameters if p.category == category]

        if exchange:
            # In reality, this would filter for exchange-specific parameters
            pass

        return parameters

    def validate_configuration(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Validate a set of configuration parameters.

        Args:
            parameters: Dictionary of parameter names and values

        Returns:
            Dictionary with validation results
        """
        # Get all configuration parameters
        config_params = self.get_configuration_parameters()
        param_dict = {p.name: p for p in config_params}

        # Check for required parameters
        errors = []
        for param in config_params:
            if param.required and param.name not in parameters:
                errors.append({
                    "parameter": param.name,
                    "error": f"Required parameter '{param.name}' is missing"
                })

        # Validate parameter values
        for name, value in parameters.items():
            if name in param_dict:
                param = param_dict[name]
                # Add more validation logic here as needed
                if param.name == "exchange" and value not in ["binance", "bybit", "okx", "bitget", "kucoin"]:
                    errors.append({
                        "parameter": param.name,
                        "error": f"Invalid exchange '{value}'. Must be one of: binance, bybit, okx, bitget, kucoin"
                    })

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def get_parameter_value(
        self,
        parameter_name: str,
        default_value: str | None = None
    ) -> str | None:
        """Get the value of a parameter from the highest priority source.

        Args:
            parameter_name: Name of the parameter to get
            default_value: Default value if not found in any source

        Returns:
            Value of the parameter or None if not found
        """
        # Check CLI arguments (highest priority)
        if self.cli_args and hasattr(self.cli_args, parameter_name):
            cli_value = getattr(self.cli_args, parameter_name)
            if cli_value is not None:
                return cli_value

        # Check environment variables (medium priority)
        env_var_name = self._get_env_var_name(parameter_name)
        if env_var_name and env_var_name in os.environ:
            return os.environ[env_var_name]

        # Return default value (lowest priority)
        return default_value

    def _get_env_var_name(self, parameter_name: str) -> str | None:
        """Get the environment variable name for a parameter.

        Args:
            parameter_name: Name of the parameter

        Returns:
            Environment variable name or None if not found
        """
        # In reality, this would look up the mapping from parameter to env var
        # This is a simplified implementation
        env_var_mapping = {
            "exchange": "DEFAULT_EXCHANGE",
            "symbol": "DEFAULT_SYMBOL",
            "timeframe": "DEFAULT_TIMEFRAME",
            "api_key": "API_KEY",
            "api_secret": "API_SECRET",
            "binance_api_key": "BINANCE_API_KEY",
            "binance_api_secret": "BINANCE_API_SECRET",
            "bybit_api_key": "BYBIT_API_KEY",
            "bybit_api_secret": "BYBIT_API_SECRET",
            "okx_api_key": "OKX_API_KEY",
            "okx_api_secret": "OKX_API_SECRET",
            "okx_api_passphrase": "OKX_API_PASSPHRASE",
            "bitget_api_key": "BITGET_API_KEY",
            "bitget_api_secret": "BITGET_API_SECRET",
            "kucoin_api_key": "KUCOIN_API_KEY",
            "kucoin_api_secret": "KUCOIN_API_SECRET",
            "kucoin_api_passphrase": "KUCOIN_API_PASSPHRASE"
        }

        return env_var_mapping.get(parameter_name)

    def align_configuration_sources(self) -> dict[str, Any]:
        """Align configuration parameters across different sources.

        Returns:
            Dictionary with alignment results
        """
        # Get all configuration parameters
        parameters = self.get_configuration_parameters()

        # Check alignment between template, environment, and CLI
        alignment_issues = []

        for param in parameters:
            # Check that env_var_name is properly set
            if param.env_var_name is None and param.category == "api":
                alignment_issues.append(f"Parameter {param.name} missing environment variable name")

            # Check that cli_arg_name is properly set
            if param.cli_arg_name is None:
                alignment_issues.append(f"Parameter {param.name} missing CLI argument name")

        return {
            "aligned": len(alignment_issues) == 0,
            "issues": alignment_issues
        }

    def get_configuration_with_priority(self) -> dict[str, Any]:
        """Get all configuration parameters with proper priority handling.

        Returns:
            Dictionary of configuration parameters with values
        """
        # Get all configuration parameters
        parameters = self.get_configuration_parameters()

        # Build configuration dictionary with priority handling
        config = {}

        for param in parameters:
            value = self.get_parameter_value(param.name, param.default_value)
            if value is not None:
                config[param.name] = value

        return config
