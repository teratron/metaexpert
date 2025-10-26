"""Module for checking required dependencies."""

import typer
from rich.console import Console

console = Console()


def _get_package_version(package: str) -> str:
    """Get the version of a package."""
    if package == "typer":
        import typer

        return typer.__version__
    elif package == "rich":
        import rich

        # Rich doesn't always have __version__ attribute, so we use __version__ if available
        return getattr(rich, "__version__", "unknown")
    elif package == "pydantic":
        import pydantic

        return getattr(pydantic, "VERSION", getattr(pydantic, "__version__", "unknown"))
    elif package == "psutil":
        import psutil

        return getattr(psutil, "__version__", "unknown")
    elif package == "jinja2":
        import jinja2

        return getattr(jinja2, "__version__", "unknown")
    else:
        # For packages not specifically handled, try generic import
        __import__(package)
        pkg = __import__(package)
        return getattr(pkg, "__version__", "unknown")


def _check_package_compatibility(
    package: str, version_spec: str
) -> tuple[str | None, str | None]:
    """Check if a package meets version requirements."""
    try:
        # Import the package
        version = _get_package_version(package)

        # Check version compatibility
        if version == "unknown":
            console.print(
                f"[yellow]Warning: Could not determine version for {package}[/yellow]"
            )
            return None, None

        # Parse version spec and actual version
        # This is a simplified check - in a real implementation you might want to use packaging.version
        if version_spec.startswith(">="):
            min_version = version_spec[2:]
            if not _is_version_compatible(version, min_version):
                return version, version_spec
        return version, None
    except ImportError:
        return "missing", None
    except Exception as e:
        console.print(f"[red]Error checking {package}: {e!s}[/red]")
        return None, None


def check_dependencies() -> None:
    """Check if all required dependencies are installed with correct versions."""
    required_packages: dict[str, str] = {
        "typer": ">=0.9.0",
        "rich": ">=13.0.0",
        "pydantic": ">=2.0.0",
        "psutil": ">=5.0.0",
        "jinja2": ">=3.0.0",
    }

    missing_packages: list[str] = []
    incompatible_packages: list[tuple[str, str, str]] = []

    for package, version_spec in required_packages.items():
        version, incompatible_spec = _check_package_compatibility(package, version_spec)

        if version == "missing":
            missing_packages.append(package)
        elif version is not None and incompatible_spec is not None:
            incompatible_packages.append((package, version, incompatible_spec))

    # Report missing packages
    if missing_packages:
        console.print(
            f"[red]Error: Missing required packages: {', '.join(missing_packages)}[/red]"
        )
        console.print(
            f"[red]Please install them using: pip install {' '.join(missing_packages)}[/red]"
        )
        raise typer.Exit(code=1)

    # Report incompatible packages
    if incompatible_packages:
        console.print("[red]Error: Incompatible package versions:[/red]")
        for package, actual_version, required_spec in incompatible_packages:
            console.print(
                f" [red]{package}: required {required_spec}, found {actual_version}[/red]"
            )
        console.print(
            "[red]Please update the packages to meet version requirements.[/red]"
        )
        raise typer.Exit(code=1)

    # All dependencies are satisfied
    console.print("[green]All required dependencies are satisfied.[/green]")


def _is_version_compatible(actual_version: str, min_version: str) -> bool:
    """Check if actual version is compatible with minimum required version."""
    try:
        actual_parts = [int(x) for x in actual_version.split(".")[:3]]
        min_parts = [int(x) for x in min_version.split(".")[:3]]

        # Compare major.minor.patch
        for a, m in zip(actual_parts, min_parts, strict=True):
            if a > m:
                return True
            elif a < m:
                return False

        # If all compared parts are equal, it's compatible
        return True
    except (ValueError, IndexError):
        # If we can't parse the version, assume it's compatible to avoid false positives
        return True
