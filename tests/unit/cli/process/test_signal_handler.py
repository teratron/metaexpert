"""Unit tests for SignalHandler class."""

import signal
from unittest.mock import Mock, patch

from metaexpert.cli.process.signal_handler import SignalHandler


class TestSignalHandler:
    """Test cases for SignalHandler class."""

    def test_initialization_registers_handlers(self):
        """Test that initialization properly registers signal handlers."""
        with patch("signal.signal") as mock_signal:
            SignalHandler()

            # Check that signal.signal was called for both SIGINT and SIGTERM
            assert mock_signal.call_count == 2

            # Verify calls were made for SIGINT and SIGTERM
            calls = mock_signal.call_args_list
            called_signals = [call[0][0] for call in calls]
            assert signal.SIGINT in called_signals
            assert signal.SIGTERM in called_signals

    def test_register_handler(self):
        """Test registering a handler for a signal."""
        handler = SignalHandler()
        mock_func = Mock()

        # Register handler for SIGINT
        handler.register(signal.SIGINT, mock_func)

        # Verify handler is registered
        assert signal.SIGINT in handler.handlers
        assert mock_func in handler.handlers[signal.SIGINT]

    def test_unregister_handler(self):
        """Test unregistering a handler."""
        handler = SignalHandler()
        mock_func = Mock()

        # Register and then unregister handler
        handler.register(signal.SIGINT, mock_func)
        result = handler.unregister(signal.SIGINT, mock_func)

        # Verify handler was removed
        assert result is True
        assert (
            signal.SIGINT not in handler.handlers
            or mock_func not in handler.handlers[signal.SIGINT]
        )

    def test_unregister_nonexistent_handler(self):
        """Test unregistering a handler that doesn't exist."""
        handler = SignalHandler()
        mock_func = Mock()

        # Try to unregister non-registered handler
        result = handler.unregister(signal.SIGINT, mock_func)

        # Should return False
        assert result is False

    def test_handle_signal_executes_registered_handlers(self):
        """Test that handling a signal executes all registered handlers."""
        handler = SignalHandler()
        mock_func1 = Mock()
        mock_func2 = Mock()

        # Register multiple handlers
        handler.register(signal.SIGINT, mock_func1)
        handler.register(signal.SIGINT, mock_func2)

        # Manually call the signal handler
        with patch("sys.exit") as mock_exit:
            handler._handle_signal(signal.SIGINT, None)

        # Verify all handlers were called
        mock_func1.assert_called_once()
        mock_func2.assert_called_once()
        mock_exit.assert_called_once_with(0)

    def test_handle_signal_with_exception(self):
        """Test that exceptions in handlers don't stop other handlers."""
        handler = SignalHandler()
        mock_func1 = Mock(side_effect=Exception("Test error"))
        mock_func2 = Mock()

        # Register handlers where first one raises exception
        handler.register(signal.SIGINT, mock_func1)
        handler.register(signal.SIGINT, mock_func2)

        # Manually call the signal handler
        with patch("sys.exit") as mock_exit:
            handler._handle_signal(signal.SIGINT, None)

        # Both handlers should be called despite exception in first
        mock_func1.assert_called_once()
        mock_func2.assert_called_once()
        mock_exit.assert_called_once_with(0)

    def test_restore_original_handlers(self):
        """Test that original handlers can be restored."""
        with patch("signal.signal") as mock_signal:
            # Set up initial state
            original_handler = Mock()
            mock_signal.return_value = original_handler

            handler = SignalHandler()

            # Reset mock to check restore call
            mock_signal.reset_mock()

            # Restore original handlers
            handler.restore_original_handlers()

            # Verify that original handlers were restored
            assert mock_signal.call_count == 2
            calls = mock_signal.call_args_list
            called_signals = [call[0][0] for call in calls]
            assert signal.SIGINT in called_signals
            assert signal.SIGTERM in called_signals
