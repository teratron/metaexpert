"""Unit tests for the package utility functions."""

import subprocess
from pathlib import Path
from unittest.mock import Mock, PropertyMock, patch

import pytest

from metaexpert.utils.package import (
    compare_package_versions,
    get_bin_path,
    get_lib_path,
    get_package_version,
    get_packages_path,
    get_pip_path,
    get_python_path,
    get_venv_path,
    install_package,
    is_package_installed,
)


@pytest.fixture
def mock_subprocess_run():
    """Fixture to mock subprocess.run."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_path_iterdir():
    """Fixture to mock Path.iterdir."""
    with patch.object(Path, "iterdir") as mock_iterdir:
        yield mock_iterdir


@pytest.fixture
def mock_sys_platform():
    """Fixture to mock sys.platform."""
    with patch("metaexpert.utils.package.sys"):
        yield


class TestGetPackageVersion:
    """Tests for get_package_version function."""

    def test_get_package_version_success(self, mock_subprocess_run):
        """Test that get_package_version returns the correct version when package is found."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Name: requests\nVersion: 2.28.1\nLocation: somewhere\n"
        mock_subprocess_run.return_value = mock_result

        version = get_package_version("requests")

        assert version == "2.28.1"
        mock_subprocess_run.assert_called_once()

    def test_get_package_version_package_not_found(self, mock_subprocess_run):
        """Test that get_package_version returns None when package is not found."""
        mock_result = Mock()
        mock_result.returncode = 1  # pip show failed
        mock_result.stdout = ""
        mock_subprocess_run.return_value = mock_result

        version = get_package_version("nonexistent_package")

        assert version is None
        mock_subprocess_run.assert_called_once()

    def test_get_package_version_exception(self, mock_subprocess_run):
        """Test that get_package_version returns None when an exception occurs."""
        mock_subprocess_run.side_effect = Exception("Subprocess error")

        version = get_package_version("requests")

        assert version is None
        mock_subprocess_run.assert_called_once()


class TestIsPackageInstalled:
    """Tests for is_package_installed function."""

    @patch("metaexpert.utils.package.get_packages_path")
    def test_is_package_installed_by_directory_found(
        self, mock_get_packages_path, mock_path_iterdir
    ):
        """Test that is_package_installed returns True when package is found in site-packages."""
        mock_pkg_path = Mock()
        mock_pkg_path.exists.return_value = True
        mock_get_packages_path.return_value = mock_pkg_path

        mock_pkg_dir = Mock()
        mock_pkg_dir.is_dir.return_value = True
        mock_pkg_dir.name = "requests-2.28.1.dist-info"

        # Mock the iterdir call on the pkg_path instance returned by get_packages_path
        mock_pkg_path.iterdir.return_value = [mock_pkg_dir]

        result = is_package_installed("requests")

        assert result is True
        mock_pkg_path.exists.assert_called_once()
        mock_pkg_path.iterdir.assert_called_once()
        # We don't assert mock_path_iterdir.assert_called_once() because it's an iterator mock
        # The actual call is mock_pkg_path.iterdir(), which is asserted above

    @patch("subprocess.run")
    @patch("metaexpert.utils.package.get_pip_path")
    @patch("metaexpert.utils.package.get_packages_path")
    def test_is_package_installed_by_directory_not_found(
        self,
        mock_get_packages_path,
        mock_get_pip_path,
        mock_subprocess_run,
        mock_path_iterdir,
    ):
        """Test that is_package_installed returns False when package is not found in site-packages and pip show fails."""
        mock_pkg_path = Mock()
        mock_pkg_path.exists.return_value = True
        mock_get_packages_path.return_value = mock_pkg_path

        mock_pkg_dir = Mock()
        mock_pkg_dir.is_dir.return_value = True
        mock_pkg_dir.name = "other_package-1.0.dist-info"

        # Mock the iterdir call on the pkg_path instance returned by get_packages_path
        mock_pkg_path.iterdir.return_value = [mock_pkg_dir]

        # Mock pip show to fail (return code 1)
        mock_result = Mock()
        mock_result.returncode = 1
        mock_subprocess_run.return_value = mock_result
        mock_get_pip_path.return_value = "pip"

        result = is_package_installed("requests")

        assert result is False
        mock_pkg_path.exists.assert_called_once()
        mock_pkg_path.iterdir.assert_called_once()
        mock_get_pip_path.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            ["pip", "show", "requests"],
            check=False,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    @patch("metaexpert.utils.package.get_pip_path")
    @patch("metaexpert.utils.package.get_packages_path")
    def test_is_package_installed_fallback_pip_show_found(
        self, mock_get_packages_path, mock_get_pip_path, mock_subprocess_run
    ):
        """Test that is_package_installed returns True when package is not found in directory but pip show succeeds."""
        mock_get_packages_path.return_value = None  # get_packages_path returns None

        mock_result = Mock()
        mock_result.returncode = 0  # pip show succeeded
        mock_subprocess_run.return_value = mock_result
        mock_get_pip_path.return_value = "pip"

        result = is_package_installed("requests")

        assert result is True
        mock_get_packages_path.assert_called_once()
        mock_get_pip_path.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            ["pip", "show", "requests"],
            check=False,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    @patch("metaexpert.utils.package.get_pip_path")
    @patch("metaexpert.utils.package.get_packages_path")
    def test_is_package_installed_fallback_pip_show_not_found(
        self, mock_get_packages_path, mock_get_pip_path, mock_subprocess_run
    ):
        """Test that is_package_installed returns False when pip show fails."""
        mock_get_packages_path.return_value = None  # get_packages_path returns None

        mock_result = Mock()
        mock_result.returncode = 1  # pip show failed
        mock_subprocess_run.return_value = mock_result
        mock_get_pip_path.return_value = "pip"

        result = is_package_installed("requests")

        assert result is False
        mock_get_packages_path.assert_called_once()
        mock_get_pip_path.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            ["pip", "show", "requests"],
            check=False,
            capture_output=True,
            text=True,
        )

    @patch("metaexpert.utils.package.get_packages_path")
    def test_is_package_installed_exception(self, mock_get_packages_path):
        """Test that is_package_installed returns False when an exception occurs."""
        mock_get_packages_path.side_effect = Exception("Path error")

        result = is_package_installed("requests")

        assert result is False
        mock_get_packages_path.assert_called_once_with()


