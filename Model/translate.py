"""
    This file contains the function to translate the input sentence into target language.
"""
import torch

from parameters import (
    SRC_LANGUAGE,
    TGT_LANGUAGE,
    vocab_transform,
    text_transform,
    BOS_IDX,
)
from decoding import greedy_decode


def translate(model: torch.nn.Module, src_sentence: str):
    """
    actual function to translate input sentence into target language

    Args:
        model (torch.nn.Module): the transformer model
        src_sentence (str): the input sentence to be translated

    Returns:
        str: the translated sentence
    """
    model.eval()  # set model to eval mode for inference
    src = text_transform[SRC_LANGUAGE](src_sentence).view(
        -1, 1
    )  # convert input sentence into tensor
    num_tokens = src.shape[0]  # get number of tokens in sentence
    src_mask = (torch.zeros(num_tokens, num_tokens)).type(
        torch.bool
    )  # create mask for input sentence
    tgt_tokens = greedy_decode(
        model, src, src_mask, max_len=num_tokens + 100, start_symbol=BOS_IDX
    ).flatten()  # generate output sequence tensor
    return (
        " ".join(
            vocab_transform[TGT_LANGUAGE].lookup_tokens(list(tgt_tokens.cpu().numpy()))
        )
        .replace("<bos>", "")
        .replace("<eos>", "")
    )  # convert output sequence tensor into sentence
