"""TemplateFile model representing the template.py file."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TemplateFile:
    """Represents the template.py file that serves as the starting point for all trading strategies.

    Attributes:
        path: File path where the template is located
        content: The content of the template file
        version: Version of the template
        last_modified: When the template was last modified
    """

    path: str
    content: str
    version: str
    last_modified: datetime

    def __post_init__(self) -> None:
        """Validate the template file after initialization."""
        if not self.path:
            raise ValueError("Template file path cannot be empty")
        if not self.content:
            raise ValueError("Template file content cannot be empty")
        if not self.version:
            raise ValueError("Template file version cannot be empty")
