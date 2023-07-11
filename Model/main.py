import torch
import torch.nn as nn

from seq2seq import Seq2SeqTransformer
from config import (
    NUM_ENCODER_LAYERS,
    NUM_DECODER_LAYERS,
    EMB_SIZE,
    NHEAD,
    FFN_HID_DIM,
)
from parameters import DEVICE, PAD_IDX


def main():

    print("Sergen")
    torch.manual_seed(0)

    transformer = Seq2SeqTransformer(
        NUM_ENCODER_LAYERS,
        NUM_DECODER_LAYERS,
        EMB_SIZE,
        NHEAD,
        SRC_VOCAB_SIZE,
        TGT_VOCAB_SIZE,
        FFN_HID_DIM,
    )

    for p in transformer.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)

    transformer = transformer.to(DEVICE)

    loss_fn = torch.nn.CrossEntropyLoss(ignore_index=PAD_IDX)

    optimizer = torch.optim.Adam(
        transformer.parameters(),
        lr=3e-4,
        betas=(0.9, 0.98),
        eps=1e-9,
        weight_decay=1e-4,
    )


if __name__ == "__main__":
    main()
