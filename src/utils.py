"""
Shared utility functions.
"""

import os


def get_project_root() -> str:
    """
    Return the project root directory (parent of src/).

    Returns:
        Absolute path to the project root.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_default_pdf_path() -> str:
    """
    Return the default PDF path: document.pdf in the project root.

    Returns:
        Absolute path to document.pdf.
    """
    return os.path.join(get_project_root(), "document.pdf")
