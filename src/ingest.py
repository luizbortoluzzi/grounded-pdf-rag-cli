"""
Entrypoint for PDF ingestion into the vector store.
"""

import argparse
import sys

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config  # noqa: F401 - load env via config
from db import store_documents
from utils import get_default_pdf_path


def load_pdf(pdf_path: str):
    """
    Load a PDF file and return its pages as LangChain documents.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of Document objects (one per page).
    """
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(documents, chunk_size: int = 1000, chunk_overlap: int = 150):
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


def run_ingestion(pdf_path: str, recreate_collection: bool = True) -> None:
    """
    Run the full ingestion pipeline: load PDF, split, embed, and store.

    Args:
        pdf_path: Path to the PDF file.
        recreate_collection: If True, clear the collection before inserting
            (ensures idempotent runs).
    """
    import os

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    print("Loading PDF...")
    try:
        documents = load_pdf(pdf_path)
    except Exception as e:
        print(f"Error loading PDF: {e}")
        sys.exit(1)

    num_pages = len(documents)
    print(f"Loaded {num_pages} page(s).")

    print("Splitting into chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunk(s).")

    print("Generating embeddings...")
    print("Storing in database...")
    try:
        store_documents(chunks, pre_delete_collection=recreate_collection)
    except Exception as e:
        print(f"Error connecting to database or storing documents: {e}")
        sys.exit(1)

    print("Ingestion completed successfully.")


def main():
    """Parse arguments and run ingestion."""
    parser = argparse.ArgumentParser(
        description="Ingest PDF documents into the vector store.",
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
    args = parser.parse_args()

    pdf_path = args.pdf or config.PDF_PATH or get_default_pdf_path()
    recreate_collection = not args.no_recreate

    run_ingestion(pdf_path, recreate_collection=recreate_collection)


if __name__ == "__main__":
    main()
