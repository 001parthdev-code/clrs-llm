import torch
import torch.nn as nn

from src.model.config import ModelConfig


class FeedForward(nn.Module):
    """
    Position-wise Feed Forward Network.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(
                config.embedding_dim,
                config.ffn_hidden_dim,
            ),

            nn.GELU(),

            nn.Linear(
                config.ffn_hidden_dim,
                config.embedding_dim,
            ),

            nn.Dropout(
                config.dropout,
            ),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        return self.network(x)