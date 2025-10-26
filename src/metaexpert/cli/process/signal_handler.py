"""Signal handler for graceful shutdown of MetaExpert CLI processes.

This module provides a SignalHandler class that allows for proper handling
of system signals like SIGINT and SIGTERM to ensure clean shutdowns and
resource cleanup in CLI applications.
"""

import signal
import sys
from collections.abc import Callable

from metaexpert.logger import get_logger


class SignalHandler:
    """Handle system signals gracefully.

    This class manages signal handlers for SIGINT and SIGTERM, allowing
    multiple handlers to be registered for each signal. When a signal is
    received, all registered handlers are called in sequence.
    """

    def __init__(self):
        """Initialize the signal handler and set up default signal handling."""
        self.handlers: dict[int, list[Callable]] = {}
        self.logger = get_logger(__name__)
        self._original_handlers = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup signal handlers for SIGINT and SIGTERM."""
        # Store original handlers to restore them later if needed
        self._original_handlers[signal.SIGINT] = signal.signal(
            signal.SIGINT, self._handle_signal
        )
        self._original_handlers[signal.SIGTERM] = signal.signal(
            signal.SIGTERM, self._handle_signal
        )

    def _handle_signal(self, signum: int, frame) -> None:
        """Handle received signal by executing all registered handlers.

        Args:
            signum: The signal number received
            frame: The current stack frame (unused)
        """
        self.logger.warning(
            "signal received, initiating graceful shutdown",
            signal=signal.Signals(signum).name,
        )

        # Execute all registered handlers for this signal
        for handler in self.handlers.get(signum, []):
            try:
                handler()
            except Exception as e:
                self.logger.error(
                    "error in signal handler",
                    error=str(e),
                    signal=signal.Signals(signum).name,
                )

        # Exit the process after handling all signals
        self.logger.info("signal handling completed, exiting")
        sys.exit(0)

    def register(self, signum: int, handler: Callable) -> None:
        """Register a handler for a specific signal.

        Args:
            signum: The signal number to register handler for
            handler: The callable to execute when signal is received
        """
        if signum not in self.handlers:
            self.handlers[signum] = []
        self.handlers[signum].append(handler)
        self.logger.debug(
            "signal handler registered",
            signal=signal.Signals(signum).name,
            handler=str(handler),
        )

    def unregister(self, signum: int, handler: Callable) -> bool:
        """Unregister a handler for a specific signal.

        Args:
            signum: The signal number to unregister handler for
            handler: The callable to remove from handlers

        Returns:
            True if handler was found and removed, False otherwise
        """
        if signum in self.handlers and handler in self.handlers[signum]:
            self.handlers[signum].remove(handler)
            self.logger.debug(
                "signal handler unregistered",
                signal=signal.Signals(signum).name,
                handler=str(handler),
            )
            return True
        return False

    def restore_original_handlers(self) -> None:
        """Restore the original signal handlers."""
        for signum, original_handler in self._original_handlers.items():
            signal.signal(signum, original_handler)
        self.logger.debug("original signal handlers restored")
