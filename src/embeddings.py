"""
Embedding model setup and utilities.
"""

from langchain_openai import OpenAIEmbeddings

import config
from exceptions import ConfigError


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Create an OpenAI embeddings model using config settings.

    Returns:
        Configured OpenAIEmbeddings instance.
    """
    if not config.OPENAI_API_KEY:
        raise ConfigError("OPENAI_API_KEY is not set.")
    return OpenAIEmbeddings(
        model=config.OPENAI_EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
    )
