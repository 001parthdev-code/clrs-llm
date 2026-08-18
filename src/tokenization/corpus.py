from pathlib import Path


SECTIONS_DIR = Path("data/sections")


def load_corpus():
    texts = []

    section_files = sorted(SECTIONS_DIR.glob("*.txt"))

    for path in section_files:
        text = path.read_text(encoding="utf-8").strip()

        if text:
            texts.append(text)

    return texts


def main():
    texts = load_corpus()

    print(f"Loaded sections: {len(texts)}")
    print(f"Total characters: {sum(len(text) for text in texts):,}")

    if texts:
        print("\nFirst section preview:\n")
        print(texts[0][:1000])


if __name__ == "__main__":
    main()