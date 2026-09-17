import torch

from src.model.config import ModelConfig
from src.model.embedding import TokenEmbedding
from src.model.positional_embedding import PositionalEmbedding
from src.model.multihead_attention import MultiHeadAttention


config = ModelConfig()

embedding = TokenEmbedding(config)
position = PositionalEmbedding(config)
mha = MultiHeadAttention(config)

tokens = torch.tensor([
    [2, 54, 91, 18]
])

x = embedding(tokens)
x = position(x)

output = mha(x)

print(output.shape)