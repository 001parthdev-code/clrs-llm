import json
from pathlib import Path

from tokenizer import BPETokenizer


BPE_MODEL_PATH = Path(
    "data/bpe_model.json"
)

TOKENIZER_PATH = Path(
    "data/tokenizer.json"
)


def main():

    # ---------------------------------------------------------
    # Load trained BPE
    # ---------------------------------------------------------

    data = json.loads(
        BPE_MODEL_PATH.read_text(
            encoding="utf-8"
        )
    )

    vocabulary = set(
        data["vocabulary"]
    )

    merges = [
        tuple(merge)
        for merge in data["merges"]
    ]

    print(
        f"Loaded vocabulary: "
        f"{len(vocabulary)}"
    )

    print(
        f"Loaded merges: "
        f"{len(merges)}"
    )

    # ---------------------------------------------------------
    # Build tokenizer
    # ---------------------------------------------------------

    tokenizer = BPETokenizer()

    tokenizer.build_vocabulary(
        vocabulary,
        merges
    )

    # ---------------------------------------------------------
    # Save tokenizer
    # ---------------------------------------------------------

    tokenizer.save(
        TOKENIZER_PATH
    )

    print(
        f"Saved tokenizer to "
        f"{TOKENIZER_PATH}"
    )

    print(
        f"Final tokenizer vocabulary: "
        f"{len(tokenizer.token_to_id)}"
    )


if __name__ == "__main__":
    main()