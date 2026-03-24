"""
LLM (chat model) setup and utilities.
"""

from langchain_openai import ChatOpenAI

import config
from exceptions import ConfigError


def get_chat_model() -> ChatOpenAI:
    """
    Create a ChatOpenAI model using config settings.

    Returns:
        Configured ChatOpenAI instance.
    """
    if not config.OPENAI_API_KEY:
        raise ConfigError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(
        model=config.OPENAI_CHAT_MODEL,
        openai_api_key=config.OPENAI_API_KEY,  # type: ignore[call-arg]
        temperature=0,
    )
