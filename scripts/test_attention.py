import torch

from src.model.attention import MultiHeadSelfAttention
from src.model.config import ModelConfig
from src.model.embedding import TokenEmbedding
from src.model.positional_embedding import PositionalEmbedding


config = ModelConfig()

embedding = TokenEmbedding(config)
position = PositionalEmbedding(config)
attention = MultiHeadSelfAttention(config)

tokens = torch.tensor([
    [2, 54, 91, 18]
])

x = embedding(tokens)
x = position(x)

print("Input Shape :", x.shape)

output = attention(x)

print("Output Shape:", output.shape)