"""Tests for config module."""

from unittest.mock import patch

import pytest

import config
from exceptions import ConfigError


def test_get_database_url_uses_database_url_when_set() -> None:
    """When DATABASE_URL is set, it is returned directly."""
    with patch.object(config, "DATABASE_URL", "postgresql://custom/db"):
        url = config.get_database_url()
        assert url == "postgresql://custom/db"


def test_get_database_url_builds_from_components() -> None:
    """When DATABASE_URL is not set, URL is built from DB_* vars."""
    with patch.object(config, "DATABASE_URL", None):
        with patch.object(config, "DB_HOST", "dbhost"):
            with patch.object(config, "DB_PORT", "5433"):
                with patch.object(config, "DB_NAME", "mydb"):
                    with patch.object(config, "DB_USER", "user"):
                        with patch.object(config, "DB_PASSWORD", "pass"):
                            url = config.get_database_url()
                            assert "dbhost" in url
                            assert "5433" in url
                            assert "mydb" in url
                            assert "user" in url


def test_validate_config_raises_when_api_key_missing() -> None:
    """validate_config raises ConfigError when OPENAI_API_KEY is empty."""
    with patch.object(config, "OPENAI_API_KEY", None):
        with pytest.raises(ConfigError) as exc_info:
            config.validate_config()
        assert "OPENAI_API_KEY" in str(exc_info.value)


def test_validate_config_raises_when_api_key_whitespace_only() -> None:
    """validate_config raises ConfigError when OPENAI_API_KEY is whitespace."""
    with patch.object(config, "OPENAI_API_KEY", "   "):
        with pytest.raises(ConfigError):
            config.validate_config()


def test_validate_config_succeeds_when_api_key_set() -> None:
    """validate_config does not raise when OPENAI_API_KEY is set."""
    with patch.object(config, "OPENAI_API_KEY", "sk-test-key"):
        config.validate_config()  # Should not raise
