import torch
import torch.nn as nn

from src.model.block import TransformerBlock
from src.model.config import ModelConfig
from src.model.embedding import TokenEmbedding
from src.model.positional_embedding import PositionalEmbedding


class CLRSLLM(nn.Module):
    """
    Decoder-only GPT-style Transformer.
    """

    def __init__(self, config: ModelConfig):

        super().__init__()

        self.config = config

        # ---------------------------------------------------------
        # Input
        # ---------------------------------------------------------

        self.token_embedding = TokenEmbedding(config)

        self.position_embedding = PositionalEmbedding(config)

        # ---------------------------------------------------------
        # Transformer Blocks
        # ---------------------------------------------------------

        self.blocks = nn.ModuleList(
            [
                TransformerBlock(config)
                for _ in range(config.num_layers)
            ]
        )

        # ---------------------------------------------------------
        # Final LayerNorm
        # ---------------------------------------------------------

        self.final_layer_norm = nn.LayerNorm(
            config.embedding_dim
        )

        # ---------------------------------------------------------
        # Language Model Head
        # ---------------------------------------------------------

        self.lm_head = nn.Linear(
            config.embedding_dim,
            config.vocab_size,
            bias=False,
        )

        # ---------------------------------------------------------
        # Weight Tying
        # ---------------------------------------------------------

        self.lm_head.weight = self.token_embedding.embedding.weight

    def forward(self, token_ids: torch.Tensor):

        # --------------------------------------------
        # Token Embeddings
        # --------------------------------------------

        x = self.token_embedding(token_ids)

        # --------------------------------------------
        # Positional Embeddings
        # --------------------------------------------

        x = self.position_embedding(x)

        # --------------------------------------------
        # Transformer
        # --------------------------------------------

        for block in self.blocks:

            x = block(x)

        # --------------------------------------------
        # Final LayerNorm
        # --------------------------------------------

        x = self.final_layer_norm(x)

        # --------------------------------------------
        # Vocabulary Logits
        # --------------------------------------------

        logits = self.lm_head(x)

        return logits