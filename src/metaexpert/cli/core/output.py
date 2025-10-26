"""
Output formatting module for MetaExpert CLI using Rich.

This module provides classes and functions for formatting CLI output
with rich text, tables, JSON, trees, and progress indicators.
"""

from typing import Any

import yaml
from rich.box import ROUNDED
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

# Create global console instances
console = Console()
error_console = Console(stderr=True)


class OutputFormatter:
    """
    A comprehensive output formatter using Rich for CLI applications.
    Provides methods for different types of output including messages,
    tables, JSON, trees, and progress indicators.
    """

    def __init__(self, console: Console | None = None):
        """
        Initialize the OutputFormatter.

        Args:
            console: Optional Rich Console instance. If not provided, a default console will be used.
        """
        self.console = console or Console()

    def success(self, message: str, title: str | None = None) -> None:
        """
        Display a success message.

        Args:
            message: The success message to display
            title: Optional title for the panel
        """
        panel = Panel(
            Text(message, style="green"),
            title=title or "Success",
            border_style="green",
            box=ROUNDED,
        )
        self.console.print(panel)

    def error(self, message: str, title: str | None = None) -> None:
        """
        Display an error message.

        Args:
            message: The error message to display
            title: Optional title for the panel
        """
        panel = Panel(
            Text(message, style="red"),
            title=title or "Error",
            border_style="red",
            box=ROUNDED,
        )
        self.console.print(panel)

    def warning(self, message: str, title: str | None = None) -> None:
        """
        Display a warning message.

        Args:
            message: The warning message to display
            title: Optional title for the panel
        """
        panel = Panel(
            Text(message, style="yellow"),
            title=title or "Warning",
            border_style="yellow",
            box=ROUNDED,
        )
        self.console.print(panel)

    def info(self, message: str, title: str | None = None) -> None:
        """
        Display an informational message.

        Args:
            message: The informational message to display
            title: Optional title for the panel
        """
        panel = Panel(
            Text(message, style="blue"),
            title=title or "Info",
            border_style="blue",
            box=ROUNDED,
        )
        self.console.print(panel)

    def table(
        self,
        headers: list[str],
        rows: list[list[Any]],
        title: str | None = None,
        show_header: bool = True,
        header_style: str = "bold magenta",
    ) -> None:
        """
        Display data in a table format.

        Args:
            headers: List of column headers
            rows: List of row data
            title: Optional title for the table
            show_header: Whether to show the header row
            header_style: Style for the header row
        """
        table = Table(title=title, show_header=show_header, header_style=header_style)

        for header in headers:
            table.add_column(header)

        for row in rows:
            table.add_row(*[str(item) for item in row])

        self.console.print(table)

    def json_output(self, data: dict | list | Any, title: str | None = None) -> None:
        """
        Display JSON data in a formatted way.

        Args:
            data: The data to display as JSON
            title: Optional title for the JSON panel
        """
        json_text = JSON.from_data(data)
        if title:
            panel = Panel(json_text, title=title, border_style="cyan")
            self.console.print(panel)
        else:
            self.console.print(json_text)

    def tree(
        self,
        root_label: str,
        children: list[str | dict[str, Any]],
        title: str | None = None,
    ) -> None:
        """
        Display data in a tree format.

        Args:
            root_label: The label for the root node
            children: List of child nodes (strings or dictionaries)
            title: Optional title for the tree panel
        """
        tree = Tree(root_label)

        for child in children:
            if isinstance(child, str):
                tree.add(child)
            elif isinstance(child, dict):
                for key, value in child.items():
                    branch = tree.add(f"{key}")
                    if isinstance(value, (list, tuple)):
                        for item in value:
                            branch.add(str(item))
                    else:
                        branch.add(str(value))

        if title:
            panel = Panel(tree, title=title, border_style="green")
            self.console.print(panel)
        else:
            self.console.print(tree)

    def progress(
        self, tasks: list[dict[str, Any]], description: str = "Processing..."
    ) -> None:
        """
        Display a progress indicator for multiple tasks.

        Args:
            tasks: List of tasks, each with 'name' and 'work' keys
                   where 'work' is a callable that takes the progress instance
            description: Description text for the progress indicator
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console,
        ) as progress:
            task_id = progress.add_task(description, total=len(tasks))

            for i, task in enumerate(tasks):
                progress.update(
                    task_id,
                    description=f"{description} {task.get('name', f'Task {i + 1}')}",
                )
                if "work" in task and callable(task["work"]):
                    task["work"](progress)
                progress.update(task_id, advance=1)

    def custom_table(
        self,
        data: list[dict[str, Any]],
        columns: list[str] | None = None,
        title: str | None = None,
    ) -> None:
        """
        Display a custom table from a list of dictionaries.

        Args:
            data: List of dictionaries representing rows
            columns: Optional list of columns to display (if None, uses all keys from first dict)
            title: Optional title for the table
        """
        if not data:
            self.info("No data to display", title="Empty Table")
            return

        if columns is None:
            columns = list(data[0].keys())

        table = Table(title=title, show_header=True, header_style="bold magenta")

        for col in columns:
            table.add_column(col)

        for row in data:
            table.add_row(*[str(row.get(col, "")) for col in columns])

        self.console.print(table)

    def display_table(
        self,
        data: list[dict[str, Any]],
        columns: list[str] | None = None,
        title: str | None = None,
    ) -> None:
        """
        Display data as table using custom_table method.

        Args:
            data: List of dictionaries representing rows
            columns: Optional list of columns to display
            title: Optional title for the table
        """
        self.custom_table(data, columns=columns, title=title)

    def display_json(self, data: Any, title: str | None = None) -> None:
        """
        Display data as JSON using json_output method.

        Args:
            data: The data to display as JSON
            title: Optional title for the JSON panel
        """
        self.json_output(data, title=title)

    def display_yaml(self, data: Any) -> None:
        """
        Display data as YAML.

        Args:
            data: The data to display as YAML
        """
        yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        syntax = Syntax(yaml_str, "yaml", theme="monokai")
        self.console.print(syntax)


# Global instance for convenience
_default_formatter = OutputFormatter()


def success(message: str, title: str | None = None) -> None:
    """Display a success message using the default formatter."""
    _default_formatter.success(message, title)


def error(message: str, title: str | None = None) -> None:
    """Display an error message using the default formatter."""
    _default_formatter.error(message, title)


def warning(message: str, title: str | None = None) -> None:
    """Display a warning message using the default formatter."""
    _default_formatter.warning(message, title)


def info(message: str, title: str | None = None) -> None:
    """Display an informational message using the default formatter."""
    _default_formatter.info(message, title)


def table(headers: list[str], rows: list[list[Any]], title: str | None = None) -> None:
    """Display data in a table format using the default formatter."""
    _default_formatter.table(headers, rows, title)


def json_output(data: dict | list | Any, title: str | None = None) -> None:
    """Display JSON data in a formatted way using the default formatter."""
    _default_formatter.json_output(data, title=title)


def tree(
    root_label: str, children: list[str | dict[str, Any]], title: str | None = None
) -> None:
    """Display data in a tree format using the default formatter."""
    _default_formatter.tree(root_label, children, title=title)


def progress(tasks: list[dict[str, Any]], description: str = "Processing...") -> None:
    """Display a progress indicator using the default formatter."""
    _default_formatter.progress(tasks, description=description)


def custom_table(
    data: list[dict[str, Any]],
    columns: list[str] | None = None,
    title: str | None = None,
) -> None:
    """Display a custom table from a list of dictionaries using the default formatter."""
    _default_formatter.custom_table(data, columns=columns, title=title)
