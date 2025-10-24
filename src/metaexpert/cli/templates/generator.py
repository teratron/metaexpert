# src/metaexpert/cli/templates/generator.py
"""Template generation system using Jinja2."""

import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template

from metaexpert.cli.core.exceptions import TemplateError


class TemplateGenerator:
    """Generates project files from templates."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template generator.
        
        Args:
            template_dir: Custom template directory (defaults to built-in templates)
        """
        if template_dir is None:
            template_dir = Path(__file__).parent / "files"
        
        if not template_dir.exists():
            raise TemplateError(f"Template directory not found: {template_dir}")
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
    
    def generate_project(
        self,
        output_dir: Path,
        project_name: str,
        context: Dict[str, Any],
        force: bool = False,
    ) -> None:
        """
        Generate a complete project from templates.
        
        Args:
            output_dir: Output directory for the project
            project_name: Name of the project
            context: Template context variables
            force: Overwrite existing directory
        
        Raises:
            TemplateError: If generation fails
        """
        project_path = output_dir / project_name
        
        # Validate project directory
        if project_path.exists():
            if not force:
                raise TemplateError(
                    f"Directory '{project_name}' already exists. "
                    "Use --force to overwrite."
                )
            shutil.rmtree(project_path)
        
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Add project metadata to context
        context.update({
            "project_name": project_name,
            "project_path": project_path,
        })
        
        # Generate files
        try:
            self._generate_main_file(project_path, context)
            self._generate_env_file(project_path, context)
            self._generate_gitignore(project_path)
            self._generate_readme(project_path, context)
            self._generate_pyproject_toml(project_path, context)
        except Exception as e:
            # Clean up on failure
            if project_path.exists():
                shutil.rmtree(project_path)
            raise TemplateError(f"Failed to generate project: {e}") from e
    
    def _generate_main_file(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Generate main.py from template."""
        template = self.env.get_template("main.py.j2")
        content = template.render(**context)
        
        main_file = project_path / "main.py"
        main_file.write_text(content, encoding="utf-8")
    
    def _generate_env_file(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Generate .env.example from template."""
        template = self.env.get_template("env.j2")
        content = template.render(**context)
        
        env_file = project_path / ".env.example"
        env_file.write_text(content, encoding="utf-8")
    
    def _generate_gitignore(self, project_path: Path) -> None:
        """Generate .gitignore file."""
        gitignore_content = """# Environment
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Tests
.pytest_cache/
.coverage
htmlcov/

# Data
data/
*.csv
*.db

# PID files
*.pid
"""
        gitignore_file = project_path / ".gitignore"
        gitignore_file.write_text(gitignore_content, encoding="utf-8")
    
    def _generate_readme(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Generate README.md from template."""
        template = self.env.get_template("README.md.j2")
        content = template.render(**context)
        
        readme_file = project_path / "README.md"
        readme_file.write_text(content, encoding="utf-8")
    
    def _generate_pyproject_toml(
        self,
        project_path: Path,
        context: Dict[str, Any],
    ) -> None:
        """Generate pyproject.toml from template."""
        template = self.env.get_template("pyproject.toml.j2")
        content = template.render(**context)
        
        toml_file = project_path / "pyproject.toml"
        toml_file.write_text(content, encoding="utf-8")
    
    def list_strategies(self) -> list[str]:
        """List available strategy templates."""
        strategies_dir = self.template_dir / "strategies"
        if not strategies_dir.exists():
            return ["template"]
        
        return [
            f.stem
            for f in strategies_dir.glob("*.j2")
            if f.is_file()
        ]

