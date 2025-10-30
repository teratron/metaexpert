"""Tests for the output formatting module."""

from unittest.mock import Mock, patch

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from metaexpert.cli.core.output import (
    OutputFormatter,
    custom_table,
    error,
    info,
    json_output,
    progress,
    success,
    table,
    tree,
    warning,
)


class TestOutputFormatter:
    """Test cases for OutputFormatter class."""

    def test_initialization_default_console(self):
        """Test OutputFormatter initialization with default console."""
        formatter = OutputFormatter()
        assert isinstance(formatter.console, Console)

    def test_initialization_custom_console(self):
        """Test OutputFormatter initialization with custom console."""
        mock_console = Mock(spec=Console)
        formatter = OutputFormatter(console=mock_console)
        assert formatter.console == mock_console

    def test_success_message(self, mocker):
        """Test success message output."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.success("Test success message")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the expected style
        assert call_arg.title == "Success"
        assert call_arg.border_style == "green"

    def test_success_message_with_title(self, mocker):
        """Test success message output with custom title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.success("Test success message", title="Custom Success")

        # Verify that a Panel object was created and printed with custom title
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the custom title
        assert call_arg.title == "Custom Success"
        assert call_arg.border_style == "green"

    def test_error_message(self, mocker):
        """Test error message output."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.error("Test error message")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the expected style
        assert call_arg.title == "Error"
        assert call_arg.border_style == "red"

    def test_error_message_with_title(self, mocker):
        """Test error message output with custom title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.error("Test error message", title="Custom Error")

        # Verify that a Panel object was created and printed with custom title
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the custom title
        assert call_arg.title == "Custom Error"
        assert call_arg.border_style == "red"

    def test_warning_message(self, mocker):
        """Test warning message output."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.warning("Test warning message")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the expected style
        assert call_arg.title == "Warning"
        assert call_arg.border_style == "yellow"

    def test_warning_message_with_title(self, mocker):
        """Test warning message output with custom title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.warning("Test warning message", title="Custom Warning")

        # Verify that a Panel object was created and printed with custom title
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the custom title
        assert call_arg.title == "Custom Warning"
        assert call_arg.border_style == "yellow"

    def test_info_message(self, mocker):
        """Test info message output."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.info("Test info message")

        # Verify that a Panel object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the expected style
        assert call_arg.title == "Info"
        assert call_arg.border_style == "blue"

    def test_info_message_with_title(self, mocker):
        """Test info message output with custom title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.info("Test info message", title="Custom Info")

        # Verify that a Panel object was created and printed with custom title
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)
        # Check that the panel has the custom title
        assert call_arg.title == "Custom Info"
        assert call_arg.border_style == "blue"

    def test_table_with_data(self, mocker):
        """Test displaying a table with data."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        headers = ["Name", "Age"]
        rows = [["Alice", 30], ["Bob", 25]]

        formatter.table(headers, rows)

        # Verify that a Table object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        # Check that the table has the expected headers
        assert call_arg.columns[0].header == "Name"
        assert call_arg.columns[1].header == "Age"
        # Check that the table has the expected rows
        assert len(call_arg.rows) == 2
        assert call_arg.rows[0][0] == "Alice"
        assert call_arg.rows[0][1] == "30"
        assert call_arg.rows[1][0] == "Bob"
        assert call_arg.rows[1][1] == "25"
        # Check that the table has the expected headers
        assert call_arg.columns[0].header == "Name"
        assert call_arg.columns[1].header == "Age"
        # Check that the table has the expected rows
        assert len(call_arg.rows) == 2
        assert call_arg.rows[0][0] == "Alice"
        assert call_arg.rows[0][1] == "30"
        assert call_arg.rows[1][0] == "Bob"
        assert call_arg.rows[1][1] == "25"

    def test_table_with_title(self, mocker):
        """Test displaying a table with a title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        headers = ["Name", "Age"]
        rows = [["Alice", 30], ["Bob", 25]]

        formatter.table(headers, rows, title="Users")

        # Verify that a Table object with title was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        # Check that the table has the title
        assert call_arg.title == "Users"
        # Check that the table has the expected headers
        assert call_arg.columns[0].header == "Name"
        assert call_arg.columns[1].header == "Age"
        # Check that the table has the expected rows
        assert len(call_arg.rows) == 2
        # In newer versions of Rich, Row objects are not subscriptable
        # We need to access cells differently
        assert str(call_arg.rows[0].cells[0]) == "Alice"
        assert str(call_arg.rows[0].cells[1]) == "30"
        assert str(call_arg.rows[1].cells[0]) == "Bob"
        assert str(call_arg.rows[1].cells[1]) == "25"

    def test_table_with_custom_header_style(self, mocker):
        """Test displaying a table with custom header style."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        headers = ["Name", "Age"]
        rows = [["Alice", 30], ["Bob", 25]]

        formatter.table(headers, rows, header_style="bold blue")

        # Verify that a Table object with custom header style was created
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        # Check that the table has the expected headers
        assert call_arg.columns[0].header == "Name"
        assert call_arg.columns[1].header == "Age"
        # Check that the table has the expected header style
        assert call_arg.header_style == "bold blue"
        # Check that the table has the expected rows
        assert len(call_arg.rows) == 2
        # In newer versions of Rich, Row objects are not subscriptable
        # We need to access cells differently
        assert str(call_arg.rows[0].cells[0]) == "Alice"
        assert str(call_arg.rows[0].cells[1]) == "30"
        assert str(call_arg.rows[1].cells[0]) == "Bob"
        assert str(call_arg.rows[1].cells[1]) == "25"

    def test_json_output_with_dict(self, mocker):
        """Test displaying data as JSON."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = {"name": "Alice", "age": 30}

        formatter.json_output(data)

        # Check that print was called
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        # Check that print was called
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        # Check that print was called
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        # Check that the argument is a JSON object
        assert isinstance(call_arg, JSON)
        # Check that the JSON object contains the expected data
        assert call_arg.text == '{\n  "name": "Alice",\n  "age": 30\n}'

    def test_json_output_with_dict_and_title(self, mocker):
        """Test displaying data as JSON with title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = {"name": "Alice", "age": 30}

        formatter.json_output(data, title="User Data")

        # Check that print was called
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(
            call_arg, Panel
        )  # With title, it should be wrapped in a Panel

    def test_json_output_with_list(self, mocker):
        """Test displaying list as JSON."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

        formatter.json_output(data)

        # Check that print was called
        assert mock_console_print.call_count == 1

    def test_tree_simple_dict(self, mocker):
        """Test displaying a simple dictionary as a tree."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        root_label = "Root"
        children = [{"key1": "value1", "key2": "value2"}]

        formatter.tree(root_label, children)

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)
        # Check that the tree has the expected root label
        assert call_arg.label == "Root"
        # Check that the tree has the expected children
        assert len(call_arg.children) == 1
        assert isinstance(call_arg.children[0], Tree)
        assert call_arg.children[0].label == "key1"
        assert len(call_arg.children[0].children) == 1
        assert call_arg.children[0].children[0].label == "value1"

    def test_tree_with_strings(self, mocker):
        """Test displaying a tree with string children."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        root_label = "Root"
        children = ["Child1", "Child2", "Child3"]

        formatter.tree(root_label, children)

        # Verify that a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Tree)

    def test_tree_with_title(self, mocker):
        """Test displaying a tree with a title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        root_label = "Root"
        children = [{"key1": "value1", "key2": "value2"}]

        formatter.tree(root_label, children, title="Tree Title")

        # Verify that a Panel containing a Tree object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Panel)

    def test_progress_with_tasks(self, mocker):
        """Test progress indicator with tasks."""
        # Mock the Progress context manager
        with patch("metaexpert.cli.core.output.Progress") as mock_progress_class:
            mock_progress_instance = Mock()
            mock_progress_class.return_value.__enter__ = Mock(
                return_value=mock_progress_instance
            )
            mock_progress_class.return_value.__exit__ = Mock(return_value=None)

            formatter = OutputFormatter()

            tasks = [
                {"name": "Task 1", "work": lambda p: None},
                {"name": "Task 2", "work": lambda p: None},
            ]

            formatter.progress(tasks)

            # Verify that Progress was called with the correct parameters
            mock_progress_class.assert_called_once()
            # Verify that add_task was called
            assert mock_progress_instance.add_task.called

    def test_custom_table_with_data(self, mocker):
        """Test displaying a custom table from a list of dictionaries."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]

        formatter.custom_table(data)

        # Verify that a Table object was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)

    def test_custom_table_with_columns(self, mocker):
        """Test displaying a custom table with specific columns."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = [
            {"Name": "Alice", "Age": 30, "City": "NYC"},
            {"Name": "Bob", "Age": 25, "City": "LA"},
        ]
        columns = ["Name", "City"]

        formatter.custom_table(data, columns=columns)

        # Verify that a Table object with correct columns was created
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)

    def test_custom_table_with_title(self, mocker):
        """Test displaying a custom table with a title."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        data = [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]

        formatter.custom_table(data, title="Users")

        # Verify that a Table object with title was created and printed
        assert mock_console_print.call_count == 1
        call_arg = mock_console_print.call_args[0][0]
        assert isinstance(call_arg, Table)
        assert call_arg.title == "Users"

    def test_custom_table_empty_data(self, mocker):
        """Test displaying an empty custom table."""
        mock_console_print = mocker.patch.object(Console, "print")
        formatter = OutputFormatter()

        formatter.custom_table([])

        # Should call info method to display "No data to display"
        assert mock_console_print.call_count == 1


