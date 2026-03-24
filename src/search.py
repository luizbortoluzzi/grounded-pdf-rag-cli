"""
Entrypoint for similarity search over the vector store.
"""

from langchain_core.documents import Document

import config  # noqa: F401 - load env via config
from db import get_vector_store
from llm import get_chat_model
from prompts import get_grounded_qa_prompt

# Number of documents to retrieve (per assignment)
SEARCH_K = 10


def _format_context(docs: list[tuple[Document, float]]) -> str:
    """Concatenate document contents into a single context string."""
    return "\n\n".join(doc.page_content for doc, _ in docs)


def _answer_question(question: str) -> str:
    """
    Vectorize the question, search top-k chunks, build prompt, call LLM.

    Args:
        question: User question.

    Returns:
        LLM response grounded in retrieved context.
    """
    vector_store = get_vector_store()
    docs_with_scores = vector_store.similarity_search_with_score(question, k=SEARCH_K)
    context = _format_context(docs_with_scores)
    prompt = get_grounded_qa_prompt(context, question)
    llm = get_chat_model()
    response = llm.invoke(prompt)
    return response.content


def search_prompt(question=None):
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
        # Validate we can connect to the vector store and LLM
        get_vector_store()
        get_chat_model()
        return _answer_question
    except Exception:
        return None
