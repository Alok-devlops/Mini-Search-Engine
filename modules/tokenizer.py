# modules/tokenizer.py
# ---------------------------------------------------------
# TOKENIZER MODULE
# Responsibility: Split a raw text string into individual
# word tokens (a list of strings).
# ---------------------------------------------------------

import re


def tokenize(text: str) -> list:
    """
    Splits raw text into a list of word tokens.

    Strategy:
      - Use a regular expression to find sequences of word characters
        (letters, digits, underscores).  This automatically ignores
        punctuation, whitespace, and special symbols.
      - Example: "Hello, World!" → ["Hello", "World"]

    Args:
        text (str): The raw text to tokenize.

    Returns:
        list: A list of string tokens extracted from the text.
    """

    # \b[A-Za-z]+\b  matches only alphabetic words (skips pure numbers/symbols)
    # Using \w+ would also keep numbers and underscore; here we keep only letters
    # so that index terms are clean English words.
    tokens = re.findall(r'[A-Za-z]+', text)

    return tokens
