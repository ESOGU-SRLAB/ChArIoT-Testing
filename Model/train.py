"""
    This file contains the training loop for the model.
"""
from timeit import default_timer as timer
import matplotlib.pyplot as plt

from config import NUM_EPOCHS
from training import train_epoch
from evaluating import evaluate
from save import save_network


def train_model(X_train, y_train, X_val, y_val, transformer, loss_fn, optimizer):
    """
    Trains the model for the specified number of epochs.

    Args:
        transformer: The model to be trained.
        loss_fn: The loss function to be used for training.
        optimizer: The optimizer to be used for training.
    """
    train_losses = []  # initialize the list of training losses
    val_losses = []  # initialize the list of validation losses
    for epoch in range(1, NUM_EPOCHS + 1):  # +1 because range is exclusive
        start_time = timer()  # Start timer
        train_loss = train_epoch(
            X_train, y_train, transformer, loss_fn, optimizer
        )  # Train model for one epoch
        train_losses.append(train_loss)  # Add training loss to list of training losses
        end_time = timer()  # Stop timer
        val_loss = evaluate(
            X_val, y_val, transformer, loss_fn
        )  # Evaluate model on validation set
        val_losses.append(val_loss)  # Add validation loss to list of validation losses

        print(
            (
                f"Epoch: {epoch}, Train loss: {train_loss:.3f}, Val loss: {val_loss:.3f}, "
                f"Epoch time = {(end_time - start_time):.3f}s"
            )
        )

        if epoch % 5 == 0:
            save_network(transformer, epoch)
            plt.plot(range(1, len(train_losses) + 1), train_losses, label="train loss")
            plt.plot(range(1, len(val_losses) + 1), val_losses, label="val loss")
            plt.legend()
            plt.show()
