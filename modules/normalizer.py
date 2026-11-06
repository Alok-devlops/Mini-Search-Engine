# modules/normalizer.py
# ---------------------------------------------------------
# NORMALIZER MODULE
# Responsibility: Normalize a list of tokens so that the
# same word in different forms maps to the same index key.
#
# Operations performed:
#   1. Lowercase conversion  ("Python" → "python")
#   2. Strip any remaining non-alphabetic characters
#   3. Remove empty tokens
# ---------------------------------------------------------


def normalize(tokens: list) -> list:
    """
    Normalizes a list of tokens.

    Args:
        tokens (list): Raw tokens produced by the tokenizer.

    Returns:
        list: Cleaned, lowercase tokens ready for indexing.
    """

    normalized = []

    for token in tokens:
        # Step 1 – convert to lowercase for case-insensitive matching
        token = token.lower()

        # Step 2 – keep only alphabetic characters
        # (removes stray digits or underscores that slipped through)
        token = ''.join(ch for ch in token if ch.isalpha())

        # Step 3 – discard empty strings that result from the above strip
        if token:
            normalized.append(token)

    return normalized


def normalize_query_term(term: str) -> str:
    """
    Normalizes a single query term (used by the query processor).
    Preserves the '*' wildcard character so wildcard queries still work.

    Args:
        term (str): A single query word or wildcard pattern.

    Returns:
        str: The normalized term with '*' kept intact.
    """

    # Lowercase the term
    term = term.lower()

    # Keep only alphabetic characters AND the wildcard '*'
    term = ''.join(ch for ch in term if ch.isalpha() or ch == '*')

    return term
