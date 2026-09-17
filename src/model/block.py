import torch
import torch.nn as nn

from src.model.attention import MultiHeadSelfAttention
from src.model.config import ModelConfig
from src.model.feedforward import FeedForward


class TransformerBlock(nn.Module):
    """
    Single GPT Transformer Block.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        self.ln1 = nn.LayerNorm(
            config.embedding_dim,
        )

        self.attention = MultiHeadSelfAttention(
            config,
        )

        self.ln2 = nn.LayerNorm(
            config.embedding_dim,
        )

        self.feedforward = FeedForward(
            config,
        )

    def forward(self, x: torch.Tensor):

        # ----------------------------------------
        # Attention
        # ----------------------------------------

        x = x + self.attention(
            self.ln1(x)
        )

        # ----------------------------------------
        # Feed Forward
        # ----------------------------------------

        x = x + self.feedforward(
            self.ln2(x)
        )

        return x