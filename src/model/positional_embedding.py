import torch
import torch.nn as nn

from src.model.config import ModelConfig


class PositionalEmbedding(nn.Module):
    """
    Learns a vector representation for each position in the sequence.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=config.context_length,
            embedding_dim=config.embedding_dim,
        )

    def forward(self, token_embeddings: torch.Tensor):

        batch_size, sequence_length, _ = token_embeddings.shape

        positions = torch.arange(
            sequence_length,
            device=token_embeddings.device,
        )

        position_embeddings = self.embedding(positions)

        return token_embeddings + position_embeddings