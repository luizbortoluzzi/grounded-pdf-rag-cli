"""
Entrypoint for interactive chat using grounded QA.
"""

import config  # noqa: F401 - load env via config
from search import search_prompt


def main():
    """Run the chat interface."""
    answer_fn = search_prompt()

    if not answer_fn:
        print("Could not start the chat. Check initialization errors.")
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
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