class TestComparePackageVersions:
    """Tests for compare_package_versions function."""

    @patch("metaexpert.utils.package.get_package_version")
    def test_compare_package_versions_greater(self, mock_get_version):
        """Test that compare_package_versions returns True when installed version is greater."""
        mock_get_version.return_value = "2.29.0"

        result = compare_package_versions("requests", "2.28.1")

        assert result is True
        mock_get_version.assert_called_once_with("requests")

    @patch("metaexpert.utils.package.get_package_version")
    def test_compare_package_versions_equal(self, mock_get_version):
        """Test that compare_package_versions returns True when installed version is equal."""
        mock_get_version.return_value = "2.28.1"

        result = compare_package_versions("requests", "2.28.1")

        assert result is True
        mock_get_version.assert_called_once_with("requests")

    @patch("metaexpert.utils.package.get_package_version")
    def test_compare_package_versions_less(self, mock_get_version):
        """Test that compare_package_versions returns False when installed version is less."""
        mock_get_version.return_value = "2.27.0"

        result = compare_package_versions("requests", "2.28.1")

        assert result is False
        mock_get_version.assert_called_once_with("requests")

    @patch("metaexpert.utils.package.get_package_version")
    def test_compare_package_versions_package_not_installed(self, mock_get_version):
        """Test that compare_package_versions returns False when package is not installed."""
        mock_get_version.return_value = None

        result = compare_package_versions("requests", "2.28.1")

        assert result is False
        mock_get_version.assert_called_once_with("requests")

    @patch("metaexpert.utils.package.get_package_version")
    def test_compare_package_versions_exception(self, mock_get_version):
        """Test that compare_package_versions returns False when an exception occurs."""
        mock_get_version.side_effect = Exception("Version error")

        result = compare_package_versions("requests", "2.28.1")

        assert result is False
        mock_get_version.assert_called_once_with("requests")


