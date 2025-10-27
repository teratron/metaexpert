"""Dependency Injection container for CLI services."""

from typing import Any, Callable, Dict, Generic, Type, TypeVar

T = TypeVar("T")


class DIContainer:
    """Simple DI container for CLI services."""

    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}

    def register(self, interface: Type[T], factory: Callable[..., T], singleton: bool = True) -> None:
        """
        Register service factory.

        Args:
            interface: Interface type to register
            factory: Factory function to create the service
            singleton: Whether to create a single instance (default: True)
        """
        if singleton:
            self._factories[interface] = factory
        else:
            self._services[interface] = factory

    def get(self, interface: Type[T]) -> T:
        """
        Get service instance.

        Args:
            interface: Interface type to retrieve

        Returns:
            Service instance
        """
        # Check singleton cache first
        if interface in self._singletons:
            return self._singletons[interface]

        # Create via factory if registered
        factory = self._factories.get(interface)
        if factory:
            instance = factory()
            self._singletons[interface] = instance
            return instance

        # Create via non-singleton service if registered
        service = self._services.get(interface)
        if service:
            return service()

        raise ValueError(f"Service {interface.__name__} not registered")


# Global container instance
_container = DIContainer()


def get_container() -> DIContainer:
    """Get DI container instance."""
    return _container


# Example registration (these would typically be done in a startup/config file)
# _container.register(CLIConfig, lambda: CLIConfig.load(), singleton=True)
# _container.register(OutputFormatter, lambda: OutputFormatter(), singleton=True)
# _container.register(ProcessManager, lambda: ProcessManager(), singleton=True)
# _container.register(TemplateGenerator, lambda: TemplateGenerator(), singleton=True)