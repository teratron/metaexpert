# Extending MetaExpert CLI

This document explains how to extend the MetaExpert CLI with custom commands, middleware, and plugins.

## Table of Contents

1. [Custom Commands](#custom-commands)
2. [Middleware](#middleware)
3. [Plugins](#plugins)
4. [Event Bus](#event-bus)
5. [Dependency Injection](#dependency-injection)

## Custom Commands

MetaExpert CLI allows you to add custom commands to extend its functionality.

### Creating a Custom Command

1. Create a new Python file in the `src/metaexpert/cli/commands` directory (or in a custom directory if you're building a plugin).

2. Define your command function using Typer decorators:

```python
# src/metaexpert/cli/commands/my_command.py
from typing import Annotated
import typer

from metaexpert.cli.core.output import OutputFormatter

def cmd_my_command(
    argument: Annotated[str, typer.Argument(help="An argument for the command")],
    option: Annotated[str, typer.Option("--option", "-o", help="An option for the command")] = "default",
) -> None:
    """
    A custom command.
    
    Args:
        argument: An argument for the command.
        option: An option for the command.
    """
    output = OutputFormatter()
    output.info(f"Argument: {argument}")
    output.info(f"Option: {option}")
```

3. Register the command in `src/metaexpert/cli/__init__.py`:

```python
# src/metaexpert/cli/__init__.py
def register_commands() -> None:
    """Register all CLI commands."""
    # ... existing imports ...
    from metaexpert.cli.commands import my_command
    
    # ... existing registrations ...
    app.command(name="my-command")(my_command.cmd_my_command)
```

### Command Structure

All custom commands should follow this structure:

- Use `Annotated` for type hints with Typer metadata.
- Use `OutputFormatter` for consistent output.
- Handle errors gracefully using `typer.Exit(code=1)`.
- Include comprehensive docstrings.

## Middleware

Middleware allows you to intercept and modify command execution.

### Creating Middleware

1. Create a new Python file for your middleware:

```python
# src/metaexpert/cli/core/middleware/my_middleware.py
from metaexpert.cli.core.middleware import Middleware

class MyMiddleware(Middleware):
    """Custom middleware for CLI commands."""
    
    def before(self, command_name: str, **kwargs) -> None:
        """
        Execute before command.
        
        Args:
            command_name: Name of the command being executed.
            **kwargs: Command arguments.
        """
        # Add your pre-execution logic here
        print(f"Before executing {command_name}")
    
    def after(self, command_name: str, result: Any) -> None:
        """
        Execute after command.
        
        Args:
            command_name: Name of the command that was executed.
            result: Command execution result (or exception if it occurred).
        """
        # Add your post-execution logic here
        print(f"After executing {command_name}")
```

2. Register the middleware in your application's startup code:

```python
# In your app initialization code
from metaexpert.cli.core.middleware import get_middleware_manager
from metaexpert.cli.core.middleware.my_middleware import MyMiddleware

middleware_manager = get_middleware_manager()
middleware_manager.register(MyMiddleware())
```

### Built-in Middleware

MetaExpert CLI comes with several built-in middleware:

- `PerformanceMiddleware`: Tracks command execution time.
- `ErrorRecoveryMiddleware`: Handles errors gracefully.

## Plugins

Plugins are a more advanced way to extend the CLI, allowing you to add commands, middleware, and other functionality.

### Creating a Plugin

1. Create a new Python file for your plugin:

```python
# plugins/my_plugin.py
from metaexpert.cli.core.plugins import CliPlugin
from metaexpert.cli.core.middleware import MiddlewareManager
from typer import Typer

class MyPlugin(CliPlugin):
    """A custom plugin for MetaExpert CLI."""
    
    name = "my-plugin"
    version = "1.0.0"
    description = "A custom plugin for MetaExpert CLI."
    
    def register_commands(self, app: Typer) -> None:
        """
        Register custom commands.
        
        Args:
            app: Typer application instance.
        """
        @app.command()
        def my_plugin_command():
            """A command added by the plugin."""
            print("Hello from my plugin!")
    
    def register_middleware(self, manager: MiddlewareManager) -> None:
        """
        Register middleware.
        
        Args:
            manager: Middleware manager instance.
        """
        # Register any middleware provided by the plugin
        pass
```

2. Place the plugin file in the `plugins` directory (you may need to create this directory).

3. The plugin will be automatically loaded when the CLI starts.

### Plugin Structure

A plugin must:

- Inherit from `CliPlugin`.
- Define `name`, `version`, and `description` attributes.
- Implement `register_commands` and `register_middleware` methods.

## Event Bus

The Event Bus allows different parts of the CLI to communicate with each other.

### Publishing Events

To publish an event:

```python
from metaexpert.cli.core.events import get_event_bus, Event, EventType

event_bus = get_event_bus()
event = Event(type=EventType.COMMAND_START, data={"command": "my-command"})
event_bus.publish(event)
```

### Subscribing to Events

To subscribe to an event:

```python
from metaexpert.cli.core.events import get_event_bus, EventType

def my_event_handler(event):
    """Handle the event."""
    print(f"Received event: {event.type}")

event_bus = get_event_bus()
event_bus.subscribe(EventType.COMMAND_START, my_event_handler)
```

### Built-in Events

MetaExpert CLI defines several built-in events:

- `COMMAND_START`: Fired when a command starts.
- `COMMAND_END`: Fired when a command ends.
- `COMMAND_ERROR`: Fired when a command encounters an error.
- `PROCESS_START`: Fired when a process starts.
- `PROCESS_STOP`: Fired when a process stops.
- `CONFIG_CHANGED`: Fired when the configuration changes.

## Dependency Injection

MetaExpert CLI uses a simple DI container to manage dependencies.

### Registering Services

To register a service:

```python
from metaexpert.cli.core.container import get_container

container = get_container()
container.register(MyServiceInterface, lambda: MyServiceImpl(), singleton=True)
```

### Getting Services

To get a service:

```python
from metaexpert.cli.core.container import get_container

container = get_container()
service = container.get(MyServiceInterface)
```

### Service Lifecycles

Services can be registered as singletons (one instance shared across the application) or transient (a new instance created each time).

```python
# Singleton (default)
container.register(MyServiceInterface, lambda: MyServiceImpl(), singleton=True)

# Transient
container.register(MyServiceInterface, lambda: MyServiceImpl(), singleton=False)