# src/metaexpert/cli/core/output.py
"""Output formatting and display utilities."""

from enum import Enum
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

# Global console instances
console = Console()
error_console = Console(stderr=True, style="bold red")


class OutputFormat(str, Enum):
    """Available output formats."""

    TABLE = "table"
    JSON = "json"
    YAML = "yaml"
    TREE = "tree"


class OutputFormatter:
    """Handles output formatting for different data types."""

    def __init__(self, format: OutputFormat = OutputFormat.TABLE):
        self.format = format

    def display_table(
        self,
        data: List[Dict[str, Any]],
        title: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ) -> None:
        """Display data as a table."""
        if not data:
            console.print("[yellow]No data to display[/]")
            return

        if columns is None:
            columns = list(data[0].keys())

        table = Table(title=title, show_header=True, header_style="bold magenta")

        for col in columns:
            table.add_column(col, style="cyan")

        for row in data:
            table.add_row(*[str(row.get(col, "")) for col in columns])

        console.print(table)

    def display_tree(self, data: Dict[str, Any], root_label: str = "Root") -> None:
        """Display hierarchical data as a tree."""
        tree = Tree(root_label)
        self._build_tree(tree, data)
        console.print(tree)

    def _build_tree(self, tree: Tree, data: Dict[str, Any]) -> None:
        """Recursively build tree structure."""
        for key, value in data.items():
            if isinstance(value, dict):
                branch = tree.add(f"[bold]{key}[/]")
                self._build_tree(branch, value)
            elif isinstance(value, list):
                branch = tree.add(f"[bold]{key}[/]")
                for item in value:
                    if isinstance(item, dict):
                        self._build_tree(branch, item)
                    else:
                        branch.add(str(item))
            else:
                tree.add(f"[cyan]{key}:[/] {value}")

    def display_json(self, data: Any) -> None:
        """Display data as JSON."""
        import json

        console.print_json(json.dumps(data, indent=2))

    def display_yaml(self, data: Any) -> None:
        """Display data as YAML."""
        try:
            import yaml

            console.print(yaml.dump(data, default_flow_style=False))
        except ImportError:
            console.print("[yellow]YAML output requires PyYAML package[/]")
            self.display_json(data)

    def success(self, message: str) -> None:
        """Display success message."""
        console.print(f"[green]✓[/] {message}")

    def error(self, message: str) -> None:
        """Display error message."""
        error_console.print(f"[red]✗[/] {message}")

    def warning(self, message: str) -> None:
        """Display warning message."""
        console.print(f"[yellow]⚠[/] {message}")

    def info(self, message: str) -> None:
        """Display info message."""
        console.print(f"[blue]ℹ[/] {message}")

    def panel(self, content: str, title: Optional[str] = None) -> None:
        """Display content in a panel."""
        console.print(Panel(content, title=title, border_style="green"))


def progress_context(description: str = "Processing..."):
    """Context manager for progress display."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )
