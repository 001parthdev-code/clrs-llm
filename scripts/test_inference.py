from pathlib import Path

import torch

from src.model.config import ModelConfig
from src.model.transformer import CLRSLLM

config = ModelConfig()

model = CLRSLLM(config)

checkpoint = torch.load(
    Path("models") / "clrs_llm_best.pt",
    map_location="cpu",
    weights_only=False,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()

print("Inference model loaded successfully.")