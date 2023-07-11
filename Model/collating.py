"""
    This file contains functions to collate data samples into batch tensors
"""

from typing import List

import torch
from parameters import (
    BOS_IDX,
    EOS_IDX,
    PAD_IDX,
    SRC_LANGUAGE,
    TGT_LANGUAGE,
    text_transform,
    token_transform,
    vocab_transform,
)
from torch.nn.utils.rnn import pad_sequence


# helper function to club together sequential operations
def sequential_transforms(*transforms):
    """
    To club together sequential operations

    Args:
        transforms: multiple sequential transforms

    Returns:
        A single transform which is a sequential application of all transforms passesd in args
    """

    def func(txt_input):
        """
        To apply sequential transforms

        Args:
            txt_input: input text data on which transforms need to be applied

        Returns:
            txt_input: text data after applying transforms
        """
        for transform in transforms:  # apply transforms sequentially
            txt_input = transform(txt_input)  # transform txt_input
        return txt_input

    return func


def tensor_transform(token_ids: List[int]):
    """
    To add BOS/EOS and create tensor for input sequence indices

    Args:
        token_ids (List[int]): list of token ids

    Returns:
        torch.tensor: tensor of token ids with BOS/EOS tokens
    """
    return torch.cat(
        (torch.tensor([BOS_IDX]), torch.tensor(token_ids), torch.tensor([EOS_IDX]))
    )


def convert_string_to_indices():
    """
    To convert raw strings into tensors indices
    """
    for ln in [SRC_LANGUAGE, TGT_LANGUAGE]:
        text_transform[ln] = sequential_transforms(
            token_transform[ln],  # Tokenization
            vocab_transform[ln],  # Numericalization
            tensor_transform,
        )  # Add BOS/EOS and create tensor


# function to collate data samples into batch tensors
def collate_fn(batch):
    """
    To collate data samples into batch tensors

    Args:
        batch: list of raw data samples

    Returns:
        src_batch: batch of padded source sequences
        tgt_batch: batch of padded target sequences
    """
    src_batch, tgt_batch = [], []  # initialize source and target batch
    for src_sample, tgt_sample in batch:  # iterate through each sample in batch
        src_batch.append(
            text_transform[SRC_LANGUAGE](src_sample.rstrip("\n"))
        )  # append source sample after tokenizing and numericalizing
        tgt_batch.append(
            text_transform[TGT_LANGUAGE](tgt_sample.rstrip("\n"))
        )  # append target sample after tokenizing and numericalizing

    src_batch = pad_sequence(src_batch, padding_value=PAD_IDX)  # pad source sequences
    tgt_batch = pad_sequence(tgt_batch, padding_value=PAD_IDX)  # pad target sequences
    return src_batch, tgt_batch
