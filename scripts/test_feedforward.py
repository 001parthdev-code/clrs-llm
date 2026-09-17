import torch

from src.model.config import ModelConfig
from src.model.feedforward import FeedForward

config = ModelConfig()

ffn = FeedForward(config)

x = torch.randn(
    2,
    128,
    config.embedding_dim,
)

y = ffn(x)

print(x.shape)
print(y.shape)