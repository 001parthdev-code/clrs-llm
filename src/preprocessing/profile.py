from pathlib import Path
from collections import Counter

"Define File Path"
corpus_Path = Path("D:\clrs-llm\data\corpus_raw.txt")

def main():
    text = corpus_Path.read_text(encoding="cp1252") # UTF-8 was not used since
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa9
    lines = text.splitlines()

    total_chars = len(text)
    total_lines = len(lines)
    empty_lines = sum(1 for line in lines if not line.strip())

    words = text.split()
    total_words = len(words)

    line_lengths = [len(line) for line in lines]

    print("=== CORPUS PROFILE ===")
    print(f"File: {corpus_Path}")
    print(f"Characters: {total_chars:,}")
    print(f"Lines: {total_lines:,}")
    print(f"Empty lines: {empty_lines:,}")
    print(f"Whitespace-separated words: {total_words:,}")
    print(f"Shortest line: {min(line_lengths)} characters")
    print(f"Longest line: {max(line_lengths)} characters")


if __name__ == "__main__":
    main()