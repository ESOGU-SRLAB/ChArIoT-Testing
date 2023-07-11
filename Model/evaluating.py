"""
    This module contains the evaluation loop for the model.
"""
from torch.utils.data import DataLoader

from dataset import MutationDataset
from config import BATCH_SIZE
from parameters import DEVICE
from collating import collate_fn
from masking import create_mask


def evaluate(X_val, y_val, model, loss_fn):
    """
    Evaluate the model.

    Args:
        X_val: The source validation data.
        y_val: The target validation data.
        model: The model to evaluate.
        loss_fn:    The loss function.

    Returns:
        The average loss for the epoch.
    """
    model.eval()  # set the model to evaluation mode
    losses = 0  # initialize the loss to 0

    val_iter = MutationDataset(X_val, y_val)  # create the validation dataset
    val_dataloader = DataLoader(
        val_iter, batch_size=BATCH_SIZE, collate_fn=collate_fn
    )  # create the validation dataloaders

    for src, tgt in val_dataloader:  # iterate over the validation dataloaders
        src = src.to(DEVICE)  # move the source data to the device
        tgt = tgt.to(DEVICE)  # move the target data to the device

        tgt_input = tgt[:-1, :]  # remove the last token from the target data

        src_mask, tgt_mask, src_padding_mask, tgt_padding_mask = create_mask(
            src, tgt_input
        )  # create the masks

        logits = model(
            src,
            tgt_input,
            src_mask,
            tgt_mask,
            src_padding_mask,
            tgt_padding_mask,
            src_padding_mask,
        )  # get the logits

        tgt_out = tgt[1:, :]  # remove the first token from the target data
        loss = loss_fn(
            logits.reshape(-1, logits.shape[-1]), tgt_out.reshape(-1)
        )  # calculate the loss
        losses += loss.item()  # add the loss to the total loss

    return losses / len(list(val_dataloader))
