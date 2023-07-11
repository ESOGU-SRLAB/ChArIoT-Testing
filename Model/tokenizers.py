"""
    This module contains the tokenizer function that is used to tokenize the source code.
"""
import tokenize
from io import BytesIO


def get_tokenizer(source_code):
    """
    tokenize the source code and return the tokens as a list of strings

    Args:
        source_code: the source code to be tokenized

    Returns:
        a list of tokens as strings from the source code (excluding the first and last tokens)
    """
    tokens = tokenize.tokenize(
        BytesIO(source_code.encode("utf-8")).readline
    )  # tokenize the source code
    return [token.string for token in list(tokens)[1:-2]]
