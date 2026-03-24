"""Tests for custom exceptions."""

import pytest

from exceptions import (
    ConfigError,
    DatabaseError,
    GroundedRAGError,
    IngestionError,
    SearchError,
)


def test_exceptions_inherit_from_base() -> None:
    """All custom exceptions inherit from GroundedRAGError."""
    assert issubclass(ConfigError, GroundedRAGError)
    assert issubclass(IngestionError, GroundedRAGError)
    assert issubclass(SearchError, GroundedRAGError)
    assert issubclass(DatabaseError, GroundedRAGError)


def test_config_error_message() -> None:
    """ConfigError preserves message."""
    err = ConfigError("Missing API key")
    assert str(err) == "Missing API key"


def test_ingestion_error_can_be_raised() -> None:
    """IngestionError can be raised and caught."""
    with pytest.raises(IngestionError) as exc_info:
        raise IngestionError("PDF not found")
    assert "PDF not found" in str(exc_info.value)
