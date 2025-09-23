from typing import Protocol

from metaexpert.logger import Logger


class EventHandler(Protocol):
    """Base protocol for event handlers."""

    _start_time: float
    _elapsed_time: float
    _is_running: bool
    logger: Logger

    async def start(self) -> None:
        """Start the handler."""
        ...

    def stop(self) -> None:
        """Stop the handler."""
        ...
