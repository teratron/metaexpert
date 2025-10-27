"""Error handler for MetaExpert CLI."""

import sys
import traceback
from typing import List, Optional

from metaexpert.cli.core.errors.context import ErrorContext
from metaexpert.cli.core.errors.recovery import RecoveryStrategy
from metaexpert.cli.core.errors.severity import ErrorSeverity
from metaexpert.cli.core.errors.types import CLIError
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.logger import get_logger


class ErrorHandler:
    """Handles errors in the MetaExpert CLI."""
    
    def __init__(self):
        """Initialize ErrorHandler."""
        self.logger = get_logger(__name__)
        self.output = OutputFormatter()
        self.recovery_strategies: List[RecoveryStrategy] = []
    
    def add_recovery_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Add a recovery strategy.
        
        Args:
            strategy: Recovery strategy to add.
        """
        self.recovery_strategies.append(strategy)
    
    def handle_error(self, error: Exception, context: Optional[ErrorContext] = None) -> None:
        """
        Handle an error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
        """
        # If no context is provided, create a basic one
        if context is None:
            context = ErrorContext()
            
        # If the error is a CLIError, use its properties
        if isinstance(error, CLIError):
            self._handle_cli_error(error, context)
        else:
            # For other exceptions, wrap them in a CLIError
            cli_error = CLIError(str(error), cause=error)
            self._handle_cli_error(cli_error, context)
    
    def _handle_cli_error(self, error: CLIError, context: ErrorContext) -> None:
        """
        Handle a CLIError.
        
        Args:
            error: The CLIError to handle.
            context: Contextual information about the error.
        """
        # Log the error
        self._log_error(error, context)
        
        # Display the error to the user
        self._display_error(error, context)
        
        # Attempt recovery
        recovered = self._attempt_recovery(error, context)
        
        # If recovery failed and the error has an exit code, exit the program
        if not recovered and hasattr(error, 'exit_code'):
            sys.exit(error.exit_code)
    
    def _log_error(self, error: CLIError, context: ErrorContext) -> None:
        """
        Log an error.
        
        Args:
            error: The error to log.
            context: Contextual information about the error.
        """
        # Determine severity
        if isinstance(error, KeyboardInterrupt):
            severity = ErrorSeverity.INFO
        elif error.exit_code >= 100:  # Custom high exit codes for critical errors
            severity = ErrorSeverity.CRITICAL
        elif error.exit_code >= 10:   # Custom medium exit codes for errors
            severity = ErrorSeverity.ERROR
        elif error.exit_code > 1:     # Standard exit codes for warnings
            severity = ErrorSeverity.WARNING
        else:                         # Exit code 0 or 1
            severity = ErrorSeverity.ERROR
            
        # Log with appropriate level
        log_method = getattr(self.logger, severity.value, self.logger.error)
        log_method(
            error.message,
            extra={
                "error_id": str(context.id),
                "error_type": type(error).__name__,
                "exit_code": error.exit_code,
                "context": context.to_dict(),
            },
        )
        
        # Log stack trace if available
        if context.stack_trace:
            self.logger.debug(
                "Stack trace",
                extra={
                    "error_id": str(context.id),
                    "stack_trace": "\n".join(context.stack_trace),
                },
            )
        elif error.__cause__:
            # If there's a cause, log its traceback
            tb_lines = traceback.format_exception(
                type(error.__cause__), 
                error.__cause__, 
                error.__cause__.__traceback__
            )
            self.logger.debug(
                "Caused by",
                extra={
                    "error_id": str(context.id),
                    "caused_by": "".join(tb_lines),
                },
            )
    
    def _display_error(self, error: CLIError, context: ErrorContext) -> None:
        """
        Display an error to the user.
        
        Args:
            error: The error to display.
            context: Contextual information about the error.
        """
        # Determine severity for display
        if isinstance(error, KeyboardInterrupt):
            severity = ErrorSeverity.INFO
        elif error.exit_code >= 100:
            severity = ErrorSeverity.CRITICAL
        elif error.exit_code >= 10:
            severity = ErrorSeverity.ERROR
        elif error.exit_code > 1:
            severity = ErrorSeverity.WARNING
        else:
            severity = ErrorSeverity.ERROR
            
        # Display error message
        if severity == ErrorSeverity.CRITICAL:
            self.output.error(f"Critical Error: {error.message}")
        elif severity == ErrorSeverity.ERROR:
            self.output.error(f"Error: {error.message}")
        elif severity == ErrorSeverity.WARNING:
            self.output.warning(f"Warning: {error.message}")
        else:
            self.output.info(f"Info: {error.message}")
            
        # Display context if it's a critical error
        if severity >= ErrorSeverity.ERROR:
            self.output.info(f"Error ID: {context.id}")
            if context.command:
                self.output.info(f"Command: {context.command}")
                
    def _attempt_recovery(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Attempt to recover from an error.
        
        Args:
            error: The error to recover from.
            context: Contextual information about the error.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        # Try each recovery strategy
        for strategy in self.recovery_strategies:
            if strategy.can_recover(error, context):
                try:
                    if strategy.recover(error, context):
                        self.logger.info(
                            "Error recovery successful",
                            extra={"error_id": str(context.id)},
                        )
                        return True
                except Exception as e:
                    self.logger.warning(
                        "Error recovery failed",
                        extra={
                            "error_id": str(context.id),
                            "recovery_error": str(e),
                        },
                    )
                    
        # No recovery strategy was successful
        self.logger.info(
            "No suitable error recovery strategy found",
            extra={"error_id": str(context.id)},
        )
        return False


# Global error handler instance
_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    return _error_handler