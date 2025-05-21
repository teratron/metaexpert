import subprocess
import sys
import traceback
from pathlib import Path

import packaging

# import importlib.util
# import pkg_resources
from metaexpert import logger


def get_venv_path() -> Path | None:
    """Returns the way to the virtual environment of the project."""
    try:
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return Path(sys.prefix)
        return None
    except Exception as e:
        logger.error("Error when determining the path of virtual environment: %s", e)
        return None


def get_packages_path() -> Path | None:
    """Возвращает путь к директории lib виртуальной среды."""
    try:
        venv_path = get_venv_path()
        if not venv_path:
            logger.warning("Виртуальная среда не обнаружена")
            return None

        lib_path: Path = venv_path / "lib" / "site-packages"

        if sys.platform == "win32" or sys.platform == "win64":
            lib_path = venv_path / "Lib" / "site-packages"

        if not lib_path.exists():
            logger.error("Директория lib | Lib не найдена в %s", venv_path)
            return None

        logger.debug("Путь к lib | Lib: %s", lib_path)
        return lib_path

    except Exception as e:
        logger.error("Ошибка при определении пути к lib | Lib: %s", e)
        return None


def get_bin_path() -> Path | None:
    """Возвращает путь к директории bin | Scripts виртуальной среды."""
    try:
        venv_path = get_venv_path()
        if not venv_path:
            logger.warning("Виртуальная среда не обнаружена")
            return None

        bin_path: Path = venv_path / "bin"

        if sys.platform == "win32" or sys.platform == "win64":
            bin_path = venv_path / "Scripts"

        if not bin_path.exists():
            logger.error("Директория bin | Scripts не найдена в %s", venv_path)
            return None

        logger.debug("Путь к bin | Scripts: %s", bin_path)
        return bin_path

    except Exception as e:
        logger.error("Ошибка при определении пути к bin | Scripts: %s", e)
        return None


def get_python_path() -> str | None:
    """Returns the way to the executable Python file in a virtual environment."""
    try:
        return sys.executable
    except Exception as e:
        logger.error("Error when getting a path to Python: %s", e)
        return None


def get_pip_path() -> str:
    """Возвращает путь к исполняемому файлу pip в виртуальной среде."""
    try:
        bin_path = get_bin_path()
        if not bin_path:
            return "pip"

        pip_name = "pip.exe" if sys.platform.startswith("win") else "pip"
        pip_path = bin_path / pip_name

        if not pip_path.exists():
            logger.error("Файл pip не найден в %s", bin_path)
            return "pip"

        logger.debug("Путь к pip: %s", pip_path)
        return str(pip_path)

    except Exception as e:
        logger.error("Ошибка при определении пути к pip: %s", e)
        return "pip"


def is_package_installed(name: str) -> bool:
    """Checks whether the package is installed in the virtual environment."""
    try:
        # Способ 1: через importlib
        # spec = importlib.util.find_spec(name)
        # if spec is not None:
        #     return True
        # return False

        # Способ 2: через pkg_resources
        # pkg_resources.get_distribution(name)
        # return True

        result = subprocess.run(
            [get_pip_path(), "show", name],  # , "--require-virtualenv", "--isolated"
            check=False,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.warning("Mistake when checking the package: %s", e)
        print(traceback.format_exc())
        return False


def get_package_version(name: str) -> str | None:
    """Returns the version of the established package or None if the package is not installed."""
    try:
        result = subprocess.run(
            ["pip", "show", name],
            check=False,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    return line.split(": ")[1]
        return None
    except Exception as e:
        logger.error("Error retrieving version for package '%s': %s", name, e)
        return None


def compare_package_versions(name: str, required_version: str) -> bool:
    """Сравнивает установленную версию пакета с требуемой.

    Args:
        name: Имя пакета
        required_version: Требуемая версия

    Returns:
        bool: результат сравнения
        - True если установленная версия >= требуемой
        - False если пакет не установлен или версия < требуемой
    """
    try:
        installed_version = get_package_version(name)
        if not installed_version:
            logger.warning("Package '%s' not installed", name)
            return False

        if packaging.version.parse(installed_version) >= packaging.version.parse(required_version):
            logger.info("Version %s >= %s", installed_version, required_version)
            return True
        else:
            logger.warning("A version of %s is installed, %s requires", installed_version, required_version)
            return False

    except Exception as e:
        logger.error("Error when comparing versions of the package '%s': %s", name, e)
        return False


def install_package(name: str, version: str | None = None) -> None:
    """Installs a package from PyPI using pip."""
    if is_package_installed(name):
        logger.debug("Package '%s' is already installed.", name)
        return

    try:
        # Run pip as a subprocess
        # sys.executable ensures using pip from the same Python environment
        result = subprocess.run(
            # [sys.executable, "-m", "pip", "install", name],
            ["pip", "install", name if not version else f"{name}=={version}", "--target",
             get_packages_path() if get_packages_path() else ""],
            check=True,  # Will raise CalledProcessError if pip exits with an error
            capture_output=True,  # Captures stdout and stderr
            text=True  # Decodes stdout and stderr as text
        )
        logger.info("Package '%s' installed successfully.", name)
        logger.debug("%s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Error installing package '%s': %s", name, e)
        logger.debug("%s", e.stderr)
    except subprocess.SubprocessError as e:
        logger.error("Subprocess error occurred: %s", e)
    except FileNotFoundError:
        logger.error("Error: 'pip' not found. Make sure Python and pip are installed and available in PATH.")
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)


def _example_usage() -> None:
    venv_path = get_venv_path()

    if venv_path:
        print(f"The path to the virtual environment: {venv_path}")
        print(f"The path to Python: {get_python_path()}")
    else:
        print("Virtual environment was not detected.")

    # This function demonstrates how to use the install_package function
    # You can replace 'requests' with any package you want to install
    package_name = "requests"  # Replace with the name of the required package

    if is_package_installed(package_name):
        print(f"Package '{package_name}' installed, version: {get_package_version(package_name)}")
    else:
        install_package(package_name)

    # After installation, you can try to import the package
    # (may require script restart or more complex sys.path manipulation
    # depending on how and where pip installs the package)
    try:
        import requests

        print(f"Package '{package_name}' successfully imported after installation.")
    except ImportError:
        print(f"Failed to import package '{package_name}' immediately after installation.")

    required_version = "1.0.0"
    is_compatible = compare_package_versions(package_name, required_version)

    if not is_compatible:
        print(f"Installation of the package '{package_name}' version {required_version}")
        # install_package(package_name, required_version)


if __name__ == "__main__":
    _example_usage()
