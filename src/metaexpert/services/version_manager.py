"""Template version management module."""

import os
import re
from datetime import datetime


class TemplateVersionManager:
    """Manager for template versioning."""

    def __init__(self, template_path: str) -> None:
        """Initialize the template version manager.

        Args:
            template_path: Path to the template file
        """
        self.template_path = template_path
        self.version_history = []

    def get_current_version(self) -> str | None:
        """Get the current version of the template.

        Returns:
            Current version string or None if not found
        """
        if not os.path.exists(self.template_path):
            return None

        try:
            with open(self.template_path, encoding='utf-8') as f:
                content = f.read()

            # Look for version in the template content
            # This is a simplified approach - in reality, you might look in a specific location
            version_match = re.search(r'@version:\s*([0-9]+\.[0-9]+\.[0-9]+)', content)
            if version_match:
                return version_match.group(1)

            # Alternative: look for version in a comment
            version_match = re.search(r'#\s*Version:\s*([0-9]+\.[0-9]+\.[0-9]+)', content)
            if version_match:
                return version_match.group(1)

            return None
        except Exception:
            return None

    def update_version(self, new_version: str) -> bool:
        """Update the template version.

        Args:
            new_version: New version string

        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(self.template_path):
            return False

        try:
            with open(self.template_path, encoding='utf-8') as f:
                content = f.read()

            # Update version in the template content
            # This is a simplified approach - in reality, you would be more precise
            updated_content = re.sub(
                r'(@version:|Version:)\s*[0-9]+\.[0-9]+\.[0-9]+',
                f'\\1 {new_version}',
                content
            )

            # If no version was found, add it to the header
            if updated_content == content:
                # Add version to the header
                lines = content.split('\n')
                # Insert version after the first line (module docstring)
                lines.insert(1, f'# @version: {new_version}')
                updated_content = '\n'.join(lines)

            # Write the updated content back to the file
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            # Record the version change
            self.version_history.append({
                'version': new_version,
                'timestamp': datetime.now().isoformat(),
                'previous_version': self.get_current_version()
            })

            return True
        except Exception:
            return False

    def get_version_history(self) -> list:
        """Get the version history.

        Returns:
            List of version history entries
        """
        return self.version_history.copy()

    def is_version_compatible(self, required_version: str) -> bool:
        """Check if the current version is compatible with a required version.

        Args:
            required_version: Required version string

        Returns:
            True if compatible, False otherwise
        """
        current_version = self.get_current_version()
        if current_version is None:
            return False

        # Simple version comparison (major.minor.patch)
        try:
            current_parts = [int(x) for x in current_version.split('.')]
            required_parts = [int(x) for x in required_version.split('.')]

            # Check major version compatibility
            if current_parts[0] != required_parts[0]:
                return False

            # Check minor version compatibility
            if current_parts[1] < required_parts[1]:
                return False

            # Check patch version compatibility
            if current_parts[1] == required_parts[1] and current_parts[2] < required_parts[2]:
                return False

            return True
        except Exception:
            return False
