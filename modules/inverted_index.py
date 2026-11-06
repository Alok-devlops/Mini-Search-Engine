# modules/inverted_index.py
# ---------------------------------------------------------
# INVERTED INDEX MODULE
# Responsibility: Build and store an inverted index from a
# collection of documents.
#
# Data structure:
#   {
#     "python":  ["doc1", "doc3"],
#     "machine": ["doc2", "doc3"],
#     ...
#   }
#
# An inverted index maps each unique term to the sorted list
# of documents that contain it, allowing fast lookup by term.
# ---------------------------------------------------------

from modules.tokenizer import tokenize
from modules.normalizer import normalize


def build_index(documents: dict) -> dict:
    """
    Builds an inverted index from a dictionary of documents.

    Algorithm:
      For each document:
        1. Tokenize its text into words.
        2. Normalize the tokens (lowercase, strip punctuation).
        3. For each unique normalized token, record the doc_id
           in the posting list IF it is not already present
           (this avoids duplicate entries per document).

    Args:
        documents (dict): { doc_id (str): content (str) }

    Returns:
        dict: The inverted index { term (str): [doc_id, ...] }
    """

    index = {}  # This will be our inverted index

    for doc_id, content in documents.items():
        # --- Step 1: Tokenize the raw document text ---
        tokens = tokenize(content)

        # --- Step 2: Normalize the tokens ---
        normalized_tokens = normalize(tokens)

        # --- Step 3: Get unique terms for THIS document ---
        # Using a set avoids adding the same doc_id twice for a repeated term
        unique_terms = set(normalized_tokens)

        # --- Step 4: Update the index ---
        for term in unique_terms:
            if term not in index:
                # First time we see this term – create a new posting list
                index[term] = []

            # Add this document to the term's posting list
            index[term].append(doc_id)

    # Sort each posting list for consistency and easier debugging
    for term in index:
        index[term] = sorted(index[term])

    return index


def get_vocabulary(index: dict) -> list:
    """
    Returns the sorted list of all unique terms in the index (the vocabulary).

    Args:
        index (dict): The inverted index.

    Returns:
        list: Alphabetically sorted list of indexed terms.
    """
    return sorted(index.keys())
