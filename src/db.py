"""
Database and pgvector store utilities.
"""

from typing import List

from langchain_core.documents import Document
from langchain_postgres.vectorstores import PGVector

import config
from embeddings import get_embedding_model
from exceptions import DatabaseError


def get_vector_store(*, pre_delete_collection: bool = False) -> PGVector:
    """
    Create a PGVector store connected to PostgreSQL using config settings.

    Args:
        pre_delete_collection: If True, delete existing collection before use
            (ensures idempotent ingestion runs).

    Returns:
        Configured PGVector store instance.
    """
    try:
        return PGVector(
            embeddings=get_embedding_model(),
            connection=config.get_database_url(),
            collection_name=config.PG_VECTOR_COLLECTION_NAME,
            pre_delete_collection=pre_delete_collection,
        )
    except Exception as e:
        raise DatabaseError(f"Failed to connect to vector store: {e}") from e


def store_documents(
    documents: List[Document],
    pre_delete_collection: bool = False,
) -> None:
    """
    Persist documents into the pgvector store.

    Args:
        documents: List of documents to embed and store.
        pre_delete_collection: If True, clear collection before inserting.
    """
    vector_store = get_vector_store(pre_delete_collection=pre_delete_collection)
    try:
        vector_store.add_documents(documents)
    except Exception as e:
        raise DatabaseError(f"Failed to store documents: {e}") from e
