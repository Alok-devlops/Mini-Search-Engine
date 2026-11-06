# modules/query_processor.py
# ---------------------------------------------------------
# QUERY PROCESSOR MODULE
# Responsibility: Handle normal (non-wildcard) text queries.
#
# How it works:
#   1. The raw query string is split into individual terms.
#   2. Each term is normalized (lowercased, stripped of punctuation).
#   3. For each term, the inverted index is consulted to get
#      the list of documents containing that term.
#   4. AND logic is applied: only documents that contain
#      ALL query terms are returned.
#   5. For each matching document, a snippet (the first
#      sentence that contains any query term) is extracted.
# ---------------------------------------------------------

from modules.normalizer import normalize_query_term
from modules.tokenizer import tokenize


def _extract_snippet(content: str, query_terms: list, snippet_length: int = 200) -> str:
    """
    Extracts a short contextual snippet from the document text.

    Strategy: find the first line/sentence containing any query term
    and return up to `snippet_length` characters starting from there.

    Args:
        content (str): The full document text.
        query_terms (list): Normalized query terms to look for.
        snippet_length (int): Maximum number of characters in the snippet.

    Returns:
        str: A short snippet from the document, or the opening characters.
    """

    content_lower = content.lower()

    # Try each query term and find the earliest occurrence in the text
    earliest_pos = len(content)  # start with an impossible large value

    for term in query_terms:
        pos = content_lower.find(term)
        if pos != -1 and pos < earliest_pos:
            earliest_pos = pos

    if earliest_pos == len(content):
        # None of the terms were found (shouldn't happen, but be safe)
        return content[:snippet_length] + "..."

    # Find a good starting position – go back to the nearest sentence start
    start = max(0, earliest_pos - 40)

    snippet = content[start: start + snippet_length]

    # Clean up: strip leading/trailing whitespace
    snippet = snippet.strip()

    if start > 0:
        snippet = "..." + snippet
    if start + snippet_length < len(content):
        snippet = snippet + "..."

    return snippet


def process_query(query: str, index: dict, documents: dict) -> dict:
    """
    Processes a normal text query and returns matching documents.

    AND Retrieval Logic:
      - If the user types "machine learning", only documents that
        contain BOTH "machine" AND "learning" are returned.
      - This is implemented using Python set intersection.

    Args:
        query (str): The raw query string from the user.
        index (dict): The inverted index.
        documents (dict): The original documents { doc_id: content }.

    Returns:
        dict: {
            "query_terms": [normalized terms that were searched],
            "results": [
                {
                    "doc_id":  str,
                    "snippet": str
                },
                ...
            ],
            "not_found_terms": [terms not present in the index]
        }
    """

    # --- Step 1: Split the query into individual words ---
    raw_tokens = tokenize(query)

    # --- Step 2: Normalize each query term ---
    query_terms = [normalize_query_term(t) for t in raw_tokens]
    query_terms = [t for t in query_terms if t]  # remove empties

    if not query_terms:
        return {
            "query_terms": [],
            "results": [],
            "not_found_terms": [],
        }

    # --- Step 3: Look up each term in the index ---
    not_found_terms = []
    posting_sets = []  # list of sets of doc_ids, one per query term

    for term in query_terms:
        if term in index:
            posting_sets.append(set(index[term]))
        else:
            not_found_terms.append(term)
            posting_sets.append(set())  # empty set → AND will produce nothing

    # --- Step 4: AND intersection across all posting sets ---
    # Start with the first set, then intersect with each subsequent set
    if posting_sets:
        matched_doc_ids = posting_sets[0]
        for s in posting_sets[1:]:
            matched_doc_ids = matched_doc_ids.intersection(s)
    else:
        matched_doc_ids = set()

    # --- Step 5: Build result list with snippets ---
    results = []
    for doc_id in sorted(matched_doc_ids):
        snippet = _extract_snippet(documents[doc_id], query_terms)
        results.append({
            "doc_id": doc_id,
            "snippet": snippet,
        })

    return {
        "query_terms": query_terms,
        "results": results,
        "not_found_terms": not_found_terms,
    }
