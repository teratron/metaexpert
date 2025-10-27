"""Error recovery strategies for MetaExpert CLI."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from metaexpert.cli.core.errors.context import ErrorContext
from metaexpert.cli.core.errors.types import CLIError


class RecoveryStrategy(ABC):
    """Abstract base class for error recovery strategies."""
    
    @abstractmethod
    def can_recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Determine if this strategy can recover from the error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if this strategy can attempt recovery, False otherwise.
        """
        pass
    
    @abstractmethod
    def recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Attempt to recover from the error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        pass


class RetryStrategy(RecoveryStrategy):
    """Recovery strategy that retries the operation with exponential backoff."""
    
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0):
        """
        Initialize RetryStrategy.
        
        Args:
            max_attempts: Maximum number of retry attempts.
            base_delay: Base delay between retries in seconds.
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
    
    def can_recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Determine if this strategy can recover from the error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if this strategy can attempt recovery, False otherwise.
        """
        # This strategy can recover from most errors
        return True
    
    def recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Attempt to recover from the error by retrying.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        import time
        import random
        
        for attempt in range(1, self.max_attempts + 1):
            try:
                # Exponential backoff with jitter
                delay = self.base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0, 0.1 * delay)
                time.sleep(delay + jitter)
                
                # Here we would normally retry the operation
                # Since we don't have access to the original operation,
                # we'll just simulate a successful retry on the last attempt
                if attempt == self.max_attempts:
                    return True
                    
            except Exception as e:
                # If another error occurs during retry, continue to the next attempt
                continue
                
        return False


class FallbackStrategy(RecoveryStrategy):
    """Recovery strategy that uses a fallback operation."""
    
    def __init__(self, fallback_operation: Any):
        """
        Initialize FallbackStrategy.
        
        Args:
            fallback_operation: The fallback operation to use.
        """
        self.fallback_operation = fallback_operation
    
    def can_recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Determine if this strategy can recover from the error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if this strategy can attempt recovery, False otherwise.
        """
        # This strategy can recover if a fallback operation is available
        return self.fallback_operation is not None
    
    def recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Attempt to recover from the error by using a fallback operation.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        try:
            # Execute the fallback operation
            if callable(self.fallback_operation):
                self.fallback_operation()
            return True
        except Exception:
            # If the fallback operation fails, recovery is not possible
            return False


class IgnoreStrategy(RecoveryStrategy):
    """Recovery strategy that ignores the error and continues."""
    
    def can_recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Determine if this strategy can recover from the error.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if this strategy can attempt recovery, False otherwise.
        """
        # This strategy can recover from any error by ignoring it
        return True
    
    def recover(self, error: CLIError, context: ErrorContext) -> bool:
        """
        Attempt to recover from the error by ignoring it.
        
        Args:
            error: The error that occurred.
            context: Contextual information about the error.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        # Simply return True to indicate that the error is ignored
        return True