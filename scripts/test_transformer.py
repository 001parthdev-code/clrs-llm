import torch

from src.model.config import ModelConfig
from src.model.transformer import CLRSLLM

config = ModelConfig()

model = CLRSLLM(config)

tokens = torch.randint(
    0,
    config.vocab_size,
    (2, 32),
)

logits = model(tokens)

print("Input")
print(tokens.shape)

print()

print("Output")
print(logits.shape)