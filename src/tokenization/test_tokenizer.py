from tokenizer import BPETokenizer


TOKENIZER_PATH = "data/tokenizer.json"


def main():

    tokenizer = BPETokenizer.load(
        TOKENIZER_PATH
    )

    print(
        f"Vocabulary size: "
        f"{len(tokenizer.token_to_id)}"
    )

    print(
        f"Merges: "
        f"{len(tokenizer.merges)}"
    )

    text = (
        "Algorithms are fundamental "
        "to computer science."
    )

    print("\nOriginal:")
    print(text)

    token_ids = tokenizer.encode(
        text,
        add_bos=True,
        add_eos=True
    )

    print("\nToken IDs:")
    print(token_ids)

    print(
        f"\nToken count: "
        f"{len(token_ids)}"
    )

    decoded = tokenizer.decode(
        token_ids
    )

    print("\nDecoded:")
    print(decoded)


if __name__ == "__main__":
    main()