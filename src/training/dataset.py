from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset


class CLRSDataset(Dataset):
    """
    Loads the preprocessed CLRS training dataset.
    """

    def __init__(self, data_dir: Path):

        self.inputs = np.load(
            data_dir / "inputs.npy"
        )

        self.targets = np.load(
            data_dir / "targets.npy"
        )

    def __len__(self):

        return len(self.inputs)

    def __getitem__(self, index):

        x = torch.tensor(
            self.inputs[index],
            dtype=torch.long,
        )

        y = torch.tensor(
            self.targets[index],
            dtype=torch.long,
        )

        return x, y