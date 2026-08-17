from pathlib import Path
import unicodedata
import re


INPUT_PATH = Path("data/corpus_raw.txt")
OUTPUT_PATH = Path("data/corpus_clean.txt")


def load_text(path):
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        "Unable to decode corpus",
    )


def normalize_unicode(text):
    text = unicodedata.normalize("NFC", text)

    # Remove soft hyphen extraction artifacts.
    text = text.replace("\u00ad", "")

    # Form-feed represents PDF page boundaries.
    text = text.replace("\f", "\n")

    return text


def normalize_whitespace(text):
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        # Remove trailing whitespace.
        line = line.rstrip()

        # Remove layout indentation.
        line = line.strip()

        # Collapse repeated spaces inside a line.
        line = re.sub(r" {2,}", " ", line)

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def repair_hyphenation(text):
    # Join words broken across a line by PDF extraction.
    #
    # Example:
    # algo-
    # rithm
    #
    # becomes:
    # algorithm

    text = re.sub(
        r"(?<=\w)-\n(?=\w)",
        "",
        text,
    )

    return text


def normalize_blank_lines(text):
    # Preserve paragraph separation,
    # but prevent huge runs of blank lines.

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def clean_corpus(text):
    text = normalize_unicode(text)
    text = repair_hyphenation(text)
    text = normalize_whitespace(text)
    text = normalize_blank_lines(text)

    return text


def main():
    print(f"Input:  {INPUT_PATH.resolve()}")
    print(f"Output: {OUTPUT_PATH.resolve()}")

    text = load_text(INPUT_PATH)

    print(f"Raw characters: {len(text):,}")

    cleaned = clean_corpus(text)

    OUTPUT_PATH.write_text(
        cleaned,
        encoding="utf-8",
        newline="\n",
    )

    print(f"Clean characters: {len(cleaned):,}")
    print("Cleaning complete.")


if __name__ == "__main__":
    main()