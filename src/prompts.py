"""
Prompt templates for grounded question answering.
"""

# Fallback answer when context does not contain relevant information
FALLBACK_ANSWER = "I don't have the necessary information to answer your question."

GROUNDED_QA_TEMPLATE = """
CONTEXT:
{{context}}

RULES:
- Answer ONLY based on the CONTEXT above.
- If the information is not explicitly in the CONTEXT, respond exactly:
  "{fallback}"
- Never invent or use external knowledge.
- Never produce opinions or interpretations beyond what is written.

QUESTION:
{{question}}

ANSWER:
""".format(fallback=FALLBACK_ANSWER)


def get_grounded_qa_prompt(context: str, question: str) -> str:
    """
    Build a grounded QA prompt using only the retrieved context.

    Args:
        context: Retrieved document chunks.
        question: User question.

    Returns:
        Formatted prompt string.
    """
    return GROUNDED_QA_TEMPLATE.format(
        context=context,
        question=question,
    )
