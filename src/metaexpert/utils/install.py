import subprocess
#import sys


def install_package(package_name) -> None:
    """Installs a package from PyPI using pip."""
    try:
        # Run pip as a subprocess
        # sys.executable ensures using pip from the same Python environment
        result = subprocess.run(
            #[sys.executable, "-m", "pip", "install", package_name],
            ["pip", "install", package_name],
            #["uv", "add", package_name],
            check=True,  # Will raise CalledProcessError if pip exits with an error
            capture_output=True,  # Captures stdout and stderr
            text=True  # Decodes stdout and stderr as text
        )
        print(f"Package '{package_name}' installed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{package_name}':")
        print(e.stderr)
    except FileNotFoundError:
        print("Error: 'pip' not found. Make sure Python and pip are installed and available in PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Usage example:
def __example_usage() -> None:
    # This function demonstrates how to use the install_package function
    # You can replace 'requests' with any package you want to install
    package_to_install = "requests"  # Replace with the name of the required package
    install_package(package_to_install)

    # After installation, you can try to import the package
    # (may require script restart or more complex sys.path manipulation
    # depending on how and where pip installs the package)
    try:
        import requests

        print(f"Package '{package_to_install}' successfully imported after installation.")
    except ImportError:
        print(f"Failed to import package '{package_to_install}' immediately after installation.")
