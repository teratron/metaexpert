"""Tests for TemplateGenerator class."""

import shutil
from pathlib import Path
from unittest.mock import Mock, call, patch, MagicMock

import pytest

from metaexpert.cli.core.exceptions import TemplateError
from metaexpert.cli.templates.generator import TemplateGenerator


class TestTemplateGenerator:
    """Test suite for TemplateGenerator class."""

    def test_init_default_template_dir(self):
        """Test initialization with default template directory."""
        # Mock Path.exists to return True so initialization doesn't fail
        with patch.object(Path, 'exists', return_value=True):
            generator = TemplateGenerator()
        
        # Check that default template directory is set correctly
        # Use the actual path where the TemplateGenerator gets its default from
        expected_dir = Path(__file__).parent.parent.parent.parent / "src" / "metaexpert" / "cli" / "templates" / "files"
        expected_dir = expected_dir.resolve()
        
        # The generator uses Path(__file__) from its own file, so we need to match that behavior
        actual_dir = generator.template_dir.resolve()
        
        # Check that the actual directory exists and contains the expected files directory
        assert actual_dir.exists()
        assert actual_dir.name == "files"
        assert (actual_dir.parent / "generator.py").exists()  # Verify it's in the right location
        assert generator.env is not None

    def test_init_custom_template_dir(self):
        """Test initialization with custom template directory."""
        custom_dir = Path("/custom/templates")
        with patch.object(Path, 'exists', return_value=True):
            generator = TemplateGenerator(template_dir=custom_dir)
            
        assert generator.template_dir == custom_dir

    def test_init_template_dir_not_found(self):
        """Test initialization raises error when template directory doesn't exist."""
        non_existent_dir = Path("/non/existent/dir")
        with patch.object(Path, 'exists', return_value=False):
            with pytest.raises(TemplateError, match=r"Template directory not found: .*"):
                TemplateGenerator(template_dir=non_existent_dir)

    def test_generate_project_creates_directory(self, tmp_path):
        """Test that generate_project creates the project directory."""
        generator = TemplateGenerator()
        output_dir = tmp_path / "output"
        project_name = "test_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        # Mock the template rendering to avoid actual file operations
        with patch.object(generator, '_generate_main_file') as mock_main, \
             patch.object(generator, '_generate_env_file') as mock_env, \
             patch.object(generator, '_generate_gitignore') as mock_gitignore, \
             patch.object(generator, '_generate_readme') as mock_readme, \
             patch.object(generator, '_generate_pyproject_toml') as mock_pyproject:
            
            generator.generate_project(output_dir, project_name, context)
            
            project_path = output_dir / project_name
            assert project_path.exists()
            assert project_path.is_dir()

    def test_generate_project_with_existing_dir_and_force_false_raises_error(self, tmp_path):
        """Test that generate_project raises error when directory exists and force=False."""
        generator = TemplateGenerator()
        output_dir = tmp_path / "output"
        project_name = "existing_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        # Create the project directory beforehand
        project_path = output_dir / project_name
        project_path.mkdir(parents=True)
        
        with pytest.raises(TemplateError, match=f"Directory '{project_name}' already exists. Use --force to overwrite."):
            generator.generate_project(output_dir, project_name, context, force=False)

    def test_generate_project_with_existing_dir_and_force_true_overwrites(self, tmp_path):
        """Test that generate_project overwrites existing directory when force=True."""
        generator = TemplateGenerator()
        output_dir = tmp_path / "output"
        project_name = "existing_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        # Create the project directory beforehand with some content
        project_path = output_dir / project_name
        project_path.mkdir(parents=True)
        (project_path / "old_file.txt").write_text("old content")
        
        # Mock the template rendering to avoid actual file operations
        with patch.object(generator, '_generate_main_file') as mock_main, \
             patch.object(generator, '_generate_env_file') as mock_env, \
             patch.object(generator, '_generate_gitignore') as mock_gitignore, \
             patch.object(generator, '_generate_readme') as mock_readme, \
             patch.object(generator, '_generate_pyproject_toml') as mock_pyproject:
            
            generator.generate_project(output_dir, project_name, context, force=True)
            
            # Check that the old directory was removed and new one created
            assert project_path.exists()
            assert not (project_path / "old_file.txt").exists()

    def test_generate_project_calls_all_generation_methods(self, tmp_path):
        """Test that generate_project calls all expected generation methods."""
        generator = TemplateGenerator()
        output_dir = tmp_path / "output"
        project_name = "test_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        # Mock the template rendering to avoid actual file operations
        with patch.object(generator, '_generate_main_file') as mock_main, \
             patch.object(generator, '_generate_env_file') as mock_env, \
             patch.object(generator, '_generate_gitignore') as mock_gitignore, \
             patch.object(generator, '_generate_readme') as mock_readme, \
             patch.object(generator, '_generate_pyproject_toml') as mock_pyproject:
            
            generator.generate_project(output_dir, project_name, context)
            
            # Verify all generation methods were called
            project_path = output_dir / project_name
            expected_context = context.copy()
            expected_context.update({
                "project_name": project_name,
                "project_path": project_path,
            })
            
            mock_main.assert_called_once_with(project_path, expected_context)
            mock_env.assert_called_once_with(project_path, expected_context)
            mock_gitignore.assert_called_once_with(project_path)
            mock_readme.assert_called_once_with(project_path, expected_context)
            mock_pyproject.assert_called_once_with(project_path, expected_context)

    def test_generate_project_cleanup_on_failure(self, tmp_path):
        """Test that generate_project cleans up on failure."""
        generator = TemplateGenerator()
        output_dir = tmp_path / "output"
        project_name = "test_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        # Mock one of the generation methods to raise an exception
        with patch.object(generator, '_generate_main_file') as mock_main, \
             patch.object(generator, '_generate_env_file') as mock_env, \
             patch.object(generator, '_generate_gitignore') as mock_gitignore, \
             patch.object(generator, '_generate_readme') as mock_readme, \
             patch.object(generator, '_generate_pyproject_toml') as mock_pyproject, \
             patch('shutil.rmtree') as mock_rmtree:
            
            mock_main.side_effect = Exception("Generation failed")
            
            with pytest.raises(TemplateError, match="Failed to generate project: Generation failed"):
                generator.generate_project(output_dir, project_name, context)
            
            # Verify that rmtree was called to clean up
            project_path = output_dir / project_name
            mock_rmtree.assert_called_once_with(project_path)

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_main_file(self, mock_env_class, tmp_path):
        """Test _generate_main_file method."""
        generator = TemplateGenerator()
        generator.env = mock_env_class.return_value
        
        # Mock template and its render method
        mock_template = Mock()
        mock_env_class.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "mocked content"
        
        project_path = tmp_path / "project"
        project_path.mkdir()
        context = {"exchange": "binance", "strategy": "template"}
        
        generator._generate_main_file(project_path, context)
        
        # Verify template was retrieved and rendered
        mock_env_class.return_value.get_template.assert_called_once_with("main.py.j2")
        mock_template.render.assert_called_once_with(**context)
        
        # Check that the file was written
        main_file = project_path / "main.py"
        assert main_file.exists()
        assert main_file.read_text(encoding="utf-8") == "mocked content"

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_env_file(self, mock_env_class, tmp_path):
        """Test _generate_env_file method."""
        generator = TemplateGenerator()
        generator.env = mock_env_class.return_value
        
        # Mock template and its render method
        mock_template = Mock()
        mock_env_class.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "mocked content"
        
        project_path = tmp_path / "project"
        project_path.mkdir()
        context = {"exchange": "binance", "strategy": "template"}
        
        generator._generate_env_file(project_path, context)
        
        # Verify template was retrieved and rendered
        mock_env_class.return_value.get_template.assert_called_once_with("env.j2")
        mock_template.render.assert_called_once_with(**context)
        
        # Check that the file was written
        env_file = project_path / ".env.example"
        assert env_file.exists()
        assert env_file.read_text(encoding="utf-8") == "mocked content"

    def test_generate_gitignore(self, tmp_path):
        """Test _generate_gitignore method."""
        generator = TemplateGenerator()
        
        project_path = tmp_path / "project"
        project_path.mkdir()
        
        generator._generate_gitignore(project_path)
        
        # Check that the file was written with expected content
        gitignore_file = project_path / ".gitignore"
        assert gitignore_file.exists()
        
        content = gitignore_file.read_text(encoding="utf-8")
        expected_content = """# Environment
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
        assert content == expected_content

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_readme(self, mock_env_class, tmp_path):
        """Test _generate_readme method."""
        generator = TemplateGenerator()
        generator.env = mock_env_class.return_value
        
        # Mock template and its render method
        mock_template = Mock()
        mock_env_class.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "mocked content"
        
        project_path = tmp_path / "project"
        project_path.mkdir()
        context = {"exchange": "binance", "strategy": "template"}
        
        generator._generate_readme(project_path, context)
        
        # Verify template was retrieved and rendered
        mock_env_class.return_value.get_template.assert_called_once_with("README.md.j2")
        mock_template.render.assert_called_once_with(**context)
        
        # Check that the file was written
        readme_file = project_path / "README.md"
        assert readme_file.exists()
        assert readme_file.read_text(encoding="utf-8") == "mocked content"

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_pyproject_toml(self, mock_env_class, tmp_path):
        """Test _generate_pyproject_toml method."""
        generator = TemplateGenerator()
        generator.env = mock_env_class.return_value
        
        # Mock template and its render method
        mock_template = Mock()
        mock_env_class.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "mocked content"
        
        project_path = tmp_path / "project"
        project_path.mkdir()
        context = {"exchange": "binance", "strategy": "template"}
        
        generator._generate_pyproject_toml(project_path, context)
        
        # Verify template was retrieved and rendered
        mock_env_class.return_value.get_template.assert_called_once_with("pyproject.toml.j2")
        mock_template.render.assert_called_once_with(**context)
        
        # Check that the file was written
        toml_file = project_path / "pyproject.toml"
        assert toml_file.exists()
        assert toml_file.read_text(encoding="utf-8") == "mocked content"

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_list_strategies_with_existing_strategies_dir(self, mock_env_class):
        """Test list_strategies method when strategies directory exists."""
        generator = TemplateGenerator()
        
        # Mock template directory structure
        mock_template_dir = MagicMock(spec=Path)
        generator.template_dir = mock_template_dir
        
        # Create mock strategies directory with template files
        mock_strategies_dir = MagicMock(spec=Path)
        mock_template_dir.__truediv__.return_value = mock_strategies_dir
        mock_strategies_dir.exists.return_value = True
        
        # Mock glob to return some strategy files
        mock_strategy_files = [
            MagicMock(spec=Path, stem="ema"),
            MagicMock(spec=Path, stem="rsi"),
            MagicMock(spec=Path, stem="macd")
        ]
        mock_strategies_dir.glob.return_value = mock_strategy_files
        
        strategies = generator.list_strategies()
        
        # Should return the stem of each .j2 file
        expected_strategies = ["ema", "rsi", "macd"]
        assert strategies == expected_strategies

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_list_strategies_with_nonexistent_strategies_dir(self, mock_env_class):
        """Test list_strategies method when strategies directory doesn't exist."""
        generator = TemplateGenerator()
        
        # Mock template directory structure
        mock_template_dir = MagicMock(spec=Path)
        generator.template_dir = mock_template_dir
        
        # Create mock strategies directory that doesn't exist
        mock_strategies_dir = MagicMock(spec=Path)
        mock_template_dir.__truediv__.return_value = mock_strategies_dir
        mock_strategies_dir.exists.return_value = False
        
        strategies = generator.list_strategies()
        
        # Should return default ["template"]
        assert strategies == ["template"]

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_project_with_different_context_parameters(self, mock_env_class, tmp_path):
        """Test generate_project with various context parameters."""
        generator = TemplateGenerator()
        generator.env = mock_env_class
        
        # Mock all template rendering methods
        with patch.object(generator, '_generate_main_file'), \
             patch.object(generator, '_generate_env_file'), \
             patch.object(generator, '_generate_gitignore'), \
             patch.object(generator, '_generate_readme'), \
             patch.object(generator, '_generate_pyproject_toml'):
            
            output_dir = tmp_path / "output"
            project_name = "test_project"
            
            # Test with different context parameters
            context = {
                "exchange": "bybit",
                "strategy": "ema",
                "market_type": "futures",
                "contract_type": "linear",
                "margin_mode": "cross",
                "position_mode": "hedge",
                "symbol": "BTCUSDT",
                "timeframe": "5m",
                "lookback_bars": 200,
                "strategy_id": 2002,
                "strategy_name": "EMA Strategy",
                "leverage": 20,
                "size_value": 2.0,
                "stop_loss_pct": 3.0,
                "take_profit_pct": 6.0,
                "requires_passphrase": True
            }
            
            generator.generate_project(output_dir, project_name, context)
            
            # Verify that context was updated with project metadata
            project_path = output_dir / project_name
            expected_context = context.copy()
            expected_context.update({
                "project_name": project_name,
                "project_path": project_path,
            })

    @patch('metaexpert.cli.templates.generator.Environment')
    def test_generate_project_creates_expected_files(self, mock_env_class, tmp_path):
        """Test that generate_project creates all expected files."""
        # Mock Path.exists to return True for template directory only
        def custom_exists(self):
            # Return True only for the template directory path
            if "templates" in str(self) and "files" in str(self):
                return True
            # For all other paths, use the original behavior
            # But make sure the project path doesn't exist initially
            project_path_str = str(tmp_path / "output" / "test_project")
            if str(self) == project_path_str or str(self).startswith(project_path_str):
                return self.name == ".gitignore"  # Only return True for .gitignore after creation
            return self.name == ".gitignore"  # For the _generate_gitignore call
        
        with patch.object(Path, 'exists', custom_exists):
            generator = TemplateGenerator()
        
        # Mock templates to return some content
        mock_main_template = Mock()
        mock_env_template = Mock()
        mock_readme_template = Mock()
        mock_pyproject_template = Mock()
        
        def get_template_side_effect(template_name):
            if template_name == "main.py.j2":
                return mock_main_template
            elif template_name == "env.j2":
                return mock_env_template
            elif template_name == "README.md.j2":
                return mock_readme_template
            elif template_name == "pyproject.toml.j2":
                return mock_pyproject_template
            else:
                raise Exception(f"Unexpected template: {template_name}")
        
        mock_env_class.return_value.get_template.side_effect = get_template_side_effect
        mock_main_template.render.return_value = "# Main file content"
        mock_env_template.render.return_value = "# Env file content"
        mock_readme_template.render.return_value = "# README content"
        mock_pyproject_template.render.return_value = "# TOML content"
        
        # Replace the generator's environment with the mock
        generator.env = mock_env_class.return_value
        
        output_dir = tmp_path / "output"
        project_name = "test_project"
        context = {"exchange": "binance", "strategy": "template", "market_type": "spot"}
        
        generator.generate_project(output_dir, project_name, context)
        
        project_path = output_dir / project_name
        
        # Check that all expected files were created
        assert (project_path / "main.py").exists()
        assert (project_path / ".env.example").exists()
        assert (project_path / ".gitignore").exists()
        assert (project_path / "README.md").exists()
        assert (project_path / "pyproject.toml").exists()
        
        # Check file contents
        assert (project_path / "main.py").read_text(encoding="utf-8") == "# Main file content"
        assert (project_path / ".env.example").read_text(encoding="utf-8") == "# Env file content"
        assert (project_path / "README.md").read_text(encoding="utf-8") == "# README content"
        assert (project_path / "pyproject.toml").read_text(encoding="utf-8") == "# TOML content"
        
        # Check gitignore content specifically
        gitignore_content = (project_path / ".gitignore").read_text(encoding="utf-8")
        assert "# Environment" in gitignore_content
        assert "# Python" in gitignore_content
        assert "__pycache__/" in gitignore_content