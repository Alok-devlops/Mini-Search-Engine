# modules/document_loader.py
# ---------------------------------------------------------
# DOCUMENT LOADER MODULE
# Responsibility: Read all .txt files from a given directory
# and return their contents as a dictionary.
# ---------------------------------------------------------

import os


def load_documents(directory: str) -> dict:
    """
    Reads all .txt files from the specified directory.

    Args:
        directory (str): Path to the folder containing .txt documents.

    Returns:
        dict: A dictionary where keys are document IDs (e.g., 'doc1')
              and values are the raw text content of each document.

    Raises:
        FileNotFoundError: If the given directory does not exist.
        ValueError: If no .txt files are found in the directory.
    """

    # Check that the directory actually exists on disk
    if not os.path.exists(directory):
        raise FileNotFoundError(
            f"Document directory '{directory}' not found. "
            "Please create it and add .txt files."
        )

    documents = {}  # Will hold { doc_id: content }

    # Walk through every file in the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            # Build the doc_id by stripping the .txt extension (e.g., "doc1")
            doc_id = filename.replace(".txt", "")
            filepath = os.path.join(directory, filename)

            # Open and read the file content
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            documents[doc_id] = content

    if not documents:
        raise ValueError(
            f"No .txt files found in '{directory}'. "
            "Please add at least one document."
        )

    return documents
