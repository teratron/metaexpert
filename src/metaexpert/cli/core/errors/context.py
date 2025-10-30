"""Error context for MetaExpert CLI."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class ErrorContext:
    """Contextual information about an error."""

    # Unique identifier for this error instance
    id: UUID = field(default_factory=uuid4)

    # Timestamp when the error occurred
    timestamp: datetime = field(default_factory=datetime.now)

    # Command that was being executed
    command: str | None = None

    # Arguments passed to the command
    arguments: dict[str, Any] = field(default_factory=dict)

    # Working directory
    working_directory: str | None = None

    # Environment variables (filtered for security)
    environment: dict[str, str] = field(default_factory=dict)

    # Stack trace
    stack_trace: list[str] | None = None

    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the error context.

        Args:
            key: Metadata key.
            value: Metadata value.
        """
        self.metadata[key] = value

    def filter_sensitive_data(self) -> None:
        """Filter sensitive data from environment variables."""
        sensitive_keys = {
            "API_KEY",
            "API_SECRET",
            "PASSWORD",
            "SECRET",
            "TOKEN",
        }

        for key in list(self.environment.keys()):
            if any(sensitive_key in key.upper() for sensitive_key in sensitive_keys):
                self.environment[key] = "***FILTERED***"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert error context to dictionary.

        Returns:
            Dictionary representation of the error context.
        """
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat(),
            "command": self.command,
            "arguments": self.arguments,
            "working_directory": self.working_directory,
            "environment": self.environment,
            "stack_trace": self.stack_trace,
            "metadata": self.metadata,
        }
