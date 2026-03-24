"""Tests for utils module."""

import os

from utils import get_default_pdf_path, get_project_root


def test_get_project_root_returns_absolute_path() -> None:
    """Project root is an absolute path."""
    root = get_project_root()
    assert os.path.isabs(root)
    assert os.path.isdir(root)


def test_get_project_root_contains_src() -> None:
    """Project root contains the src directory."""
    root = get_project_root()
    src_path = os.path.join(root, "src")
    assert os.path.isdir(src_path)


def test_get_default_pdf_path_ends_with_document_pdf() -> None:
    """Default PDF path points to document.pdf."""
    path = get_default_pdf_path()
    assert path.endswith("document.pdf")


def test_get_default_pdf_path_is_in_project_root() -> None:
    """Default PDF path is in project root."""
    root = get_project_root()
    path = get_default_pdf_path()
    assert path.startswith(root)
