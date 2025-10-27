"""Custom exception types for MetaExpert CLI."""

from typing import Optional


class CLIError(Exception):
    """Base exception for CLI errors."""
    
    def __init__(self, message: str, exit_code: int = 1, cause: Optional[Exception] = None):
        """
        Initialize CLIError.
        
        Args:
            message: Error message.
            exit_code: Exit code to use when exiting.
            cause: Underlying exception that caused this error.
        """
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.cause = cause


class ValidationError(CLIError):
    """Raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        """
        Initialize ValidationError.
        
        Args:
            message: Error message.
            field: Field that failed validation.
        """
        super().__init__(message, exit_code=1)
        self.field = field


class ProcessError(CLIError):
    """Raised when a process-related operation fails."""
    
    def __init__(self, message: str, pid: Optional[int] = None):
        """
        Initialize ProcessError.
        
        Args:
            message: Error message.
            pid: Process ID related to the error.
        """
        super().__init__(message, exit_code=1)
        self.pid = pid


class ProjectError(CLIError):
    """Raised when a project-related operation fails."""
    
    def __init__(self, message: str, project_path: Optional[str] = None):
        """
        Initialize ProjectError.
        
        Args:
            message: Error message.
            project_path: Path to the project related to the error.
        """
        super().__init__(message, exit_code=1)
        self.project_path = project_path


class TemplateError(CLIError):
    """Raised when a template-related operation fails."""
    
    def __init__(self, message: str, template_name: Optional[str] = None):
        """
        Initialize TemplateError.
        
        Args:
            message: Error message.
            template_name: Name of the template related to the error.
        """
        super().__init__(message, exit_code=1)
        self.template_name = template_name