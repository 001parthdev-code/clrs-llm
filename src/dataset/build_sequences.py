import json
from pathlib import Path

import numpy as np

# ============================================================
# Configuration
# ============================================================

CONTEXT_LENGTH = 128


def build_sequences(token_ids, context_length):
    """
    Convert one token sequence into many
    (input, target) training examples.
    """

    inputs = []
    targets = []

    # Need at least context_length + 1 tokens
    if len(token_ids) <= context_length:
        return inputs, targets

    for start in range(len(token_ids) - context_length):

        input_sequence = token_ids[start:start + context_length]

        target_sequence = token_ids[start + 1:start + context_length + 1]

        inputs.append(input_sequence)
        targets.append(target_sequence)

    return inputs, targets


def main():

    print("===== BUILD TRAINING DATASET =====")

    # ---------------------------------------------------------
    # Paths
    # ---------------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    tokenized_dir = project_root / "data" / "tokenized"

    output_dir = project_root / "data" / "training"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # Locate tokenized sections
    # ---------------------------------------------------------

    section_files = sorted(
        tokenized_dir.glob("*.json")
    )

    print(f"Found {len(section_files)} tokenized sections.\n")

    # ---------------------------------------------------------
    # Dataset
    # ---------------------------------------------------------

    all_inputs = []
    all_targets = []

    # ---------------------------------------------------------
    # Process every section
    # ---------------------------------------------------------

    for section_file in section_files:

        print(f"Processing {section_file.name}")

        data = json.loads(
            section_file.read_text(
                encoding="utf-8"
            )
        )

        token_ids = data["tokens"]

        inputs, targets = build_sequences(
            token_ids,
            CONTEXT_LENGTH,
        )

        all_inputs.extend(inputs)
        all_targets.extend(targets)

    # ---------------------------------------------------------
    # Convert to NumPy
    # ---------------------------------------------------------

    inputs_array = np.array(
        all_inputs,
        dtype=np.int32,
    )

    targets_array = np.array(
        all_targets,
        dtype=np.int32,
    )

    # ---------------------------------------------------------
    # Save dataset
    # ---------------------------------------------------------

    np.save(
        output_dir / "inputs.npy",
        inputs_array,
    )

    np.save(
        output_dir / "targets.npy",
        targets_array,
    )

    metadata = {
        "context_length": CONTEXT_LENGTH,
        "num_examples": int(inputs_array.shape[0]),
        "sequence_length": CONTEXT_LENGTH,
        "vocab_size": 8196,
        "dtype": "int32",
    }

    with open(
        output_dir / "metadata.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print("\n===== SUMMARY =====")

    print(f"Training Examples : {inputs_array.shape[0]}")
    print(f"Sequence Length   : {CONTEXT_LENGTH}")
    print(f"Input Shape       : {inputs_array.shape}")
    print(f"Target Shape      : {targets_array.shape}")

    print("\nDataset written to:")

    print(output_dir)


if __name__ == "__main__":
    main()