class TestInstallPackage:
    """Tests for install_package function."""

    @patch("metaexpert.utils.package.is_package_installed")
    @patch("metaexpert.utils.package.get_packages_path")
    def test_install_package_already_installed(
        self, mock_get_packages_path, mock_is_installed
    ):
        """Test that install_package does nothing if package is already installed."""
        mock_is_installed.return_value = True

        install_package("requests")

        mock_is_installed.assert_called_once_with("requests")
        mock_get_packages_path.assert_not_called()

    @patch("metaexpert.utils.package.is_package_installed")
    @patch("metaexpert.utils.package.get_packages_path")
    @patch("subprocess.run")
    def test_install_package_success_latest_version(
        self, mock_subprocess_run, mock_get_packages_path, mock_is_installed
    ):
        """Test that install_package calls subprocess.run correctly for latest version."""
        mock_is_installed.return_value = False
        mock_get_packages_path.return_value = Path("/fake/venv/lib/site-packages")
        mock_result = Mock()
        mock_result.stdout = "Successfully installed requests"
        mock_subprocess_run.return_value = mock_result

        install_package("requests")

        mock_is_installed.assert_called_once_with("requests")
        mock_get_packages_path.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            [
                "pip",
                "install",
                "requests",
                "--target",
                str(Path("/fake/venv/lib/site-packages")),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("metaexpert.utils.package.is_package_installed")
    @patch("metaexpert.utils.package.get_packages_path")
    @patch("subprocess.run")
    def test_install_package_success_specific_version(
        self, mock_subprocess_run, mock_get_packages_path, mock_is_installed
    ):
        """Test that install_package calls subprocess.run correctly for specific version."""
        mock_is_installed.return_value = False
        mock_get_packages_path.return_value = Path("/fake/venv/lib/site-packages")
        mock_result = Mock()
        mock_result.stdout = "Successfully installed requests==2.28.1"
        mock_subprocess_run.return_value = mock_result

        install_package("requests", version="2.28.1")

        mock_is_installed.assert_called_once_with("requests")
        mock_get_packages_path.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            [
                "pip",
                "install",
                "requests==2.28.1",
                "--target",
                str(Path("/fake/venv/lib/site-packages")),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("metaexpert.utils.package.is_package_installed")
    @patch("metaexpert.utils.package.get_packages_path")
    @patch("subprocess.run")
    def test_install_package_called_process_error(
        self, mock_subprocess_run, mock_get_packages_path, mock_is_installed
    ):
        """Test that install_package handles CalledProcessError."""
        mock_is_installed.return_value = False
        mock_get_packages_path.return_value = Path("/fake/venv/lib/site-packages")
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            1, "pip install"
        )

        install_package("requests")

        mock_is_installed.assert_called_once_with("requests")
        mock_get_packages_path.assert_called_once()
        mock_subprocess_run.assert_called_once()

    @patch("metaexpert.utils.package.is_package_installed")
    @patch("metaexpert.utils.package.get_packages_path")
    def test_install_package_file_not_found_error(
        self, mock_get_packages_path, mock_is_installed
    ):
        """Test that install_package handles FileNotFoundError when site-packages is not found."""
        mock_is_installed.return_value = False
        mock_get_packages_path.return_value = None  # get_packages_path returns None

        install_package("requests")

        mock_is_installed.assert_called_once_with("requests")
        mock_get_packages_path.assert_called_once()


class TestGetPythonPath:
    """Tests for get_python_path function."""

    @patch("metaexpert.utils.package.sys")
    def test_get_python_path_success(self, mock_sys):
        """Test that get_python_path returns the correct Python executable path."""
        mock_sys.executable = "/path/to/python"

        result = get_python_path()

        assert result == "/path/to/python"

    @patch("metaexpert.utils.package.sys")
    def test_get_python_path_exception(self, mock_sys):
        """Test that get_python_path returns None when an exception occurs."""
        type(mock_sys).executable = PropertyMock(side_effect=Exception("Error"))

        result = get_python_path()

        assert result is None


class TestGetVenvPath:
    """Tests for get_venv_path function."""

    @patch("metaexpert.utils.package.sys")
    def test_get_venv_path_with_real_prefix(self, mock_sys):
        """Test that get_venv_path returns the correct path when real_prefix exists."""
        with patch("builtins.hasattr") as mock_hasattr:

            def hasattr_side_effect(obj, name):
                if name == "real_prefix":
                    return True
                elif name == "base_prefix":
                    return True
                else:
                    return object.__getattribute__(
                        obj, "__class__"
                    ).__dict__.__contains__(name)

            mock_hasattr.side_effect = hasattr_side_effect
            mock_sys.real_prefix = "/path/to/venv"
            mock_sys.base_prefix = "/original/python"
            mock_sys.prefix = "/path/to/venv"

            result = get_venv_path()

            assert result == Path("/path/to/venv")
            # Verify hasattr was called for real_prefix (it should return True and exit early)
            mock_hasattr.assert_any_call(mock_sys, "real_prefix")

    @patch("metaexpert.utils.package.sys")
    def test_get_venv_path_with_different_base_prefix(self, mock_sys):
        """Test that get_venv_path returns the correct path when base_prefix != prefix."""
        # Mock hasattr to return False for 'real_prefix' but True for 'base_prefix'
        with patch("builtins.hasattr") as mock_hasattr:

            def hasattr_side_effect(obj, name):
                if name == "real_prefix":
                    return False
                elif name == "base_prefix":
                    return True
                else:
                    return object.__getattribute__(
                        obj, "__class__"
                    ).__dict__.__contains__(name)

            mock_hasattr.side_effect = hasattr_side_effect
            mock_sys.base_prefix = "/original/python"
            mock_sys.prefix = "/path/to/venv"

            result = get_venv_path()

            assert result == Path("/path/to/venv")
            # Verify hasattr was called appropriately
            mock_hasattr.assert_any_call(mock_sys, "real_prefix")
            mock_hasattr.assert_any_call(mock_sys, "base_prefix")

    @patch("metaexpert.utils.package.sys")
    def test_get_venv_path_no_venv(self, mock_sys):
        """Test that get_venv_path returns None when not in a virtual environment."""
        # Set up sys to have the same base_prefix and prefix, and ensure hasattr returns False for real_prefix
        # We'll mock hasattr to return False for 'real_prefix'
        with patch("builtins.hasattr") as mock_hasattr:
            # Configure hasattr to return False for 'real_prefix', True for 'base_prefix', and call the original for everything else
            def hasattr_side_effect(obj, name):
                if name == "real_prefix":
                    return False
                elif name == "base_prefix":
                    return True
                else:
                    return object.__getattribute__(
                        obj, "__class__"
                    ).__dict__.__contains__(name)

            mock_hasattr.side_effect = hasattr_side_effect
            mock_sys.base_prefix = "/same/python"
            mock_sys.prefix = "/same/python"

            result = get_venv_path()

            assert result is None
            # Verify hasattr was called appropriately
            mock_hasattr.assert_any_call(mock_sys, "real_prefix")
            mock_hasattr.assert_any_call(mock_sys, "base_prefix")

    @patch("metaexpert.utils.package.sys")
    def test_get_venv_path_exception(self, mock_sys):
        """Test that get_venv_path returns None when an exception occurs."""
        type(mock_sys).prefix = PropertyMock(side_effect=Exception("Error"))

        result = get_venv_path()

        assert result is None


class TestGetLibPath:
    """Tests for get_lib_path function."""

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_lib_path_linux(self, mock_sys, mock_get_venv_path):
        """Test that get_lib_path returns the correct path on Linux."""
        mock_sys.platform = "linux"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method for the lib path
        with patch.object(Path, "exists", return_value=True):
            result = get_lib_path()

        assert result == Path("/path/to/venv/lib")

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_lib_path_windows(self, mock_sys, mock_get_venv_path):
        """Test that get_lib_path returns the correct path on Windows."""
        mock_sys.platform = "win32"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method for the lib path
        with patch.object(Path, "exists", return_value=True):
            result = get_lib_path()

        assert result == Path("/path/to/venv/Lib")

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_lib_path_no_venv(self, mock_sys, mock_get_venv_path):
        """Test that get_lib_path returns None when no virtual environment is detected."""
        mock_get_venv_path.return_value = None

        result = get_lib_path()

        assert result is None
        mock_get_venv_path.assert_called_once()

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_lib_path_no_lib_dir(self, mock_sys, mock_get_venv_path):
        """Test that get_lib_path returns None when the lib directory doesn't exist."""
        mock_sys.platform = "linux"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method to return False
        with patch.object(Path, "exists", return_value=False):
            result = get_lib_path()

        assert result is None

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_lib_path_exception(self, mock_sys, mock_get_venv_path):
        """Test that get_lib_path returns None when an exception occurs."""
        mock_get_venv_path.return_value = Path("/path/to/venv")
        # Make Path operations raise an exception
        with patch.object(Path, "__truediv__", side_effect=Exception("Error")):
            result = get_lib_path()

        assert result is None


class TestGetPackagesPath:
    """Tests for get_packages_path function."""

    @patch("metaexpert.utils.package.get_lib_path")
    def test_get_packages_path_success(self, mock_get_lib_path):
        """Test that get_packages_path returns the correct site-packages path."""
        mock_get_lib_path.return_value = Path("/path/to/venv/lib")

        result = get_packages_path()

        assert result == Path("/path/to/venv/lib/site-packages")
        mock_get_lib_path.assert_called_once()

    @patch("metaexpert.utils.package.get_lib_path")
    def test_get_packages_path_no_lib_path(self, mock_get_lib_path):
        """Test that get_packages_path returns None when get_lib_path returns None."""
        mock_get_lib_path.return_value = None

        result = get_packages_path()

        assert result is None
        mock_get_lib_path.assert_called_once()

    @patch("metaexpert.utils.package.get_lib_path")
    def test_get_packages_path_exception(self, mock_get_lib_path):
        """Test that get_packages_path returns None when an exception occurs."""
        mock_get_lib_path.return_value = Path("/path/to/venv/lib")
        # Make Path operations raise an exception
        with patch.object(Path, "__truediv__", side_effect=Exception("Error")):
            result = get_packages_path()

        assert result is None


class TestGetBinPath:
    """Tests for get_bin_path function."""

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_bin_path_linux(self, mock_sys, mock_get_venv_path):
        """Test that get_bin_path returns the correct path on Linux."""
        mock_sys.platform = "linux"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method for the bin path
        with patch.object(Path, "exists", return_value=True):
            result = get_bin_path()

        assert result == Path("/path/to/venv/bin")

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_bin_path_windows(self, mock_sys, mock_get_venv_path):
        """Test that get_bin_path returns the correct path on Windows."""
        mock_sys.platform = "win32"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method for the bin path
        with patch.object(Path, "exists", return_value=True):
            result = get_bin_path()

        assert result == Path("/path/to/venv/Scripts")

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_bin_path_no_venv(self, mock_sys, mock_get_venv_path):
        """Test that get_bin_path returns None when no virtual environment is detected."""
        mock_get_venv_path.return_value = None

        result = get_bin_path()

        assert result is None
        mock_get_venv_path.assert_called_once()

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_bin_path_no_bin_dir(self, mock_sys, mock_get_venv_path):
        """Test that get_bin_path returns None when the bin directory doesn't exist."""
        mock_sys.platform = "linux"
        mock_get_venv_path.return_value = Path("/path/to/venv")

        # Mock the exists method to return False
        with patch.object(Path, "exists", return_value=False):
            result = get_bin_path()

        assert result is None

    @patch("metaexpert.utils.package.get_venv_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_bin_path_exception(self, mock_sys, mock_get_venv_path):
        """Test that get_bin_path returns None when an exception occurs."""
        mock_get_venv_path.return_value = Path("/path/to/venv")
        # Make Path operations raise an exception
        with patch.object(Path, "__truediv__", side_effect=Exception("Error")):
            result = get_bin_path()

        assert result is None


class TestGetPipPath:
    """Tests for get_pip_path function."""

    @patch("metaexpert.utils.package.get_bin_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_pip_path_linux_success(self, mock_sys, mock_get_bin_path):
        """Test that get_pip_path returns the correct pip path on Linux."""
        mock_sys.platform = "linux"
        mock_get_bin_path.return_value = Path("/path/to/venv/bin")

        # Mock the exists method for the pip path
        with patch.object(Path, "exists", return_value=True):
            result = get_pip_path()

        # Use Path to normalize the path comparison
        assert result == str(Path("/path/to/venv/bin/pip"))

    @patch("metaexpert.utils.package.get_bin_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_pip_path_windows_success(self, mock_sys, mock_get_bin_path):
        """Test that get_pip_path returns the correct pip path on Windows."""
        mock_sys.platform = "win32"
        mock_get_bin_path.return_value = Path("/path/to/venv/Scripts")

        # Mock the exists method for the pip path
        with patch.object(Path, "exists", return_value=True):
            result = get_pip_path()

        # Use Path to normalize the path comparison
        assert result == str(Path("/path/to/venv/Scripts/pip.exe"))

    @patch("metaexpert.utils.package.get_bin_path")
    def test_get_pip_path_no_bin_path(self, mock_get_bin_path):
        """Test that get_pip_path returns default 'pip' when get_bin_path returns None."""
        mock_get_bin_path.return_value = None

        result = get_pip_path()

        assert result == "pip"
        mock_get_bin_path.assert_called_once()

    @patch("metaexpert.utils.package.get_bin_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_pip_path_no_pip_file(self, mock_sys, mock_get_bin_path):
        """Test that get_pip_path returns default 'pip' when pip executable doesn't exist."""
        mock_sys.platform = "linux"
        mock_get_bin_path.return_value = Path("/path/to/venv/bin")

        # Mock the exists method to return False
        with patch.object(Path, "exists", return_value=False):
            result = get_pip_path()

        assert result == "pip"

    @patch("metaexpert.utils.package.get_bin_path")
    @patch("metaexpert.utils.package.sys")
    def test_get_pip_path_exception(self, mock_sys, mock_get_bin_path):
        """Test that get_pip_path returns default 'pip' when an exception occurs."""
        mock_get_bin_path.return_value = Path("/path/to/venv/bin")
        # Make Path operations raise an exception
        with patch.object(Path, "__truediv__", side_effect=Exception("Error")):
            result = get_pip_path()

        assert result == "pip"
