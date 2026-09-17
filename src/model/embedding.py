import torch
import torch.nn as nn

from src.model.config import ModelConfig


class TokenEmbedding(nn.Module):
    """
    Converts token IDs into dense vectors.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.embedding_dim,
        )

    def forward(self, token_ids: torch.Tensor):

        return self.embedding(token_ids)