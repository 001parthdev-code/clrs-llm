from pathlib import Path

from torch.utils.data import DataLoader

from src.training.dataset import CLRSDataset


dataset = CLRSDataset(
    Path("data/training")
)

print(f"Dataset Size: {len(dataset)}")

loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True,
)

inputs, targets = next(iter(loader))

print(inputs.shape)
print(targets.shape)