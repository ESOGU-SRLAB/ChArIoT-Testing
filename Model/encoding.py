"""
    helper Module that adds positional encoding to the token embedding to introduce a notion of word order.
"""

import math

import torch
import torch.nn as nn
from torch import Tensor


class PositionalEncoding(nn.Module):
    """
    positional encoding module that adds positional information to the token embedding

    Args:
        emb_size (int): embedding size
        dropout (float): dropout rate
        maxlen (int): maximum length of a sequence. Defaults to 5000.

    Attributes:
        den: tensor of shape (emb_size // 2) containing values used to compute the positional encoding
        pos: tensor of shape (maxlen, 1) containing the position of each token in the sequence
        pos_embedding: tensor of shape (maxlen, emb_size) containing the positional encoding
        dropout: dropout layer to apply to the sum of the token embedding and the positional encoding
        register_buffer: register a buffer tensor to the module

    Methods:
        __init__(self, emb_size: int, dropout: float, maxlen: int = 5000):
            constructor method

        forward(self, token_embedding: Tensor):
            forward pass of the module
    """

    def __init__(self, emb_size: int, dropout: float, maxlen: int = 5000):
        """
        constructor method

        Args:
            emb_size (int): embedding size of the token embedding to which the positional encoding will be added
            dropout (float): dropout rate to apply to the sum of the token embedding and the positional encoding
            maxlen (int): maximum length of a sequence. Defaults to 5000.
        """
        super(PositionalEncoding, self).__init__()
        den = torch.exp(
            -torch.arange(0, emb_size, 2) * math.log(10000) / emb_size
        )  # den = 10000^(2i/emb_size) for i in range(emb_size//2)
        pos = torch.arange(0, maxlen).reshape(
            maxlen, 1
        )  # pos = [0, 1, 2, ..., maxlen-1] (maxlen, 1) tensor
        pos_embedding = torch.zeros(
            (maxlen, emb_size)
        )  # (maxlen, emb_size) tensor of zeros
        pos_embedding[:, 0::2] = torch.sin(
            pos * den
        )  # pos_embedding[:, 0::2] = sin(pos * den) for even indices of pos_embedding (i.e. 0, 2, 4, ..., emb_size-2)
        pos_embedding[:, 1::2] = torch.cos(
            pos * den
        )  # pos_embedding[:, 1::2] = cos(pos * den) for odd indices of pos_embedding (i.e. 1, 3, 5, ..., emb_size-1)
        pos_embedding = pos_embedding.unsqueeze(
            -2
        )  # pos_embedding = pos_embedding.unsqueeze(-2) = pos_embedding.unsqueeze(-2) = (maxlen, 1, emb_size)

        self.dropout = nn.Dropout(
            dropout
        )  # dropout layer to apply to the sum of the token embedding and the positional encoding
        self.register_buffer(
            "pos_embedding", pos_embedding
        )  # register the positional encoding as a buffer tensor

    def forward(self, token_embedding: Tensor):
        """
        forward pass of the module

        Args:
            token_embedding (Tensor): embedding of the tokens of shape (seq_len, batch_size, emb_size)

        Returns:
            Tensor: tensor of shape (seq_len, batch_size, emb_size) containing the sum of the token embedding and the positional encoding
        """
        return self.dropout(
            token_embedding + self.pos_embedding[: token_embedding.size(0), :]
        )
