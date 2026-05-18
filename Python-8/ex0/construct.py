"""construct.py — Virtual environment detection."""
from __future__ import annotations
import sys
import os
import site


def get_global_site_packages() -> str:
    """Get global site-packages path from base prefix."""
    major: int = sys.version_info.major
    minor: int = sys.version_info.minor
    if sys.platform == "win32":
        return os.path.join(
            sys.base_prefix, "Lib", "site-packages"
        )
    return os.path.join(
        sys.base_prefix, "lib",
        f"python{major}.{minor}", "site-packages"
    )


def main() -> None:
    """Detect virtual environment and display Python environment info."""
    venv_path: str | None = os.environ.get("VIRTUAL_ENV")

    if venv_path is None:
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        global_packages: list[str] = site.getsitepackages()
        if global_packages:
            print("\nGlobal package location:")
            print(f"  {global_packages[0]}")
        print()
        print("To enter the construct, run:")
        print("  python -m venv matrix_env")
        print("  source matrix_env/bin/activate  # On Unix")
        print("  matrix_env\\Scripts\\activate      # On Windows")
        print()
        print("Then run this program again.")
    else:
        env_name: str = os.path.basename(venv_path)
        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path: {venv_path}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        venv_packages: list[str] = site.getsitepackages()
        if venv_packages:
            print("\nPackage installation path:")
            print(f"  {venv_packages[0]}")
        global_path: str = get_global_site_packages()
        print("\nGlobal package location (outside construct):")
        print(f"  {global_path}")


if __name__ == "__main__":
    main()
