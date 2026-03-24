"""
Health check: validate configuration and connectivity.
"""

import sys

import config  # noqa: F401 - load env via config
from exceptions import ConfigError


def check_api_key() -> bool:
    """Verify OPENAI_API_KEY is set and non-empty."""
    if not config.OPENAI_API_KEY or not config.OPENAI_API_KEY.strip():
        print("FAIL: OPENAI_API_KEY is not set or empty.")
        print("       Set it in .env or export OPENAI_API_KEY=your-key")
        return False
    print("OK: OPENAI_API_KEY is set")
    return True


def check_database() -> bool:
    """Verify database connection."""
    try:
        from db import get_vector_store

        store = get_vector_store()
        # Trigger connection by accessing a property or doing a minimal operation
        _ = store.embeddings
        print("OK: Database connection successful")
        return True
    except Exception as e:
        print(f"FAIL: Database connection failed: {e}")
        print("       Ensure PostgreSQL is running: docker compose up -d")
        return False


def main() -> None:
    """Run all health checks."""
    print("Health check\n" + "-" * 40)

    try:
        config.validate_config()
    except ConfigError as e:
        print(f"FAIL: {e}")
        sys.exit(1)

    api_ok = check_api_key()
    db_ok = check_database()

    print("-" * 40)
    if api_ok and db_ok:
        print("All checks passed.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
