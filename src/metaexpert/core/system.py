"""Dummy system module to satisfy dependencies during testing of the logging system."""
from typing import Any


class MetaProcess:
    """Dummy MetaProcess class to satisfy import dependencies."""
    
    def __init__(self, *args, **kwargs):
        """Initialize dummy process."""
        pass
    
    @classmethod
    def create(cls, *args, **kwargs) -> 'MetaProcess':
        """Create a dummy process."""
        return cls(*args, **kwargs)
    
    def start(self):
        """Start the dummy process."""
        pass
    
    def stop(self):
        """Stop the dummy process."""
        pass