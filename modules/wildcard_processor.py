# modules/wildcard_processor.py
# ---------------------------------------------------------
# WILDCARD PROCESSOR MODULE
# Responsibility: Handle wildcard search queries containing
# the '*' character.
#
# How it works:
#   The user types a pattern like "py*" or "comput*".
#   We convert the '*' into a regex pattern (.*)  and test
#   it against every term in the indexed vocabulary.
#   The matching terms are then used to retrieve documents
#   from the inverted index (same as a normal term lookup).
#
# Supported wildcard positions:
#   Prefix wildcard  : *ing  → anything ending in "ing"
#   Suffix wildcard  : py*   → anything starting with "py"
#   Infix wildcard   : m*ne  → anything matching m...ne
# ---------------------------------------------------------

import re


def expand_wildcard(pattern: str, vocabulary: list) -> list:
    """
    Expands a wildcard pattern into matching vocabulary terms.

    Args:
        pattern (str): A wildcard query string, e.g. "py*" or "comput*".
        vocabulary (list): The full list of indexed terms.

    Returns:
        list: All vocabulary terms that match the wildcard pattern.
    """

    # Convert the wildcard '*' into a regex equivalent '.*'
    # We also anchor the pattern with ^ and $ so that it must
    # match the ENTIRE term, not just a substring.
    regex_pattern = "^" + re.escape(pattern).replace(r'\*', '.*') + "$"

    matched_terms = []

    for term in vocabulary:
        # re.fullmatch could also be used; using re.match with anchors is explicit
        if re.match(regex_pattern, term):
            matched_terms.append(term)

    return matched_terms


def wildcard_search(pattern: str, index: dict, vocabulary: list) -> dict:
    """
    Performs a wildcard search and returns results.

    Args:
        pattern (str): The wildcard query (e.g., "py*").
        index (dict): The inverted index.
        vocabulary (list): All indexed terms.

    Returns:
        dict: {
            "matched_terms": [list of vocabulary terms matching the pattern],
            "doc_ids":        [sorted list of doc_ids containing any matched term]
        }
    """

    # Step 1 – find all vocabulary terms that match the pattern
    matched_terms = expand_wildcard(pattern, vocabulary)

    # Step 2 – collect all document IDs that contain ANY matched term
    # Using a set to avoid duplicates across different matched terms
    doc_id_set = set()
    for term in matched_terms:
        for doc_id in index.get(term, []):
            doc_id_set.add(doc_id)

    return {
        "matched_terms": sorted(matched_terms),
        "doc_ids": sorted(doc_id_set),
    }
