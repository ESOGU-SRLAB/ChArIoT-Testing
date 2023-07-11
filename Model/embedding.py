"""
    helper Module to convert tensor of input indices into corresponding tensor of token embeddings
"""
import math

import torch.nn as nn
from torch import Tensor


class TokenEmbedding(nn.Module):
    """
    token embedding module that maps vocab indices into embedding space

    Args:
        vocab_size (int): size of the vocabulary
        emb_size: size of the embedding

    Attributes:
        embedding (nn.Embedding): embedding matrix
        emb_size: size of the embedding

    Methods:
        __init__(self, vocab_size: int, emb_size):
            constructor method

        forward(self, tokens: Tensor):
            forward pass of the module
    """

    def __init__(self, vocab_size: int, emb_size):
        """
        constructor method

        Args:
            vocab_size (int): vocabulary size of the input tokens
            emb_size: size of the embedding
        """
        super(TokenEmbedding, self).__init__()
        self.embedding = nn.Embedding(
            vocab_size, emb_size
        )  # embedding matrix of size vocab_size x emb_size
        self.emb_size = emb_size  # size of the embedding

    def forward(self, tokens: Tensor):
        """
        forward pass of the module

        Args:
            tokens (Tensor): input tensor of tokens

        Returns:
            Tensor: tensor of token embeddings
        """
        return self.embedding(tokens.long()) * math.sqrt(self.emb_size)
