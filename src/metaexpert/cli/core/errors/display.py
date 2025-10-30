"""Error display with recommendations for MetaExpert CLI."""

from metaexpert.cli.core.errors.context import ErrorContext
from metaexpert.cli.core.errors.severity import ErrorSeverity
from metaexpert.cli.core.errors.types import CLIError
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.logger import get_logger


class ErrorDisplay:
    """Display errors with helpful suggestions."""

    def __init__(self, output: OutputFormatter):
        """
        Initialize ErrorDisplay.

        Args:
            output: Output formatter instance.
        """
        self.output = output
        self.logger = get_logger(__name__)

    def show_error(self, error: CLIError, context: ErrorContext) -> None:
        """
        Display error with all context and recommendations.

        Args:
            error: The error to display.
            context: Contextual information about the error.
        """
        # 1. Основная ошибка
        self._display_main_error(error, context)

        # 2. Рекомендации
        suggestions = self._generate_suggestions(error, context)
        if suggestions:
            self._display_suggestions(suggestions)

        # 3. Действия восстановления
        recovery_actions = self._get_recovery_actions(error, context)
        if recovery_actions:
            self._display_recovery_actions(recovery_actions)

        # 4. Дополнительная информация
        self._display_additional_info(error, context)

    def _display_main_error(self, error: CLIError, context: ErrorContext) -> None:
        """
        Display the main error message.

        Args:
            error: The error to display.
            context: Contextual information about the error.
        """
        # Determine severity for display
        if isinstance(error, KeyboardInterrupt):
            severity = ErrorSeverity.INFO
        elif error.exit_code >= 100:  # Custom high exit codes for critical errors
            severity = ErrorSeverity.CRITICAL
        elif error.exit_code >= 10:  # Custom medium exit codes for errors
            severity = ErrorSeverity.ERROR
        elif error.exit_code > 1:  # Standard exit codes for warnings
            severity = ErrorSeverity.WARNING
        else:  # Exit code 0 or 1
            severity = ErrorSeverity.ERROR

        # Display error message
        if severity == ErrorSeverity.CRITICAL:
            self.output.error(
                f"Critical Error: {error.message}", title=f"{severity.value.upper()}"
            )
        elif severity == ErrorSeverity.ERROR:
            self.output.error(
                f"Error: {error.message}", title=f"{severity.value.upper()}"
            )
        elif severity == ErrorSeverity.WARNING:
            self.output.warning(
                f"Warning: {error.message}", title=f"{severity.value.upper()}"
            )
        else:
            self.output.info(
                f"Info: {error.message}", title=f"{severity.value.upper()}"
            )

    def _generate_suggestions(
        self, error: CLIError, context: ErrorContext
    ) -> list[str]:
        """
        Generate suggestions for resolving the error.

        Args:
            error: The error to generate suggestions for.
            context: Contextual information about the error.

        Returns:
            List of suggestions.
        """
        suggestions = []

        # Add general suggestions based on error type
        if isinstance(error, CLIError):
            if "validation" in error.message.lower():
                suggestions.append("Check your input parameters")
                suggestions.append("Use 'metaexpert help' for syntax")
                suggestions.append("Validate using 'metaexpert doctor'")
            elif "process" in error.message.lower():
                suggestions.append("Check if process is already running")
                suggestions.append("Verify project directory exists")
                suggestions.append("Check system resources")
            elif "template" in error.message.lower():
                suggestions.append("Reinstall MetaExpert package")
                suggestions.append("Check template files exist")
                suggestions.append("Verify Jinja2 is installed")
            elif (
                "file" in error.message.lower() and "not found" in error.message.lower()
            ):
                suggestions.append("Check file path exists")
                suggestions.append("Verify file permissions")
                suggestions.append("Use absolute path if needed")
            elif "permission" in error.message.lower():
                suggestions.append("Check directory permissions")
                suggestions.append("Try running with sudo (not recommended)")
                suggestions.append("Change working directory")

        # Add context-specific suggestions
        if context.command:
            suggestions.append(
                f"Review '{context.command}' command usage with 'metaexpert {context.command} --help'"
            )

        # Add general suggestions
        suggestions.append("Run with --debug flag for more info")
        suggestions.append(
            "Report issue at https://github.com/teratron/metaexpert/issues"
        )

        return suggestions

    def _display_suggestions(self, suggestions: list[str]) -> None:
        """
        Display suggestions for resolving the error.

        Args:
            suggestions: List of suggestions to display.
        """
        if suggestions:
            suggestions_text = "\n".join(f"  • {s}" for s in suggestions)
            self.output.custom_table(
                [{"Suggestion": s} for s in suggestions],
                columns=["Suggestion"],
                title="💡 Suggestions",
            )

    def _get_recovery_actions(
        self, error: CLIError, context: ErrorContext
    ) -> list[str]:
        """
        Get recovery actions for the error.

        Args:
            error: The error to get recovery actions for.
            context: Contextual information about the error.

        Returns:
            List of recovery actions.
        """
        # In a real implementation, this would interact with the ErrorHandler
        # to get actual recovery actions. For now, we'll return placeholder actions.
        recovery_actions = []

        # Add recovery actions based on error type
        if isinstance(error, CLIError):
            if "process" in error.message.lower():
                recovery_actions.append("cleanup_stale_processes")
                recovery_actions.append("free_system_resources")
            elif "template" in error.message.lower():
                recovery_actions.append("reinstall_templates")

        return recovery_actions

    def _display_recovery_actions(self, recovery_actions: list[str]) -> None:
        """
        Display recovery actions for the error.

        Args:
            recovery_actions: List of recovery actions to display.
        """
        if recovery_actions:
            recovery_text = "\n".join(f"  • {action}" for action in recovery_actions)

            self.output.custom_table(
                [{"Action": action} for action in recovery_actions],
                columns=["Action"],
                title="🔧 Recovery Actions",
            )

    def _display_additional_info(self, error: CLIError, context: ErrorContext) -> None:
        """
        Display additional information about the error.

        Args:
            error: The error to display additional information for.
            context: Contextual information about the error.
        """
        # Display error ID
        self.output.info(f"Error ID: {context.id}")

        # Display command if available
        if context.command:
            self.output.info(f"Command: {context.command}")

        # Display working directory if available
        if context.working_directory:
            self.output.info(f"Working Directory: {context.working_directory}")

        # Display technical details for critical errors
        if error.exit_code >= 100:
            # Display stack trace if available
            if context.stack_trace:
                stack_trace_text = "\n".join(context.stack_trace)
                self.output.custom_table(
                    [{"Line": line} for line in context.stack_trace],
                    columns=["Line"],
                    title="📋 Technical Details",
                )
            elif error.__cause__:
                # If there's a cause, display its traceback
                import traceback

                tb_lines = traceback.format_exception(
                    type(error.__cause__),
                    error.__cause__,
                    error.__cause__.__traceback__,
                )
                tb_text = "".join(tb_lines)
                self.output.custom_table(
                    [{"Traceback": tb_text}],
                    columns=["Traceback"],
                    title="📋 Technical Details",
                )

            # Display resources
            self.output.custom_table(
                [
                    {"Resource": "Run with --debug flag for more information"},
                    {
                        "Resource": "Report at: https://github.com/teratron/metaexpert/issues"
                    },
                ],
                columns=["Resource"],
                title="🔗 Resources",
            )
