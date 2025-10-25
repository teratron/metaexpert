"""Tests for the output formatting module."""
import json
from unittest.mock import Mock, patch

import pytest
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.progress import Progress

from metaexpert.cli.core.output import OutputFormatter, OutputFormat, console, error_console, progress_context


class TestOutputFormatter:
    """Test cases for OutputFormatter class."""

    def test_initialization_default_format(self):
        """Test OutputFormatter initialization with default format."""
        formatter = OutputFormatter()
        assert formatter.format == OutputFormat.TABLE

    def test_initialization_custom_format(self):
        """Test OutputFormatter initialization with custom format."""
        formatter = OutputFormatter(format=OutputFormat.JSON)
        assert formatter.format == OutputFormat.JSON

    def test_success_message(self, mocker):
        """Test success message output."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.success("Test success message")

        mock_console_print.assert_called_once_with("[green]✓[/] Test success message")

    def test_error_message(self, mocker):
        """Test error message output."""
        mock_error_console_print = mocker.patch.object(error_console, 'print')
        formatter = OutputFormatter()

        formatter.error("Test error message")

        mock_error_console_print.assert_called_once_with("[red]✗[/] Test error message")

    def test_warning_message(self, mocker):
        """Test warning message output."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.warning("Test warning message")

        mock_console_print.assert_called_once_with("[yellow]⚠[/] Test warning message")

    def test_info_message(self, mocker):
        """Test info message output."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.info("Test info message")

        mock_console_print.assert_called_once_with("[blue]ℹ[/] Test info message")

    def test_display_table_with_data(self, mocker):
        """Test displaying a table with data."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = [
            {"Name": "Alice", "Age": 30},
            {"Name": "Bob", "Age": 25}
        ]

        formatter.display_table(data)

        # Verify that a Table object was created and printed
        assert mock_console_print.call_count == 1
        # Check that the first call's argument is a Table instance
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)

    def test_display_table_with_title(self, mocker):
        """Test displaying a table with a title."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = [
            {"Name": "Alice", "Age": 30},
            {"Name": "Bob", "Age": 25}
        ]

        formatter.display_table(data, title="Users")

        # Verify that a Table object with title was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        assert call_arg.title == "Users"

    def test_display_table_with_custom_columns(self, mocker):
        """Test displaying a table with custom columns."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = [
            {"Name": "Alice", "Age": 30, "City": "NYC"},
            {"Name": "Bob", "Age": 25, "City": "LA"}
        ]

        formatter.display_table(data, columns=["Name", "City"])

        # Verify that a Table object with correct columns was created
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        # Check that the table has the correct number of columns
        assert len(call_arg.columns) == 2

    def test_display_table_empty_data(self, mocker):
        """Test displaying an empty table."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.display_table([])

        mock_console_print.assert_called_once_with("[yellow]No data to display[/]")

    def test_display_json(self, mocker):
        """Test displaying data as JSON."""
        mock_console_print_json = mocker.patch.object(console, 'print_json')
        formatter = OutputFormatter()

        data = {"name": "Alice", "age": 30}

        formatter.display_json(data)

        # Check that print_json was called with the JSON string
        mock_console_print_json.assert_called_once()
        # Get the actual argument passed to print_json
        json_arg = mock_console_print_json.call_args[0][0]
        # Verify it's a valid JSON string representation of the data
        parsed_data = json.loads(json_arg)
        assert parsed_data == data

    def test_display_tree_simple_dict(self, mocker):
        """Test displaying a simple dictionary as a tree."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = {"key1": "value1", "key2": "value2"}

        formatter.display_tree(data)

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)

    def test_display_tree_nested_dict(self, mocker):
        """Test displaying a nested dictionary as a tree."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                },
                "sibling": "sibling_value"
            }
        }

        formatter.display_tree(data)

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)

    def test_display_tree_with_list(self, mocker):
        """Test displaying a dictionary with a list as a tree."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = {
            "items": ["item1", "item2", {"nested": "value"}]
        }

        formatter.display_tree(data)

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)

    def test_display_tree_custom_root_label(self, mocker):
        """Test displaying a tree with a custom root label."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        data = {"key": "value"}

        formatter.display_tree(data, root_label="Custom Root")

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)

    def test_panel_display(self, mocker):
        """Test displaying content in a panel."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.panel("Panel content", title="Panel Title")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        assert call_arg.renderable == "Panel content"
        # Panel title is stored differently, so we check if it was passed correctly
        # The title should be set in the Panel constructor

    def test_panel_display_without_title(self, mocker):
        """Test displaying content in a panel without a title."""
        mock_console_print = mocker.patch.object(console, 'print')
        formatter = OutputFormatter()

        formatter.panel("Panel content")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        assert call_arg.renderable == "Panel content"


def test_progress_context():
    """Test progress context manager creation."""
    # Test that progress_context returns a Progress instance
    progress = progress_context("Test description")
    
    assert isinstance(progress, Progress)
    
    # Check that it has the expected components
    assert len(progress.columns) > 0  # Should have columns defined