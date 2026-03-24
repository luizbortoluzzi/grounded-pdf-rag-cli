"""
Centralized configuration and environment loading.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# Database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "rag")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

# Paths
PDF_PATH = os.getenv("PDF_PATH", "")

# Allow full connection string override
DATABASE_URL = os.getenv("DATABASE_URL")


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
