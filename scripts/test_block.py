import torch

from src.model.block import TransformerBlock
from src.model.config import ModelConfig

config = ModelConfig()

block = TransformerBlock(config)

x = torch.randn(
    2,
    32,
    config.embedding_dim,
)

y = block(x)

print(y.shape)