"""
LLM (chat model) setup and utilities.
"""

from langchain_openai import ChatOpenAI

import config


def get_chat_model() -> ChatOpenAI:
    """
    Create a ChatOpenAI model using config settings.

    Returns:
        Configured ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=config.OPENAI_CHAT_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
        temperature=0,
    )
