"""Tests for prompts module."""

from prompts import FALLBACK_ANSWER, get_grounded_qa_prompt


def test_fallback_answer_matches_expected_text() -> None:
    """Fallback answer is the expected default when context is insufficient."""
    assert FALLBACK_ANSWER == "I don't have the necessary information to answer your question."


def test_get_grounded_qa_prompt_includes_context() -> None:
    """Prompt includes the provided context."""
    prompt = get_grounded_qa_prompt("Some document text", "What is it?")
    assert "Some document text" in prompt


def test_get_grounded_qa_prompt_includes_question() -> None:
    """Prompt includes the user question."""
    prompt = get_grounded_qa_prompt("Context", "What is the revenue?")
    assert "What is the revenue?" in prompt


def test_get_grounded_qa_prompt_includes_fallback() -> None:
    """Prompt includes the fallback answer in the instructions."""
    prompt = get_grounded_qa_prompt("Context", "Question?")
    assert FALLBACK_ANSWER in prompt


def test_get_grounded_qa_prompt_has_expected_structure() -> None:
    """Prompt has CONTEXT, RULES, QUESTION sections."""
    prompt = get_grounded_qa_prompt("ctx", "q")
    assert "CONTEXT:" in prompt
    assert "RULES" in prompt
    assert "QUESTION:" in prompt
