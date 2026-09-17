import torch

from src.model.config import ModelConfig
from src.model.embedding import TokenEmbedding


config = ModelConfig()

embedding = TokenEmbedding(config)

tokens = torch.tensor([
    [2, 54, 91, 18]
])

output = embedding(tokens)

print("Input Shape :", tokens.shape)
print("Output Shape:", output.shape)
print(output[0][0])