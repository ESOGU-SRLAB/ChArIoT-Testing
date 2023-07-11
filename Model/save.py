"""
    This file is used to save the model weights after each epoch.
"""

import os
import torch


def save_network(model, epoch):
    """
    Save the model weights after each epoch.

    Args:
        model: The model to save.
        epoch: The epoch number.
    """
    save_filename = "model_weights-%s.pth" % (epoch)  # create the save filename
    save_path = os.path.join("./savedModels", save_filename)  # create the save path
    torch.save(model.state_dict(), save_path)  # save the model weights
