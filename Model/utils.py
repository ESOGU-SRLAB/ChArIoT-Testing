"""
    This file contains helper functions for the model.
"""

from typing import Iterable, List
from torchtext.vocab import build_vocab_from_iterator

from parameters import (
    SRC_LANGUAGE,
    TGT_LANGUAGE,
    token_transform,
    vocab_transform,
    special_symbols,
    UNK_IDX,
)
from dataset import MutationDataset


def yield_tokens(data_iter: Iterable, language: str) -> List[str]:
    """
    Yield list tokens from iterator.

    Args:
        data_iter (Iterable): data iterator
        language (str): language of the tokens to be iterated over (source or target)

    Yields:
        Iterator[List[str]]: list of tokens
    """
    language_index = {
        SRC_LANGUAGE: 0,
        TGT_LANGUAGE: 1,
    }  # index for source and target language

    for data_sample in data_iter:  # data_sample is a tuple of source and target code
        yield token_transform[language](
            data_sample[language_index[language]]
        )  # token_transform is a function that tokenizes the source code


def build_vocab(X_train, y_train):
    """
    Build vocabulary for source and target language.

    Args:
        X_train: training source data
        y_train: training target data
    """
    for ln in [SRC_LANGUAGE, TGT_LANGUAGE]:  # ln is either SRC_LANGUAGE or TGT_LANGUAGE
        # Training data Iterator
        train_iter = MutationDataset(
            X_train, y_train
        )  # MutationDataset is a class that returns a tuple of source and target code
        # Create torchtext's Vocab object
        vocab_transform[ln] = build_vocab_from_iterator(
            yield_tokens(train_iter, ln),
            min_freq=1,
            specials=special_symbols,
            special_first=True,
        )  # build_vocab_from_iterator is a function that builds a vocabulary from an iterator over tokens


def set_default_index():
    """
    Set default index for source and target language.
    """
    # Set UNK_IDX as the default index. This index is returned when the token is not found.
    # If not set, it throws RuntimeError when the queried token is not found in the Vocabulary.
    for ln in [SRC_LANGUAGE, TGT_LANGUAGE]:  # ln is either SRC_LANGUAGE or TGT_LANGUAGE
        vocab_transform[ln].set_default_index(
            UNK_IDX
        )  # UNK_IDX is the index for the unknown token
