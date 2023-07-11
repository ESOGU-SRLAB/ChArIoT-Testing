"""
    This file contains the implementation of the Seq2Seq Transformer model.
"""

from torch import Tensor
import torch.nn as nn
from torch.nn import Transformer

from embedding import TokenEmbedding
from encoding import PositionalEncoding


class Seq2SeqTransformer(nn.Module):
    """
    seq2seqtransformer module that contains the encoder and decoder

    Args:
        num_encoder_layers (int): number of encoder layers
        num_decoder_layers (int): number of decoder layers
        emb_size (int): embedding size
        nhead (int): number of attention heads
        src_vocab_size (int): size of the source vocabulary
        tgt_vocab_size (int): size of the target vocabulary
        dim_feedforward (int): size of the feedforward network model. Defaults to 512.
        dropout (float): dropout rate. Defaults to 0.1.

    Attributes:
        transformer: transformer module that contains the encoder and decoder layers and the feedforward network model
        generator: linear layer that maps the output of the transformer to the target vocabulary
        src_tok_emb: token embedding layer for the source vocabulary
        tgt_tok_emb: token embedding layer for the target vocabulary
        positional_encoding: positional encoding module that adds positional information to the token embedding

    Methods:
        __init__(self, num_encoder_layers: int, num_decoder_layers: int, emb_size: int, nhead: int, src_vocab_size: int, tgt_vocab_size: int, dim_feedforward: int = 512, dropout: float = 0.1):
            constructor method

        forward(self, src: Tensor, trg: Tensor, src_mask: Tensor, tgt_mask: Tensor, src_padding_mask: Tensor, tgt_padding_mask: Tensor, memory_key_padding_mask: Tensor):
            forward pass of the module

        encode(self, src: Tensor, src_mask: Tensor):
            encode the source sequence by passing it through the encoder layers

        decode(self, tgt: Tensor, memory: Tensor, tgt_mask: Tensor):
            decode the target sequence by passing it through the decoder layers
    """

    def __init__(
        self,
        num_encoder_layers: int,
        num_decoder_layers: int,
        emb_size: int,
        nhead: int,
        src_vocab_size: int,
        tgt_vocab_size: int,
        dim_feedforward: int = 512,
        dropout: float = 0.1,
    ):
        """
        constructor method

        Args:
            num_encoder_layers (int): number of encoder layers
            num_decoder_layers (int): number of decoder layers
            emb_size (int): embedding size
            nhead (int): number of attention heads
            src_vocab_size (int): the size of the source vocabulary
            tgt_vocab_size (int): the size of the target vocabulary
            dim_feedforward (int): the size of the feedforward network model. Defaults to 512.
            dropout (float): dropout rate. Defaults to 0.1.
        """
        super(Seq2SeqTransformer, self).__init__()
        self.transformer = Transformer(
            d_model=emb_size,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
        )  # transformer module that contains the encoder and decoder layers and the feedforward network model
        self.generator = nn.Linear(
            emb_size, tgt_vocab_size
        )  # linear layer that maps the output of the transformer to the target vocabulary
        self.src_tok_emb = TokenEmbedding(
            src_vocab_size, emb_size
        )  # token embedding layer for the source vocabulary
        self.tgt_tok_emb = TokenEmbedding(
            tgt_vocab_size, emb_size
        )  # token embedding layer for the target vocabulary
        self.positional_encoding = PositionalEncoding(
            emb_size, dropout=dropout
        )  # positional encoding module that adds positional information to the token embedding

    def forward(
        self,
        src: Tensor,
        trg: Tensor,
        src_mask: Tensor,
        tgt_mask: Tensor,
        src_padding_mask: Tensor,
        tgt_padding_mask: Tensor,
        memory_key_padding_mask: Tensor,
    ):
        """
        forward pass of the module

        Args:
            src (Tensor): source tensor of shape (src_len, batch_size)
            trg (Tensor): target tensor of shape (trg_len, batch_size)
            src_mask (Tensor): source mask tensor of shape (src_len, src_len)
            tgt_mask (Tensor): target mask tensor of shape (trg_len, trg_len)
            src_padding_mask (Tensor): source padding mask tensor of shape (batch_size, src_len)
            tgt_padding_mask (Tensor): target padding mask tensor of shape (batch_size, trg_len)
            memory_key_padding_mask (Tensor): memory key padding mask tensor of shape (batch_size, src_len)

        Returns:
            Tensor: output tensor of shape (trg_len, batch_size, tgt_vocab_size)
        """
        src_emb = self.positional_encoding(
            self.src_tok_emb(src)
        )  # positional encoding of the source token embedding
        tgt_emb = self.positional_encoding(
            self.tgt_tok_emb(trg)
        )  # positional encoding of the target token embedding
        outs = self.transformer(
            src_emb,
            tgt_emb,
            src_mask,
            tgt_mask,
            None,
            src_padding_mask,
            tgt_padding_mask,
            memory_key_padding_mask,
        )  # transformer output
        return self.generator(outs)

    def encode(self, src: Tensor, src_mask: Tensor):
        """
        encode the source sequence by passing it through the encoder layers

        Args:
            src (Tensor): source tensor of shape (src_len, batch_size)
            src_mask (Tensor): source mask tensor of shape (src_len, src_len)

        Returns:
            Tensor: output tensor of shape (src_len, batch_size, emb_size)
        """
        return self.transformer.encoder(
            self.positional_encoding(self.src_tok_emb(src)), src_mask
        )

    def decode(self, tgt: Tensor, memory: Tensor, tgt_mask: Tensor):
        """
        decode the target sequence by passing it through the decoder layers

        Args:
            tgt (Tensor): target tensor of shape (trg_len, batch_size)
            memory (Tensor): memory tensor of shape (src_len, batch_size, emb_size)
            tgt_mask (Tensor): target mask tensor of shape (trg_len, trg_len)

        Returns:
            Tensor: output tensor of shape (trg_len, batch_size, emb_size)
        """
        return self.transformer.decoder(
            self.positional_encoding(self.tgt_tok_emb(tgt)), memory, tgt_mask
        )
