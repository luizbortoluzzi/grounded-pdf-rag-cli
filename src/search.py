"""
Entrypoint for similarity search over the vector store.
"""

import logging
from typing import Callable, Iterator, List, Optional, Tuple, Union

from langchain_core.documents import Document

import config  # noqa: F401 - load env via config
from db import get_vector_store
from llm import get_chat_model
from prompts import get_grounded_qa_prompt

logger = logging.getLogger(__name__)

# Number of documents to retrieve (per assignment)
SEARCH_K = 10


def _format_context(docs: List[Tuple[Document, float]]) -> str:
    """Concatenate document contents into a single context string."""
    return "\n\n".join(doc.page_content for doc, _ in docs)


def _answer_question_sync(question: str) -> str:
    """Non-streaming answer: return full response string."""
    vector_store = get_vector_store()
    docs_with_scores = vector_store.similarity_search_with_score(
        question, k=SEARCH_K
    )
    context = _format_context(docs_with_scores)
    prompt = get_grounded_qa_prompt(context, question)
    llm = get_chat_model()
    response = llm.invoke(prompt)
    return str(response.content)


def _answer_question_stream(question: str) -> Iterator[str]:
    """Streaming answer: yield response chunks."""
    vector_store = get_vector_store()
    docs_with_scores = vector_store.similarity_search_with_score(
        question, k=SEARCH_K
    )
    context = _format_context(docs_with_scores)
    prompt = get_grounded_qa_prompt(context, question)
    llm = get_chat_model()
    for chunk in llm.stream(prompt):
        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content


def _answer_question(
    question: str,
    *,
    stream: bool = False,
) -> Union[str, Iterator[str]]:
    """
    Vectorize the question, search top-k chunks, build prompt, call LLM.

    Args:
        question: User question.
        stream: If True, yield response chunks; otherwise return full string.

    Returns:
        Full response string, or iterator of chunks when stream=True.
    """
    if stream:
        return _answer_question_stream(question)
    return _answer_question_sync(question)


def search_prompt(
    question: Optional[str] = None,
) -> Optional[Callable[..., Union[str, Iterator[str]]]]:
    """
    Build a QA chain for grounded question answering.

    Args:
        question: Optional question for a single query (not used when
            returning the chain for chat loop).

    Returns:
        Callable that takes a question string and returns the answer,
        or None if initialization fails.
    """
    try:
        config.validate_config()
        get_vector_store()
        get_chat_model()
        return _answer_question
    except Exception as e:
        logger.debug("Search initialization failed: %s", e)
        return None
