"""Unit tests for TemplateGenerator class.

Note: The TemplateGenerator class does not have a '_get_default_dir()' method as mentioned
in the original task. The class uses 'template_dir' parameter in initialization to set
the template directory path. All tests have been created accordingly.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from metaexpert.cli.templates.generator import TemplateGenerator


class TestTemplateGenerator:
    """Test cases for TemplateGenerator class."""

    def test_initialization(self):
        """Test TemplateGenerator initialization."""
        generator = TemplateGenerator()
        assert generator.template_dir == Path("src/metaexpert/cli/templates/files")
        assert generator.environment is not None

        # Test with custom template directory
        custom_dir = "custom/templates"
        generator = TemplateGenerator(template_dir=custom_dir)
        assert generator.template_dir == Path(custom_dir)

    def test_generate_project_success(self):
        """Test successful project generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = TemplateGenerator()
            project_name = "test_project"
            context = {
                "project_name": project_name,
                "exchange": "binance",
                "strategy": "ema",
                "market_type": "spot",
                "symbol": "BTCUSDT",
                "version": "0.1.0",
                "description": "Test project",
                "author_name": "Test Author",
                "author_email": "test@example.com",
            }

            success = generator.generate_project(project_name, temp_dir, context)
            assert success is True

            # Check that project directory was created
            project_path = Path(temp_dir) / project_name
            assert project_path.exists()
            assert project_path.is_dir()

            # Check that expected files were generated
            expected_files = ["main.py", "README.md", ".env", "pyproject.toml"]
            for file_name in expected_files:
                file_path = project_path / file_name
                assert file_path.exists()
                assert file_path.is_file()

            # Verify content was rendered with context
            main_py_path = project_path / "main.py"
            with open(main_py_path, encoding="utf-8") as f:
                content = f.read()
                assert f'"""{project_name} - Trading Expert' in content
                assert 'exchange="binance"' in content
                assert "# EMA (Exponential Moving Average) Strategy" in content

    def test_generate_project_with_existing_directory_and_force(self):
        """Test project generation with existing directory and force option."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = TemplateGenerator()
            project_name = "test_project"
            context = {
                "project_name": project_name,
                "exchange": "bybit",
                "strategy": "rsi",
                "market_type": "futures",
                "symbol": "ETHUSDT",
                "version": "0.1.0",
                "description": "Test project",
                "author_name": "Test Author",
                "author_email": "test@example.com",
            }

            # Create the project directory first
            project_path = Path(temp_dir) / project_name
            project_path.mkdir(parents=True, exist_ok=True)

            # Add a file to the existing directory
            existing_file = project_path / "existing_file.txt"
            with open(existing_file, "w", encoding="utf-8") as f:
                f.write("This file already exists")

            # Generate project (should succeed since directory will be recreated)
            success = generator.generate_project(project_name, temp_dir, context)
            assert success is True

            # Verify the project was recreated with template files
            expected_files = ["main.py", "README.md", ".env", "pyproject.toml"]
            for file_name in expected_files:
                file_path = project_path / file_name
                assert file_path.exists()
                assert file_path.is_file()

            # The existing file should be gone (directory was recreated)
            assert not existing_file.exists()

    def test_validate_template_exists(self):
        """Test template existence validation."""
        generator = TemplateGenerator()

        # Check that a known template exists
        assert generator.validate_template_exists("main.py.j2") is True
        assert generator.validate_template_exists("nonexistent.j2") is False

    def test_list_available_templates(self):
        """Test listing available templates."""
        generator = TemplateGenerator()

        templates = generator.list_available_templates()

        # Check that expected templates are in the list
        expected_templates = [
            "main.py.j2",
            "env.j2",
            "README.md.j2",
            "pyproject.toml.j2",
            ".gitignore.j2",
        ]
        for template in expected_templates:
            assert template in templates

    def test_render_template_with_undefined_variable(self):
        """Test handling of undefined variables in templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom template with an undefined variable
            custom_template_dir = Path(temp_dir) / "custom_templates"
            custom_template_dir.mkdir()

            # Create a simple template with undefined variable
            template_content = "{{ undefined_variable }}"
            template_path = custom_template_dir / "test.py.j2"
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(template_content)

            generator = TemplateGenerator(str(custom_template_dir))

            # Try to generate project - should handle undefined variable gracefully
            success = generator.generate_project("test_project", temp_dir, {})
            # This should fail gracefully, not raise an exception
            assert success is False

    def test_generate_project_with_special_context_values(self):
        """Test project generation with special context values like conditionals."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = TemplateGenerator()
            project_name = "test_project"
            context = {
                "project_name": project_name,
                "exchange": "okx",
                "strategy": "macd",
                "market_type": "futures",
                "symbol": "BTCUSDT",
                "version": "0.1.0",
                "description": "Test project with futures",
                "author_name": "Test Author",
                "author_email": "test@example.com",
                "requires_passphrase": True,  # This should trigger conditional in template
                "contract_type": "linear",
                "margin_mode": "cross",
                "position_mode": "hedge",
                "leverage": 5,
                "size_value": 2.0,
                "stop_loss_pct": 3.0,
                "take_profit_pct": 6.0,
            }

            success = generator.generate_project(project_name, temp_dir, context)
            assert success is True

            # Check that project directory was created
            project_path = Path(temp_dir) / project_name
            assert project_path.exists()
            assert project_path.is_dir()

            # Check that .env file contains passphrase (because requires_passphrase=True)
            env_path = project_path / ".env"
            with open(env_path, encoding="utf-8") as f:
                env_content = f.read()
                assert "OKX_API_PASSPHRASE" in env_content

            # Check that main.py contains futures-specific configuration
            main_py_path = project_path / "main.py"
            with open(main_py_path, encoding="utf-8") as f:
                main_content = f.read()
                assert 'contract_type="linear"' in main_content
                assert 'margin_mode="cross"' in main_content
                assert 'position_mode="hedge"' in main_content
                # Check MACD strategy section
                assert "MACD Strategy" in main_content

    def test_generate_project_empty_context(self):
        """Test project generation with minimal context."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = TemplateGenerator()
            project_name = "minimal_project"
            # Using minimal context - template should use defaults
            context = {
                "project_name": project_name,
                "exchange": "binance",
                "strategy": "template",  # Use template strategy which has default handling
                "market_type": "spot",
                "version": "0.1.0",
                "description": "Minimal project",
                "author_name": "Test Author",
                "author_email": "test@example.com",
            }

            success = generator.generate_project(project_name, temp_dir, context)
            assert success is True

            # Check that project directory was created
            project_path = Path(temp_dir) / project_name
            assert project_path.exists()
            assert project_path.is_dir()

            # Check that expected files were generated
            expected_files = ["main.py", "README.md", ".env", "pyproject.toml"]
            for file_name in expected_files:
                file_path = project_path / file_name
                assert file_path.exists()
                assert file_path.is_file()

            # Verify content was rendered with defaults
            main_py_path = project_path / "main.py"
            with open(main_py_path, encoding="utf-8") as f:
                content = f.read()
                assert f'"""{project_name} - Trading Expert' in content
                # Should have default values where not provided
                assert 'symbol="BTCUSDT"' in content  # Default value
                assert 'timeframe="1h"' in content  # Default value

    def test_generate_project_template_not_found(self):
        """Test project generation when a template is not found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom template directory without required templates
            custom_template_dir = Path(temp_dir) / "missing_templates"
            custom_template_dir.mkdir()

            generator = TemplateGenerator(str(custom_template_dir))

            # Try to generate project - should fail because templates are missing
            success = generator.generate_project(
                "test_project",
                temp_dir,
                {
                    "project_name": "test_project",
                    "exchange": "binance",
                    "strategy": "ema",
                    "market_type": "spot",
                    "version": "0.1.0",
                    "description": "Test project",
                    "author_name": "Test Author",
                    "author_email": "test@example.com",
                },
            )
            # This should fail because required templates are missing
            assert success is False

    def test_render_template_to_file_error_handling(self):
        """Test error handling in _render_template_to_file method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom template with syntax error
            custom_template_dir = Path(temp_dir) / "bad_templates"
            custom_template_dir.mkdir()

            # Create a template with Jinja2 syntax error
            template_content = "{{ invalid syntax here"
            template_path = custom_template_dir / "bad.py.j2"
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(template_content)

            generator = TemplateGenerator(str(custom_template_dir))

            # Try to generate project - should handle syntax error gracefully
            success = generator.generate_project("test_project", temp_dir, {})
            # This should fail gracefully, not raise an exception
            assert success is False

    def test_process_templates_exception_handling(self):
        """Test exception handling in _process_templates method."""
        with patch("pathlib.Path.glob", side_effect=OSError("Permission denied")):
            generator = TemplateGenerator()

            success = generator._process_templates(Path("/fake/path"), {})
            assert success is False

    def test_copy_static_files_exception_handling(self):
        """Test exception handling in _copy_static_files method."""
        with patch("pathlib.Path.iterdir", side_effect=OSError("Permission denied")):
            generator = TemplateGenerator()

            success = generator._copy_static_files(Path("/fake/path"))
            assert success is False

    def test_list_available_templates_exception_handling(self):
        """Test exception handling in list_available_templates method."""
        with patch("pathlib.Path.glob", side_effect=OSError("Permission denied")):
            generator = TemplateGenerator()

            templates = generator.list_available_templates()
            assert templates == []
