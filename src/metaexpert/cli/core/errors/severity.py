"""Error severity levels for MetaExpert CLI."""

from enum import Enum


class ErrorSeverity(Enum):
    """Enumeration of error severity levels."""
    
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    
    def __str__(self) -> str:
        """Return string representation of severity."""
        return self.value
    
    def __lt__(self, other: "ErrorSeverity") -> bool:
        """Compare severity levels."""
        severity_order = [ErrorSeverity.DEBUG, ErrorSeverity.INFO, ErrorSeverity.WARNING, 
                          ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]
        return severity_order.index(self) < severity_order.index(other)
    
    def __le__(self, other: "ErrorSeverity") -> bool:
        """Compare severity levels."""
        return self < other or self == other
    
    def __gt__(self, other: "ErrorSeverity") -> bool:
        """Compare severity levels."""
        return not self <= other
    
    def __ge__(self, other: "ErrorSeverity") -> bool:
        """Compare severity levels."""
        return not self < other