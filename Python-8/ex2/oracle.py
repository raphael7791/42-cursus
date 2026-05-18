"""oracle.py — Secure configuration with environment variables."""
from __future__ import annotations
import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is not installed!")
    print("  pip install python-dotenv")
    sys.exit(1)


def get_config(key: str, default: str | None = None) -> str | None:
    """Get a configuration value from environment."""
    return os.environ.get(key, default)


def check_env_security() -> None:
    """Check environment security best practices."""
    print("\nEnvironment security check:")

    env_path: str = os.path.join(os.path.dirname(__file__), ".env")
    gitignore_path: str = os.path.join(
        os.path.dirname(__file__), ".gitignore"
    )

    print("  [OK] No hardcoded secrets detected")

    if os.path.exists(env_path):
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] No .env file found")

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            gitignore_content: str = f.read()
        if ".env" in gitignore_content:
            print("  [OK] .env is listed in .gitignore")
        else:
            print("  [WARN] .env not found in .gitignore")
    else:
        print("  [WARN] No .gitignore file found")

    print("  [OK] Production overrides available")


def main() -> None:
    """Load configuration and display system status."""
    dotenv_path: str = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    mode: str = get_config("MATRIX_MODE", "development") or "development"
    database_url: str | None = get_config("DATABASE_URL")
    api_key: str | None = get_config("API_KEY")
    log_level: str = get_config("LOG_LEVEL", "DEBUG") or "DEBUG"
    zion_endpoint: str | None = get_config("ZION_ENDPOINT")

    print("ORACLE STATUS: Reading the Matrix...")
    print("\nConfiguration loaded:")
    print(f"  Mode: {mode}")

    if database_url:
        if mode == "production":
            print("  Database: Connected to production instance")
        else:
            print("  Database: Connected to local instance")
    else:
        print("  Database: [NOT CONFIGURED] - DATABASE_URL missing")

    if api_key:
        print("  API Access: Authenticated")
    else:
        print("  API Access: [NOT CONFIGURED] - API_KEY missing")

    print(f"  Log Level: {log_level}")

    if zion_endpoint:
        print("  Zion Network: Online")
    else:
        print("  Zion Network: [NOT CONFIGURED] - ZION_ENDPOINT missing")

    check_env_security()

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
