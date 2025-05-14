import subprocess


def is_package_installed(name: str) -> bool:
    """Checks whether the package is installed in the virtual environment."""
    try:
        result = subprocess.run(
            ["pip", "show", name],
            check=False,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Mistake when checking the package: {e}")
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
        print(f"Error retrieving version for package '{name}': {e}")
        return None


def install_package(name: str) -> None:
    """Installs a package from PyPI using pip."""
    if is_package_installed(name):
        print(f"Package '{name}' is already installed.")
        return

    try:
        # Run pip as a subprocess
        # sys.executable ensures using pip from the same Python environment
        # import sys
        result = subprocess.run(
            # [sys.executable, "-m", "pip", "install", name],
            ["pip", "install", name],
            check=True,  # Will raise CalledProcessError if pip exits with an error
            capture_output=True,  # Captures stdout and stderr
            text=True  # Decodes stdout and stderr as text
        )
        print(f"Package '{name}' installed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{name}': {e}")
        print(e.stderr)
    except subprocess.SubprocessError as e:
        print(f"Subprocess error occurred: {e}")
    except FileNotFoundError:
        print("Error: 'pip' not found. Make sure Python and pip are installed and available in PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def __example_usage() -> None:
    # This function demonstrates how to use the install_package function
    # You can replace 'requests' with any package you want to install
    package_name = "requests"  # Replace with the name of the required package

    if is_package_installed(package_name):
        print(f"Пакет '{package_name}' установлен")
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
