"""
Entrypoint for interactive chat using grounded QA.
"""

import logging
import sys

import config  # noqa: F401 - load env via config
from search import search_prompt

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the chat interface."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    answer_fn = search_prompt()

    if not answer_fn:
        logger.error("Could not start the chat. Check OPENAI_API_KEY and database connection.")
        return

    print("Ask your question (or type 'exit' to quit):\n")

    while True:
        try:
            question = input("QUESTION: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Exiting.")
            break

        try:
            response = answer_fn(question)
            print(f"ANSWER: {response}\n")
        except Exception as e:
            logger.exception("Error processing question")
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
