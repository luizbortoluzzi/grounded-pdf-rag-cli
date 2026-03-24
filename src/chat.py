"""
Entrypoint for interactive chat using grounded QA.
"""

import argparse
import logging
import sys

import config  # noqa: F401 - load env via config
from search import search_prompt

try:
    from __init__ import __version__
except ImportError:
    __version__ = "0.0.0"

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the chat interface."""
    parser = argparse.ArgumentParser(
        description="Interactive chat using grounded QA.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming (print full response at once)",
    )
    args, _ = parser.parse_known_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(message)s" if not args.verbose else "%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    answer_fn = search_prompt()

    if not answer_fn:
        logger.error("Could not start the chat. Check OPENAI_API_KEY and database connection.")
        return

    stream = not args.no_stream
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
            result = answer_fn(question, stream=stream)
            if stream and hasattr(result, "__iter__") and not isinstance(result, str):
                print("ANSWER: ", end="", flush=True)
                for chunk in result:
                    print(chunk, end="", flush=True)
                print("\n")
            else:
                print(f"ANSWER: {result}\n")
        except Exception as e:
            logger.exception("Error processing question")
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
