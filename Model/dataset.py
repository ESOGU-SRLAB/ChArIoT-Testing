"""
    This file contains the dataset class for the mutation dataset.
"""
from torch.utils.data import Dataset


class MutationDataset(Dataset):
    """
    MutationDataset class for the mutation dataset that inherits from the Dataset class.

    Args:
        fixed: The fixed code snippets.
        buggy: The buggy code snippets.
        transform: The transformation to apply to the fixed code snippets.
        target_transform: The transformation to apply to the buggy code snippets.

    Attributes:
        fixed: The fixed code snippets.
        buggy: The buggy code snippets.
        transform: The transformation to apply to the fixed code snippets.
        target_transform: The transformation to apply to the buggy code snippets.

    Methods:
        __init__(self, fixed, buggy, transform=None, target_transform=None):
            constructor method

        __len__(self):
            returns the length of the dataset

        __getitem__(self, idx):
            returns the fixed and buggy code snippets at the given index
    """

    def __init__(self, fixed, buggy, transform=None, target_transform=None):
        """
        constructor method

        Args:
            fixed: The fixed code snippets.
            buggy: The buggy code snippets.
            transform: The transformation to apply to the fixed code snippets. Defaults to None.
            target_transform: The transformation to apply to the buggy code snippets. Defaults to None.
        """
        super(MutationDataset, self).__init__()

        self.fixed = fixed  # fixed code snippets
        self.buggy = buggy  # buggy code snippets
        self.transform = transform  # transformation to apply to the fixed code snippets
        self.target_transform = (
            target_transform  # transformation to apply to the buggy code snippets
        )

    def __len__(self):
        """
        returns the length of the dataset

        Returns:
            int: length of the dataset
        """
        return len(self.fixed)

    def __getitem__(self, idx):
        """
        returns the fixed and buggy code snippets at the given index

        Args:
            idx: index of the code snippets to return

        Returns:
            fixed: fixed code snippet at the given index
            buggy: buggy code snippet at the given index
        """
        fixed = self.fixed[idx]  # fixed code snippet at the given index
        buggy = self.buggy[idx]  # buggy code snippet at the given index

        if self.transform:  # apply the transformation to the fixed code snippet
            fixed = self.transform(
                fixed
            )  # apply the transformation to the fixed code snippet
        if self.target_transform:  # apply the transformation to the buggy code snippet
            buggy = self.target_transform(
                buggy
            )  # apply the transformation to the buggy code snippet

        return fixed, buggy
