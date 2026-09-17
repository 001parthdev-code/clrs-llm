import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from src.model.config import ModelConfig


class MultiHeadSelfAttention(nn.Module):
    """
    GPT-style Multi-Head Causal Self-Attention.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        assert (
            config.embedding_dim % config.num_heads == 0
        ), "Embedding dimension must be divisible by number of heads."

        self.embedding_dim = config.embedding_dim
        self.num_heads = config.num_heads
        self.head_dim = config.embedding_dim // config.num_heads

        # ---------------------------------------------------------
        # QKV Projection
        # ---------------------------------------------------------

        self.qkv_projection = nn.Linear(
            config.embedding_dim,
            3 * config.embedding_dim,
        )

        # ---------------------------------------------------------
        # Output Projection
        # ---------------------------------------------------------

        self.output_projection = nn.Linear(
            config.embedding_dim,
            config.embedding_dim,
        )

        # ---------------------------------------------------------
        # Dropout
        # ---------------------------------------------------------

        self.dropout = nn.Dropout(config.dropout)

        # ---------------------------------------------------------
        # Causal Mask
        # ---------------------------------------------------------

        causal_mask = torch.triu(
            torch.ones(
                config.context_length,
                config.context_length,
            ),
            diagonal=1,
        ).bool()

        self.register_buffer(
            "causal_mask",
            causal_mask,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Input:
            (batch, sequence_length, embedding_dim)

        Output:
            (batch, sequence_length, embedding_dim)
        """

        batch_size, sequence_length, _ = x.shape

        # ---------------------------------------------------------
        # Project once -> Q K V
        # ---------------------------------------------------------

        qkv = self.qkv_projection(x)

        Q, K, V = qkv.chunk(
            3,
            dim=-1,
        )

        # ---------------------------------------------------------
        # Split into heads
        # ---------------------------------------------------------

        Q = (
            Q.view(
                batch_size,
                sequence_length,
                self.num_heads,
                self.head_dim,
            )
            .transpose(1, 2)
        )

        K = (
            K.view(
                batch_size,
                sequence_length,
                self.num_heads,
                self.head_dim,
            )
            .transpose(1, 2)
        )

        V = (
            V.view(
                batch_size,
                sequence_length,
                self.num_heads,
                self.head_dim,
            )
            .transpose(1, 2)
        )

        # ---------------------------------------------------------
        # Attention Scores
        # ---------------------------------------------------------

        scores = Q @ K.transpose(-2, -1)

        scores = scores / math.sqrt(self.head_dim)

        # ---------------------------------------------------------
        # Causal Mask
        # ---------------------------------------------------------

        mask = self.causal_mask[
            :sequence_length,
            :sequence_length,
        ]

        scores = scores.masked_fill(
            mask,
            float("-inf"),
        )

        # ---------------------------------------------------------
        # Attention Probabilities
        # ---------------------------------------------------------

        attention = F.softmax(
            scores,
            dim=-1,
        )

        attention = self.dropout(attention)

        # ---------------------------------------------------------
        # Weighted Sum
        # ---------------------------------------------------------

        output = attention @ V

        # ---------------------------------------------------------
        # Merge Heads
        # ---------------------------------------------------------

        output = (
            output.transpose(1, 2)
            .contiguous()
            .view(
                batch_size,
                sequence_length,
                self.embedding_dim,
            )
        )

        # ---------------------------------------------------------
        # Output Projection
        # ---------------------------------------------------------

        output = self.output_projection(output)

        return output