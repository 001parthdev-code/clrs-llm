import torch

from src.model.config import ModelConfig
from src.model.embedding import TokenEmbedding
from src.model.positional_embedding import PositionalEmbedding


config = ModelConfig()

token_embedding = TokenEmbedding(config)
position_embedding = PositionalEmbedding(config)

tokens = torch.tensor([
    [2, 54, 91, 18]
])

x = token_embedding(tokens)

print("Token Embeddings")
print(x.shape)

x = position_embedding(x)

print("After Positional Embeddings")
print(x.shape)