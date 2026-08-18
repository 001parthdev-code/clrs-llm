import re
from pathlib import Path


INPUT_PATH = Path("data/corpus_semantic_clean.txt")

BODY_START = 781

CHAPTERS = {
    1: "The Role of Algorithms in Computing",
    2: "Getting Started",
    3: "Characterizing Running Times",
    4: "Divide-and-Conquer",
    5: "Probabilistic Analysis and Randomized",
    6: "Heapsort",
    7: "Quicksort",
    8: "Sorting in Linear Time",
    9: "Medians and Order Statistics",
    10: "Elementary Data Structures",
    11: "Hash Tables",
    12: "Binary Search Trees",
    13: "Red-Black Trees",
    14: "Dynamic Programming",
    15: "Greedy Algorithms",
    16: "Amortized Analysis",
    17: "Augmenting Data Structures",
    18: "B-Trees",
    19: "Data Structures for Disjoint Sets",
    20: "Elementary Graph Algorithms",
    21: "Minimum Spanning Trees",
    22: "Single-Source Shortest Paths",
    23: "All-Pairs Shortest Paths",
    24: "Maximum Flow",
    25: "Matchings in Bipartite Graphs",
    26: "Parallel Algorithms",
    27: "Online Algorithms",
    28: "Matrix Operations",
    29: "Linear Programming",
    30: "Polynomials and the FFT",
    31: "Number-Theoretic Algorithms",
    32: "String Matching",
    33: "Machine-Learning Algorithms",
    34: "NP-Completeness",
    35: "Approximation Algorithms",
}


def detect_chapters(text):
    chapters = []

    lines = text.splitlines()

    for line_number, line in enumerate(lines[BODY_START - 1:], start=BODY_START):
        match = re.match(r"^(\d+)\s+(.+)$", line)

        if not match:
            continue

        number = int(match.group(1))
        title = match.group(2).strip()

        if number not in CHAPTERS:
            continue

        if title != CHAPTERS[number]:
            continue

        chapters.append({
            "line": line_number,
            "number": number,
            "title": title,
        })

    return chapters

def validate_chapters(chapters, total_lines):
    errors = []

    # Check 1: exactly 35 chapters
    if len(chapters) != 35:
        errors.append(
            f"Expected 35 chapters, found {len(chapters)}"
        )

    # Check 2: chapter numbers must be exactly 1 -> 35
    numbers = [chapter["number"] for chapter in chapters]
    expected_numbers = list(range(1, 36))

    if numbers != expected_numbers:
        errors.append(
            f"Invalid chapter sequence: {numbers}"
        )

    # Check 3: boundaries must be strictly increasing
    lines = [chapter["line"] for chapter in chapters]

    for previous, current in zip(lines, lines[1:]):
        if current <= previous:
            errors.append(
                f"Non-increasing boundary: {previous} -> {current}"
            )

    # Check 4: every chapter must have content
    for i, chapter in enumerate(chapters):
        start = chapter["line"]

        if i < len(chapters) - 1:
            end = chapters[i + 1]["line"] - 1
        else:
            end = total_lines

        if end <= start:
            errors.append(
                f"Chapter {chapter['number']} has invalid "
                f"range: {start} -> {end}"
            )

    # Check 5: first chapter starts where expected
    if chapters and chapters[0]["line"] != BODY_START:
        errors.append(
            f"First chapter starts at line "
            f"{chapters[0]['line']}, expected {BODY_START}"
        )

    # Check 6: last chapter starts within the corpus
    if chapters and chapters[-1]["line"] > total_lines:
        errors.append(
            f"Chapter 35 starts beyond EOF: "
            f"{chapters[-1]['line']} > {total_lines}"
        )

    if errors:
        print("\nBOUNDARY VALIDATION FAILED")

        for error in errors:
            print(f" - {error}")

        return False

    print("\nBOUNDARY VALIDATION PASSED")
    print(" - 35 chapters detected")
    print(" - Chapter sequence: 1 -> 35")
    print(" - Boundary lines strictly increasing")
    print(" - Every chapter has a valid range")
    print(f" - Body starts at line {BODY_START}")
    print(f" - Corpus ends at line {total_lines}")

    return True




def main():
    text = INPUT_PATH.read_text(encoding="utf-8")

    total_lines = len(text.splitlines())

    chapters = detect_chapters(text)

    print(f"Detected: {len(chapters)} chapters")

    for chapter in chapters:
        print(
            f"{chapter['line']:>6} | "
            f"{chapter['number']:>2} | "
            f"{chapter['title']}"
        )

    validate_chapters(chapters, total_lines)


if __name__ == "__main__":
    main()