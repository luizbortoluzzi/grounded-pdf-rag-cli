"""
Custom exceptions for structured error handling.
"""


class GroundedRAGError(Exception):
    """Base exception for the RAG application."""

    pass


class ConfigError(GroundedRAGError):
    """Raised when configuration is invalid or missing."""

    pass


class IngestionError(GroundedRAGError):
    """Raised when PDF ingestion fails."""

    pass


class SearchError(GroundedRAGError):
    """Raised when vector search or LLM invocation fails."""

    pass


class DatabaseError(GroundedRAGError):
    """Raised when database operations fail."""

    pass
