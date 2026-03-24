"""
Embedding model setup and utilities.
"""

from langchain_openai import OpenAIEmbeddings

import config


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Create an OpenAI embeddings model using config settings.

    Returns:
        Configured OpenAIEmbeddings instance.
    """
    return OpenAIEmbeddings(
        model=config.OPENAI_EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
    )