def test_global_success_function(mocker):
    """Test the global success function."""
    mock_success = mocker.patch("metaexpert.cli.core.output._default_formatter.success")

    success("Test message", title="Test Title")

    mock_success.assert_called_once_with("Test message", title="Test Title")


def test_global_error_function(mocker):
    """Test the global error function."""
    mock_error = mocker.patch("metaexpert.cli.core.output._default_formatter.error")

    error("Test message", title="Test Title")

    mock_error.assert_called_once_with("Test message", title="Test Title")


def test_global_warning_function(mocker):
    """Test the global warning function."""
    mock_warning = mocker.patch("metaexpert.cli.core.output._default_formatter.warning")

    warning("Test message", title="Test Title")

    mock_warning.assert_called_once_with("Test message", title="Test Title")


def test_global_info_function(mocker):
    """Test the global info function."""
    mock_info = mocker.patch("metaexpert.cli.core.output._default_formatter.info")

    info("Test message", title="Test Title")

    mock_info.assert_called_once_with("Test message", title="Test Title")


def test_global_table_function(mocker):
    """Test the global table function."""
    mock_table = mocker.patch("metaexpert.cli.core.output._default_formatter.table")

    headers = ["Name", "Age"]
    rows = [["Alice", 30]]
    title = "Test Table"

    table(headers, rows, title=title)

    mock_table.assert_called_once_with(headers, rows, title=title)


