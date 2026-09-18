from pathlib import Path

import torch

from src.model.config import ModelConfig
from src.model.transformer import CLRSLLM
from src.tokenization.tokenizer import BPETokenizer


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MAX_NEW_TOKENS = 100


def main():

    # ---------------------------------------------------------
    # Device
    # ---------------------------------------------------------

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Using {device}")

    project_root = Path(__file__).resolve().parents[2]

    # ---------------------------------------------------------
    # Load Tokenizer
    # ---------------------------------------------------------

    tokenizer = BPETokenizer.load(
        project_root / "data" / "tokenizer.json"
    )

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    checkpoint = torch.load(
        project_root / "models" / "clrs_llm_best.pt",
        map_location=device,
        weights_only=False,
    )

    config = ModelConfig()

    model = CLRSLLM(config).to(device)

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    print("\nCLRS-LLM Ready!")
    print("Type 'exit' to quit.")

    # ---------------------------------------------------------
    # Interactive Loop
    # ---------------------------------------------------------

    while True:

        prompt = input("\nPrompt: ")

        if prompt.lower() == "exit":
            break

        if not prompt.strip():
            continue

        # -----------------------------------------------------
        # Encode Prompt
        # -----------------------------------------------------

        token_ids = tokenizer.encode(
            prompt,
            add_bos=True,
        )

        tokens = torch.tensor(
            [token_ids],
            dtype=torch.long,
            device=device,
        )

        # -----------------------------------------------------
        # Generate
        # -----------------------------------------------------

        with torch.no_grad():

            for _ in range(MAX_NEW_TOKENS):

                tokens = tokens[
                    :,
                    -config.context_length:
                ]

                logits = model(tokens)

                next_token_logits = logits[:, -1, :]

                next_token = torch.argmax(
                    next_token_logits,
                    dim=-1,
                    keepdim=True,
                )

                tokens = torch.cat(
                    [tokens, next_token],
                    dim=1,
                )

                if (
                    next_token.item()
                    == tokenizer.special_tokens["<EOS>"]
                ):
                    break

        # -----------------------------------------------------
        # Decode
        # -----------------------------------------------------

        generated_ids = tokens.squeeze(0).tolist()

        generated_text = tokenizer.decode(
            generated_ids
        )

        print()
        print("=" * 60)
        print(generated_text)
        print("=" * 60)


if __name__ == "__main__":
    main()