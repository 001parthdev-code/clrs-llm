from pathlib import Path

INPUT_PATH = Path("data/corpus_semantic_clean.txt")

lines = INPUT_PATH.read_text(encoding="utf-8").splitlines()

for i in range(4280, 4350):
    print(f"{i + 1:>6} | {lines[i]!r}")