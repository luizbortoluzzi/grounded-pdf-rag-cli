"""
Centralized configuration and environment loading.
"""

import os
from typing import Optional

from dotenv import load_dotenv

from exceptions import ConfigError

load_dotenv()


# Database settings
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: str = os.getenv("DB_PORT", "5432")
DB_NAME: str = os.getenv("DB_NAME", "rag")
DB_USER: str = os.getenv("DB_USER", "postgres")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
PG_VECTOR_COLLECTION_NAME: str = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")

# OpenAI settings
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

# Paths
PDF_PATH: str = os.getenv("PDF_PATH", "")

# Allow full connection string override
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")


def get_database_url() -> str:
    """
    Build the PostgreSQL connection string from environment variables.
    Uses DATABASE_URL if set, otherwise constructs from DB_HOST, DB_PORT, etc.

    Returns:
        Connection string for PostgreSQL.
    """
    if DATABASE_URL:
        return DATABASE_URL
    return (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def validate_config(for_ingestion: bool = False) -> None:
    """
    Validate required configuration. Raises ConfigError if invalid.

    Args:
        for_ingestion: If True, also validate PDF_PATH when set.
    """
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise ConfigError(
            "OPENAI_API_KEY is not set. Set it in .env or export it."
        )
    if for_ingestion and PDF_PATH and not os.path.exists(PDF_PATH):
        raise ConfigError(f"PDF_PATH points to non-existent file: {PDF_PATH}")
