"""
Entrypoint for PDF ingestion into the vector store.
"""

import argparse
import logging
import os
import sys
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config  # noqa: F401 - load env via config
from db import store_documents
from exceptions import ConfigError, IngestionError
from utils import get_default_pdf_path

try:
    from __init__ import __version__
except ImportError:
    __version__ = "0.0.0"

logger = logging.getLogger(__name__)


def load_pdf(pdf_path: str) -> List[Document]:
    """
    Load a PDF file and return its pages as LangChain documents.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of Document objects (one per page).
    """
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> List[Document]:
    """
    Split documents into smaller chunks for embedding.

    Args:
        documents: List of documents to split.
        chunk_size: Maximum size of each chunk in characters.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of chunked documents.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def run_ingestion(
    pdf_path: str,
    recreate_collection: bool = True,
    show_progress: bool = False,
) -> None:
    """
    Run the full ingestion pipeline: load PDF, split, embed, and store.

    Args:
        pdf_path: Path to the PDF file.
        recreate_collection: If True, clear the collection before inserting
            (ensures idempotent runs).
        show_progress: If True, show progress bar when storing documents.
    """
    if not os.path.exists(pdf_path):
        logger.error("PDF file not found: %s", pdf_path)
        raise IngestionError(f"PDF file not found: {pdf_path}")

    logger.info("Loading PDF...")
    try:
        documents = load_pdf(pdf_path)
    except Exception as e:
        logger.exception("Failed to load PDF")
        raise IngestionError(f"Error loading PDF: {e}") from e

    num_pages = len(documents)
    logger.info("Loaded %d page(s).", num_pages)

    logger.info("Splitting into chunks...")
    chunks = split_documents(documents)
    logger.info("Created %d chunk(s).", len(chunks))

    logger.info("Generating embeddings and storing in database...")
    try:
        store_documents(
            chunks,
            pre_delete_collection=recreate_collection,
            show_progress=show_progress,
        )
    except Exception as e:
        logger.exception("Failed to store documents")
        raise IngestionError(
            f"Error connecting to database or storing documents: {e}"
        ) from e

    logger.info("Ingestion completed successfully.")


def main() -> None:
    """Parse arguments and run ingestion."""
    parser = argparse.ArgumentParser(
        description="Ingest PDF documents into the vector store.",
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
        "--pdf",
        default=None,
        help="Path to PDF file (default: PDF_PATH env or document.pdf in project root)",
    )
    parser.add_argument(
        "--no-recreate",
        action="store_true",
        help="Do not clear collection before inserting (may create duplicates)",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar when storing documents",
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(message)s" if not args.verbose else "%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    try:
        config.validate_config()
    except ConfigError as e:
        logger.error("%s", e)
        sys.exit(1)

    pdf_path = args.pdf or config.PDF_PATH or get_default_pdf_path()
    recreate_collection = not args.no_recreate

    try:
        run_ingestion(
            pdf_path,
            recreate_collection=recreate_collection,
            show_progress=args.progress,
        )
    except IngestionError as e:
        logger.error("%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
