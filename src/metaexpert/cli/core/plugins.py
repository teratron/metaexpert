"""Plugin system for CLI applications."""

import importlib
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typer import Typer

    from metaexpert.cli.core.middleware import MiddlewareManager

from metaexpert.logger import get_logger


class CliPlugin(ABC):
    """Base class for CLI plugins."""

    name: str
    version: str
    description: str

    @abstractmethod
    def register_commands(self, app: "Typer") -> None:
        """
        Register custom commands.

        Args:
            app: Typer application instance
        """
        pass

    @abstractmethod
    def register_middleware(self, manager: "MiddlewareManager") -> None:
        """
        Register middleware.

        Args:
            manager: Middleware manager instance
        """
        pass


class PluginManager:
    """Manage CLI plugins."""

    def __init__(self):
        self.plugins: dict[str, CliPlugin] = {}
        self.logger = get_logger(__name__)

    def load_plugins(self, plugin_dir: Path) -> None:
        """
        Load plugins from directory.

        Args:
            plugin_dir: Directory containing plugin modules
        """
        if not plugin_dir.exists():
            self.logger.info(f"Plugin directory does not exist: {plugin_dir}")
            return

        # Add the plugin directory to sys.path temporarily
        original_path = list(sys.path)
        sys.path.insert(0, str(plugin_dir))

        try:
            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.name.startswith("__"):
                    continue

                try:
                    # Import the module dynamically
                    module_name = plugin_file.stem
                    module = importlib.import_module(module_name)

                    # Look for classes that inherit from CliPlugin
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, CliPlugin)
                            and attr is not CliPlugin
                        ):
                            plugin_instance = attr()
                            self.plugins[plugin_instance.name] = plugin_instance
                            self.logger.info(
                                f"Loaded plugin: {plugin_instance.name} v{plugin_instance.version}",
                                plugin_name=plugin_instance.name,
                                plugin_version=plugin_instance.version,
                                plugin_description=plugin_instance.description,
                            )

                except ImportError as e:
                    self.logger.error(
                        f"Failed to import plugin module {plugin_file.name}: {e}",
                        plugin_file=str(plugin_file),
                        error=str(e),
                    )
                except Exception as e:
                    self.logger.error(
                        f"Failed to load plugin from {plugin_file.name}: {e}",
                        plugin_file=str(plugin_file),
                        error=str(e),
                    )
        finally:
            # Restore the original path
            sys.path[:] = original_path

    def register_all(self, app: "Typer", middleware: "MiddlewareManager") -> None:
        """
        Register all loaded plugins.

        Args:
            app: Typer application instance
            middleware: Middleware manager instance
        """
        for plugin in self.plugins.values():
            self.logger.debug(
                f"Registering plugin commands: {plugin.name}",
                plugin_name=plugin.name,
            )
            plugin.register_commands(app)

            self.logger.debug(
                f"Registering plugin middleware: {plugin.name}",
                plugin_name=plugin.name,
            )
            plugin.register_middleware(middleware)
