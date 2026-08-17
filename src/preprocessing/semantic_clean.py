from pathlib import Path

INPUT_PATH = Path("data/corpus_clean.txt")
OUTPUT_PATH = Path("data/corpus_semantic_clean.txt")

START_MARKER = "1 The Role of Algorithms in Computing"


def remove_front_matter(text):
    start = text.find(START_MARKER)

    if start == -1:
        raise ValueError(f"Could not find start marker: {START_MARKER!r}")

    return text[start:]


def remove_index(text):
    marker = "\nIndex\n"

    first = text.find(marker)

    if first == -1:
        raise ValueError("Index marker not found")

    second = text.find(marker, first + len(marker))

    if second == -1:
        raise ValueError("Second Index marker not found")

    return text[:second]


def clean_semantic(text):
    text = remove_front_matter(text)
    text = remove_index(text)

    return text


def main():
    text = INPUT_PATH.read_text(encoding="utf-8")

    print(f"Input characters: {len(text):,}")

    cleaned = clean_semantic(text)

    OUTPUT_PATH.write_text(
        cleaned,
        encoding="utf-8",
        newline="\n",
    )

    print(f"Output characters: {len(cleaned):,}")
    print("Semantic cleaning complete.")


if __name__ == "__main__":
    main()