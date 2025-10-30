"""Signal handler for graceful shutdown of CLI processes."""

import signal
import sys
import threading
from collections.abc import Callable

from metaexpert.logger import get_logger


class SignalHandler:
    """Handle system signals gracefully."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.handlers: dict[int, list[Callable]] = {}
        self._lock = threading.Lock()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup signal handlers."""
        # Handle SIGINT (Ctrl+C) and SIGTERM (termination request)
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        # On Windows, SIGQUIT is not available, so we only handle SIGINT and SIGTERM
        # On Unix-like systems, we could also handle SIGQUIT
        if hasattr(signal, "SIGQUIT"):
            signal.signal(signal.SIGQUIT, self._handle_signal)

        self.logger.info("Signal handlers registered for SIGINT, SIGTERM")

    def _handle_signal(self, signum: int, frame) -> None:
        """
        Handle received signal.

        Args:
            signum: Signal number received
            frame: Current stack frame (unused)
        """
        # Log the received signal
        signal_name = (
            signal.Signals(signum).name
            if isinstance(signum, int)
            else f"Signal {signum}"
        )
        self.logger.warning(f"Signal received: {signal_name}")

        # Execute registered handlers for this signal
        with self._lock:
            handlers_for_signal = self.handlers.get(signum, [])
            for handler in handlers_for_signal:
                try:
                    handler()
                except Exception as e:
                    self.logger.error(f"Error in signal handler: {e}")

        # Exit the program gracefully after handling signals
        # This is a basic approach; in a more complex application,
        # you might want to initiate a graceful shutdown sequence.
        self.logger.info("Exiting gracefully...")
        sys.exit(0)

    def register(self, signum: int, handler: Callable) -> None:
        """
        Register handler for signal.

        Args:
            signum: Signal number to handle (e.g., signal.SIGINT)
            handler: Callable to execute when signal is received
        """
        with self._lock:
            if signum not in self.handlers:
                self.handlers[signum] = []
            self.handlers[signum].append(handler)

        self.logger.debug(f"Registered handler for signal {signum}")


# Global instance for convenience
_signal_handler = SignalHandler()


def get_signal_handler() -> SignalHandler:
    """Get the global signal handler instance."""
    return _signal_handler
