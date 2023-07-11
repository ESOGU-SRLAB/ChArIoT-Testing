"""
    This file contains the masking functions used in the transformer model.
"""
import torch

from parameters import DEVICE, PAD_IDX


def generate_square_subsequent_mask(sz):
    """
    mask out subsequent positions in the sequence for a given sequence length (sz)

    Args:
        sz: sequence length of the input sequence (src or tgt)

    Returns:
        Tensor: mask tensor of shape (sz, sz)
    """
    mask = (torch.triu(torch.ones((sz, sz), device=DEVICE)) == 1).transpose(0, 1)
    mask = (
        mask.float()
        .masked_fill(mask == 0, float("-inf"))
        .masked_fill(mask == 1, float(0.0))
    )
    return mask


def create_mask(src, tgt):
    """
    create mask for the source and target sequences

    Args:
        src: source sequence tensor of shape (src_seq_len, batch_size)
        tgt: target sequence tensor of shape (tgt_seq_len, batch_size)

    Returns:
        src_mask: source mask tensor of shape (src_seq_len, src_seq_len)
        tgt_mask: target mask tensor of shape (tgt_seq_len, tgt_seq_len)
        src_padding_mask: source padding mask tensor of shape (batch_size, src_seq_len)
        tgt_padding_mask: target padding mask tensor of shape (batch_size, tgt_seq_len)
    """
    src_seq_len = src.shape[0]
    tgt_seq_len = tgt.shape[0]

    tgt_mask = generate_square_subsequent_mask(tgt_seq_len)
    src_mask = torch.zeros((src_seq_len, src_seq_len), device=DEVICE).type(torch.bool)

    src_padding_mask = (src == PAD_IDX).transpose(0, 1)
    tgt_padding_mask = (tgt == PAD_IDX).transpose(0, 1)
    return src_mask, tgt_mask, src_padding_mask, tgt_padding_mask
