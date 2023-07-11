"""
    This module contains the training loop for the model.
"""
from torch.utils.data import DataLoader

from dataset import MutationDataset
from config import BATCH_SIZE
from parameters import DEVICE
from collating import collate_fn
from masking import create_mask


def train_epoch(X_train, y_train, model, loss_fn, optimizer):
    """
    Train the model for one epoch.

    Args:
        X_train: The source training data.
        y_train: The target training data.
        model: The model to train.
        loss_fn: The loss function.
        optimizer: The optimizer.

    Returns:
        The average loss for the epoch.
    """
    model.train()  # set the model to training mode
    losses = 0  # initialize the loss to 0
    train_iter = MutationDataset(X_train, y_train)  # create the training dataset
    train_dataloader = DataLoader(
        train_iter, batch_size=BATCH_SIZE, collate_fn=collate_fn
    )  # create the training dataloaders

    for src, tgt in train_dataloader:  # iterate over the training dataloaders
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

        optimizer.zero_grad()  # zero the gradients

        tgt_out = tgt[1:, :]  # remove the first token from the target data
        loss = loss_fn(
            logits.reshape(-1, logits.shape[-1]), tgt_out.reshape(-1)
        )  # calculate the loss
        loss.backward()  # backpropagate the loss

        optimizer.step()  # update the parameters
        losses += loss.item()  # add the loss to the total loss

    return losses / len(list(train_dataloader))
