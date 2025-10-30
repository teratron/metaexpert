"""Results and status reporting for MetaExpert logger setup."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HandlerInfo:
    """Information about a created handler."""

    name: str
    type: str
    level: str
    file_path: str | None = None
    enabled: bool = True


@dataclass
class ProcessorInfo:
    """Information about a configured processor."""

    name: str
    type: str
    enabled: bool = True


@dataclass
class LoggingSetupResult:
    """Result of logging system setup."""

    success: bool
    handlers_created: int
    processors_configured: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    # Detailed information
    handlers: list[HandlerInfo] = field(default_factory=list)
    processors: list[ProcessorInfo] = field(default_factory=list)
    setup_duration_ms: float = 0.0
    config_hash: str = ""

    def __post_init__(self):
        """Initialize default values."""
        if self.handlers is None:
            self.handlers = []
        if self.processors is None:
            self.processors = []

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.success = False

    def add_handler(self, handler: HandlerInfo) -> None:
        """Add handler information."""
        self.handlers.append(handler)
        self.handlers_created += 1

    def add_processor(self, processor: ProcessorInfo) -> None:
        """Add processor information."""
        self.processors.append(processor)
        self.processors_configured += 1

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the setup result."""
        return {
            "success": self.success,
            "handlers_created": self.handlers_created,
            "processors_configured": self.processors_configured,
            "warnings_count": len(self.warnings),
            "errors_count": len(self.errors),
            "setup_duration_ms": round(self.setup_duration_ms, 2),
            "config_hash": self.config_hash,
            "handlers": [
                {
                    "name": h.name,
                    "type": h.type,
                    "level": h.level,
                    "file_path": h.file_path,
                    "enabled": h.enabled,
                }
                for h in self.handlers
            ],
            "processors": [
                {
                    "name": p.name,
                    "type": p.type,
                    "enabled": p.enabled,
                }
                for p in self.processors
            ],
            "warnings": self.warnings,
            "errors": self.errors,
        }

    def to_string(self) -> str:
        """Convert result to human-readable string."""
        lines = [
            f"Logging Setup Result: {'SUCCESS' if self.success else 'FAILED'}",
            f"Handlers created: {self.handlers_created}",
            f"Processors configured: {self.processors_configured}",
            f"Setup duration: {self.setup_duration_ms:.2f}ms",
            "",
        ]

        if self.handlers:
            lines.append("Handlers:")
            for handler in self.handlers:
                status = "✓" if handler.enabled else "✗"
                file_info = f" -> {handler.file_path}" if handler.file_path else ""
                lines.append(
                    f"  {status} {handler.name} ({handler.type}) - {handler.level}{file_info}"
                )
            lines.append("")

        if self.processors:
            lines.append("Processors:")
            for processor in self.processors:
                status = "✓" if processor.enabled else "✗"
                lines.append(f"  {status} {processor.name} ({processor.type})")
            lines.append("")

        if self.warnings:
            lines.append("Warnings:")
            for warning in self.warnings:
                lines.append(f"  ⚠ {warning}")
            lines.append("")

        if self.errors:
            lines.append("Errors:")
            for error in self.errors:
                lines.append(f"  ❌ {error}")
            lines.append("")

        return "\n".join(lines)


def create_success_result(
    handlers_count: int,
    processors_count: int,
    setup_duration_ms: float = 0.0,
    config_hash: str = "",
) -> LoggingSetupResult:
    """Create a successful setup result."""
    return LoggingSetupResult(
        success=True,
        handlers_created=handlers_count,
        processors_configured=processors_count,
        warnings=[],
        errors=[],
        setup_duration_ms=setup_duration_ms,
        config_hash=config_hash,
    )


def create_failure_result(
    error_message: str,
    handlers_count: int = 0,
    processors_count: int = 0,
) -> LoggingSetupResult:
    """Create a failed setup result."""
    return LoggingSetupResult(
        success=False,
        handlers_created=handlers_count,
        processors_configured=processors_count,
        warnings=[],
        errors=[error_message],
    )
