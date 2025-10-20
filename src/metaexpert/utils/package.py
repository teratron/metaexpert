import subprocess
import sys
import traceback
from pathlib import Path

from packaging.version import parse as parse_version

from metaexpert.logger import get_logger

logger = get_logger()


def get_python_path() -> str | None:
    """Returns the path to the executable Python file in the current virtual environment.

    Returns:
        The absolute path to the Python executable, or None if an error occurs.
    """
    try:
        return sys.executable
    except Exception as e:
        logger.error("Error getting Python executable path: %s", e)
        return None


def get_venv_path() -> Path | None:
    """Returns the root path of the project's virtual environment.

    Detects if the code is running inside a virtual environment by checking system attributes.

    Returns:
        A Path object to the virtual environment's root, or None if not in a venv.
    """
    try:
        if hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        ):
            return Path(sys.prefix)
        return None
    except Exception as e:
        logger.error("Error determining virtual environment path: %s", e)
        return None


def get_lib_path() -> Path | None:
    """Returns the path to the 'lib' or 'Lib' directory of the virtual environment.

    The directory name depends on the operating system ('Lib' for Windows, 'lib' otherwise).

    Returns:
        A Path object to the library directory, or None if not found.
    """
    lib_name: str = "Lib" if sys.platform.startswith("win") else "lib"

    try:
        venv_path = get_venv_path()
        if not venv_path:
            logger.warning("Virtual environment not detected.")
            return None

        lib_path: Path = venv_path / lib_name

        if not lib_path.exists():
            logger.error("Directory '%s' not found in %s", lib_name, venv_path)
            return None

        logger.debug("Path to '%s': %s", lib_name, lib_path)
        return lib_path

    except Exception as e:
        logger.error("Error determining path to '%s': %s", lib_name, e)
        return None


def get_packages_path() -> Path | None:
    """Returns the path to the 'site-packages' directory of the virtual environment.

    This is the standard location for installed third-party packages.

    Returns:
        A Path object to the 'site-packages' directory, or None if not found.
    """
    try:
        lib_path = get_lib_path()
        if not lib_path:
            logger.warning("Virtual environment library path not found.")
            return None

        pkg_path: Path = lib_path / "site-packages"

        logger.debug("Path to 'site-packages': %s", pkg_path)
        return pkg_path

    except Exception as e:
        logger.error("Error determining path to 'site-packages': %s", e)
        return None


def get_bin_path() -> Path | None:
    """Returns the path to the 'bin' or 'Scripts' directory of the virtual environment.

    This directory contains executable files. The name is 'Scripts' on Windows and 'bin' otherwise.

    Returns:
        A Path object to the executables directory, or None if not found.
    """
    bin_name: str = "Scripts" if sys.platform.startswith("win") else "bin"

    try:
        venv_path = get_venv_path()
        if not venv_path:
            logger.warning("Virtual environment not detected.")
            return None

        bin_path = venv_path / bin_name

        if not bin_path.exists():
            logger.error("Directory '%s' not found in %s", bin_name, venv_path)
            return None

        logger.debug("Path to '%s': %s", bin_name, bin_path)
        return bin_path

    except Exception as e:
        logger.error("Error determining path to '%s': %s", bin_name, e)
        return None


def get_pip_path() -> str:
    """Returns the path to the 'pip' executable in the virtual environment.

    Falls back to 'pip' if the exact path cannot be determined, relying on the system's PATH.

    Returns:
        The path to the 'pip' executable as a string.
    """
    try:
        bin_path = get_bin_path()
        if not bin_path:
            return "pip"

        pip_name = "pip.exe" if sys.platform.startswith("win") else "pip"
        pip_path = bin_path / pip_name

        if not pip_path.exists():
            logger.error("Executable 'pip' not found in %s", bin_path)
            return "pip"

        logger.debug("Path to 'pip': %s", pip_path)
        return str(pip_path)

    except Exception as e:
        logger.error("Error determining path to 'pip': %s", e)
        return "pip"


def is_package_installed(name: str) -> bool:
    """Checks if a package is installed in the virtual environment.

    First, it checks the 'site-packages' directory. If not found, it falls back to 'pip show'.

    Args:
        name: The name of the package (e.g., 'requests').

    Returns:
        True if the package is installed, False otherwise.
    """
    try:
        pkg_path = get_packages_path()
        if pkg_path and pkg_path.exists():
            # Normalize package name for directory checking
            normalized_name = name.replace("-", "_").replace(" ", "_")
            for pkg in pkg_path.iterdir():
                if pkg.is_dir() and pkg.name.startswith(normalized_name):
                    logger.debug("Package '%s' found in %s", name, pkg_path)
                    return True
        else:
            logger.warning("Package path not found, falling back to 'pip show'.")

        # Fallback to 'pip show' if directory check fails
        result = subprocess.run(
            [get_pip_path(), "show", name],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        logger.warning("Error checking if package '%s' is installed: %s", name, e)
        print(traceback.format_exc())
        return False


def get_package_version(name: str) -> str | None:
    """Returns the version of an installed package.

    Args:
        name: The name of the package.

    Returns:
        The package version as a string, or None if the package is not found.
    """
    try:
        result = subprocess.run(
            [get_pip_path(), "show", name],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    return line.split(": ")[1].strip()
        return None
    except Exception as e:
        logger.error("Error retrieving version for package '%s': %s", name, e)
        return None


def compare_package_versions(name: str, required_version: str) -> bool:
    """Compares the installed version of a package with a required version.

    Args:
        name: The name of the package.
        required_version: The minimum required version string (e.g., "2.25.1").

    Returns:
        - True if the installed version is greater than or equal to the required version.
        - False if the package is not installed or the version is lower.
    """
    try:
        installed_version_str = get_package_version(name)
        if not installed_version_str:
            logger.warning("Package '%s' not installed.", name)
            return False

        installed_version = parse_version(installed_version_str)
        required_version_parsed = parse_version(required_version)

        if installed_version >= required_version_parsed:
            logger.info("Version %s >= %s", installed_version, required_version)
            return True
        else:
            logger.warning(
                "Installed version %s of package '%s' is lower than required version %s.",
                installed_version,
                name,
                required_version,
            )
            return False

    except Exception as e:
        logger.error("Error comparing versions for package '%s': %s", name, e)
        return False


def install_package(name: str, version: str | None = None) -> None:
    """Installs a package from PyPI using pip into the virtual environment's site-packages.

    Args:
        name: The name of the package to install.
        version: The specific version to install. If None, the latest version is installed.
    """
    if is_package_installed(name):
        logger.debug("Package '%s' is already installed.", name)
        return

    try:
        pkg_path = get_packages_path()
        if not pkg_path:
            raise FileNotFoundError("Target 'site-packages' directory not found.")

        package_spec = f"{name}=={version}" if version else name
        pip_path = get_pip_path()
        result = subprocess.run(
            [
                pip_path,
                "install",
                package_spec,
                "--target",
                str(pkg_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("Package '%s' installed successfully.", name)
        logger.debug("Pip output: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Error installing package '%s': %s\n%s", name, e, e.stderr)
    except FileNotFoundError as e:
        logger.error(
            "Error: 'pip' executable not found or site-packages does not exist. %s", e
        )
    except Exception as e:
        logger.error("An unexpected error occurred during package installation: %s", e)
