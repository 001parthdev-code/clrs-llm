from pathlib import Path
from collections import Counter
import re
import unicodedata


CORPUS_PATH = Path("data/corpus_semantic_clean.txt")


def load_corpus(path):
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        "Could not decode corpus with supported encodings",
    )


def profile_basic(text):
    lines = text.splitlines()

    non_empty_lines = [line for line in lines if line.strip()]

    words = text.split()

    print("\n=== BASIC CORPUS PROFILE ===")
    print(f"Characters: {len(text):,}")
    print(f"Lines: {len(lines):,}")
    print(f"Empty lines: {len(lines) - len(non_empty_lines):,}")
    print(f"Non-empty lines: {len(non_empty_lines):,}")
    print(f"Whitespace-separated words: {len(words):,}")

    if lines:
        print(f"Shortest line: {min(map(len, lines))}")
        print(f"Longest line: {max(map(len, lines))}")


def profile_line_lengths(text):
    lines = text.splitlines()
    ranges = Counter()

    for line in lines:
        length = len(line)

        start = (length // 10) * 10
        end = start + 9

        ranges[f"{start}-{end}"] += 1

    print("\n=== LINE LENGTH DISTRIBUTION ===")

    for bucket, count in sorted(
        ranges.items(),
        key=lambda x: int(x[0].split("-")[0])
    ):
        print(f"{bucket:>8}: {count:,}")


def profile_repeated_lines(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    counts = Counter(lines)

    print("\n=== MOST REPEATED LINES ===")

    for line, count in counts.most_common(30):
        print(f"{count:>5}x | {repr(line)}")


def profile_characters(text):
    counts = Counter(text)

    print("\n=== MOST COMMON CHARACTERS ===")

    for char, count in counts.most_common(50):
        if char == " ":
            display = "<SPACE>"
        elif char == "\n":
            display = "<NEWLINE>"
        elif char == "\t":
            display = "<TAB>"
        elif char == "\r":
            display = "<CR>"
        else:
            display = repr(char)

        print(f"{count:>10,} | {display}")


def profile_non_ascii(text):
    counts = Counter(
        char for char in text
        if ord(char) > 127
    )

    print("\n=== NON-ASCII CHARACTERS ===")

    for char, count in counts.most_common():
        codepoint = f"U+{ord(char):04X}"
        name = unicodedata.name(char, "UNKNOWN")

        print(
            f"{count:>8,} | "
            f"{codepoint} | "
            f"{repr(char):>8} | "
            f"{name}"
        )


def profile_whitespace(text):
    lines = text.splitlines()

    leading_spaces = sum(
        len(line) - len(line.lstrip(" "))
        for line in lines
        if line
    )

    trailing_spaces = sum(
        len(line) - len(line.rstrip(" "))
        for line in lines
        if line
    )

    tabs = text.count("\t")
    double_spaces = len(re.findall(r" {2,}", text))

    print("\n=== WHITESPACE PROFILE ===")
    print(f"Leading spaces: {leading_spaces:,}")
    print(f"Trailing spaces: {trailing_spaces:,}")
    print(f"Tabs: {tabs:,}")
    print(f"Runs of 2+ spaces: {double_spaces:,}")


def profile_suspicious_characters(text):
    suspicious = Counter()

    for char in text:
        category = unicodedata.category(char)

        if category.startswith("C"):
            suspicious[char] += 1

    print("\n=== SUSPICIOUS CONTROL / FORMAT CHARACTERS ===")

    for char, count in suspicious.most_common():
        codepoint = f"U+{ord(char):04X}"
        name = unicodedata.name(char, "UNKNOWN")

        print(
            f"{count:>8,} | "
            f"{codepoint} | "
            f"{repr(char):>8} | "
            f"{name}"
        )


def profile_number_like_lines(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    number_like = []

    for line in lines:
        if re.fullmatch(r"[\d\s\-–—]+", line):
            number_like.append(line)

    print("\n=== NUMBER-LIKE LINES ===")
    print(f"Count: {len(number_like):,}")

    for line in number_like[:30]:
        print(repr(line))


def profile_samples(text):
    lines = text.splitlines()

    print("\n=== BEGINNING SAMPLE ===")
    for line in lines[:20]:
        print(repr(line))

    print("\n=== MIDDLE SAMPLE ===")
    middle = len(lines) // 2

    for line in lines[middle:middle + 20]:
        print(repr(line))

    print("\n=== END SAMPLE ===")
    for line in lines[-20:]:
        print(repr(line))


def main():
    print(f"Corpus: {CORPUS_PATH.resolve()}")

    text, encoding = load_corpus(CORPUS_PATH)

    print(f"Encoding used: {encoding}")

    profile_basic(text)
    profile_line_lengths(text)
    profile_repeated_lines(text)
    profile_characters(text)
    profile_non_ascii(text)
    profile_whitespace(text)
    profile_suspicious_characters(text)
    profile_number_like_lines(text)
    profile_samples(text)


if __name__ == "__main__":
    main()