def test_global_json_output_function(mocker):
    """Test the global json_output function."""
    mock_json_output = mocker.patch(
        "metaexpert.cli.core.output._default_formatter.json_output"
    )

    data = {"test": "data"}
    title = "Test JSON"

    json_output(data, title=title)

    mock_json_output.assert_called_once_with(data, title=title)


def test_global_tree_function(mocker):
    """Test the global tree function."""
    mock_tree = mocker.patch("metaexpert.cli.core.output._default_formatter.tree")

    root_label = "Root"
    children = [{"key": "value"}]
    title = "Test Tree"

    tree(root_label, children, title=title)

    mock_tree.assert_called_once_with(root_label, children, title=title)


def test_global_progress_function(mocker):
    """Test the global progress function."""
    mock_progress = mocker.patch(
        "metaexpert.cli.core.output._default_formatter.progress"
    )

    tasks = [{"name": "task1", "work": lambda p: None}]
    description = "Test Progress"

    progress(tasks, description=description)

    mock_progress.assert_called_once_with(tasks, description=description)


def test_global_custom_table_function(mocker):
    """Test the global custom_table function."""
    mock_custom_table = mocker.patch(
        "metaexpert.cli.core.output._default_formatter.custom_table"
    )

    data = [{"name": "test"}]
    columns = ["name"]
    title = "Test Table"

    custom_table(data, columns=columns, title=title)

    mock_custom_table.assert_called_once_with(data, columns=columns, title=title)
