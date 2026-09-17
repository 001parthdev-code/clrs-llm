import json
from pathlib import Path

from src.tokenization.tokenizer import BPETokenizer


def main():

    print("===== CLRS-LLM DATASET TOKENIZER =====")

    # ---------------------------------------------------------
    # Project paths
    # ---------------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    sections_dir = project_root / "data" / "sections"
    output_dir = project_root / "data" / "tokenized"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # Locate section files
    # ---------------------------------------------------------

    section_files = sorted(
        sections_dir.glob("*.txt")
    )

    print(f"Found {len(section_files)} sections.")

    # ---------------------------------------------------------
    # Load tokenizer
    # ---------------------------------------------------------

    tokenizer_path = (
        project_root
        / "data"
        / "tokenizer.json"
    )

    tokenizer = BPETokenizer.load(
        tokenizer_path
    )

    print("Tokenizer loaded.\n")

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    stats = {
        "total_sections": 0,
        "total_tokens": 0,
        "shortest_section": None,
        "shortest_length": float("inf"),
        "longest_section": None,
        "longest_length": 0,
    }

    # ---------------------------------------------------------
    # Tokenize every section
    # ---------------------------------------------------------

    for section_file in section_files:

        print(f"Processing {section_file.name}...")

        text = section_file.read_text(
            encoding="utf-8"
        )

        token_ids = tokenizer.encode(
            text,
            add_bos=True,
            add_eos=True,
        )

        # -----------------------------
        # Validation
        # -----------------------------

        assert (
            token_ids[0]
            == tokenizer.special_tokens["<BOS>"]
        )

        assert (
            token_ids[-1]
            == tokenizer.special_tokens["<EOS>"]
        )

        # -----------------------------
        # Save tokenized section
        # -----------------------------

        output_file = (
            output_dir
            / f"{section_file.stem}.json"
        )

        data = {
            "section": section_file.stem,
            "token_count": len(token_ids),
            "tokens": token_ids,
        }

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        # -----------------------------
        # Update statistics
        # -----------------------------

        stats["total_sections"] += 1
        stats["total_tokens"] += len(token_ids)

        if len(token_ids) < stats["shortest_length"]:

            stats["shortest_length"] = len(token_ids)
            stats["shortest_section"] = section_file.stem

        if len(token_ids) > stats["longest_length"]:

            stats["longest_length"] = len(token_ids)
            stats["longest_section"] = section_file.stem

    # ---------------------------------------------------------
    # Final statistics
    # ---------------------------------------------------------

    average_tokens = (
        stats["total_tokens"]
        / stats["total_sections"]
    )

    print("\n===== DATASET SUMMARY =====")

    print(
        f"Sections: {stats['total_sections']}"
    )

    print(
        f"Total Tokens: {stats['total_tokens']}"
    )

    print(
        f"Average Tokens/Section: {average_tokens:.2f}"
    )

    print(
        f"Shortest Section: "
        f"{stats['shortest_section']} "
        f"({stats['shortest_length']} tokens)"
    )

    print(
        f"Longest Section: "
        f"{stats['longest_section']} "
        f"({stats['longest_length']} tokens)"
    )


if __name__ == "__main__":
    main()