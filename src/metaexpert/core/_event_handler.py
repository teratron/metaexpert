from typing import Protocol


class EventHandler(Protocol):
    """Base protocol for event handlers."""

    _is_running: bool

    async def start(self) -> None:
        """Start the handler."""
        ...

    def stop(self) -> None:
        """Stop the handler."""
        ...
