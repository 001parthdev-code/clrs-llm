import re
from pathlib import Path
from difflib import SequenceMatcher


INPUT_PATH = Path("data/corpus_semantic_clean.txt")

BODY_START = 781

SECTION_PATTERN = re.compile(
    r"^(\d+\.\d+(?:\.\d+)*)\s+(.+)$"
)


def normalize_title(title):
    """
    Normalize text so small OCR/cleaning differences
    do not prevent a title match.
    """
    title = title.lower()

    title = re.sub(r"[^a-z0-9\s]", " ", title)
    title = re.sub(r"\s+", " ", title)

    return title.strip()


def title_similarity(title_a, title_b):
    """
    Return similarity between two titles from 0 to 1.
    """
    a = normalize_title(title_a)
    b = normalize_title(title_b)

    return SequenceMatcher(None, a, b).ratio()


def extract_toc_sections(text):
    sections = []

    lines = text.splitlines()

    # Only inspect the TOC/front matter.
    for line_number, line in enumerate(
        lines[:BODY_START - 1],
        start=1
    ):
        match = SECTION_PATTERN.match(line.strip())

        if not match:
            continue

        number = match.group(1)
        title = match.group(2).strip()

        sections.append({
            "toc_line": line_number,
            "number": number,
            "title": title,
        })

    return sections


def locate_sections_in_body(text, toc_sections):
    lines = text.splitlines()

    # Map section number -> TOC title.
    toc_lookup = {
        section["number"]: section["title"]
        for section in toc_sections
    }

    body_candidates = []

    for line_number, line in enumerate(
        lines[BODY_START - 1:],
        start=BODY_START
    ):
        match = SECTION_PATTERN.match(line.strip())

        if not match:
            continue

        number = match.group(1)
        title = match.group(2).strip()

        # Ignore section numbers that don't exist in the TOC.
        if number not in toc_lookup:
            continue

        expected_title = toc_lookup[number]

        similarity = title_similarity(
            title,
            expected_title
        )

        body_candidates.append({
            "line": line_number,
            "number": number,
            "title": title,
            "expected_title": expected_title,
            "similarity": similarity,
        })

    return body_candidates


def filter_section_candidates(candidates):
    """
    Keep only candidates whose body title is sufficiently
    similar to the corresponding TOC title.
    """

    valid = []

    for candidate in candidates:

        similarity = candidate["similarity"]

        # Strong title match.
        if similarity >= 0.55:
            valid.append(candidate)

    return valid


def build_section_boundaries(sections, total_lines):
    """
    Convert section start lines into:

        section -> start line -> end line
    """

    boundaries = []

    for index, section in enumerate(sections):

        start_line = section["line"]

        if index + 1 < len(sections):
            end_line = sections[index + 1]["line"] - 1
        else:
            end_line = total_lines

        boundaries.append({
            "number": section["number"],
            "title": section["title"],
            "start": start_line,
            "end": end_line,
        })

    return boundaries


def main():
    text = INPUT_PATH.read_text(encoding="utf-8")

    lines = text.splitlines()

    # ---------------------------------------------------------
    # 1. Extract the authoritative section list from the TOC.
    # ---------------------------------------------------------

    toc_sections = extract_toc_sections(text)

    print(f"TOC sections: {len(toc_sections)}")

    # ---------------------------------------------------------
    # 2. Find possible section headings in the body.
    # ---------------------------------------------------------

    candidates = locate_sections_in_body(
        text,
        toc_sections
    )

    print(f"Body candidates: {len(candidates)}")

    # ---------------------------------------------------------
    # 3. Remove false positives using title similarity.
    # ---------------------------------------------------------

    valid_sections = filter_section_candidates(
        candidates
    )

    print(f"Valid body sections: {len(valid_sections)}")

    # ---------------------------------------------------------
    # 4. Show rejected candidates.
    # ---------------------------------------------------------

    print("\nRejected candidates:")

    for candidate in candidates:

        if candidate not in valid_sections:
            print(
                f"{candidate['line']:>6} | "
                f"{candidate['number']:<8} | "
                f"{candidate['title']}"
                f" | similarity={candidate['similarity']:.2f}"
            )

    # ---------------------------------------------------------
    # 5. Show accepted section headings.
    # ---------------------------------------------------------

    print("\nValid section boundaries:")

    for section in valid_sections:
        print(
            f"{section['line']:>6} | "
            f"{section['number']:<8} | "
            f"{section['title']}"
            f" | similarity={section['similarity']:.2f}"
        )

    # ---------------------------------------------------------
    # 6. Build actual start/end boundaries.
    # ---------------------------------------------------------

    sections_for_boundaries = [
        {
            "line": section["line"],
            "number": section["number"],
            "title": section["title"],
        }
        for section in valid_sections
    ]

    boundaries = build_section_boundaries(
        sections_for_boundaries,
        len(lines)
    )

    # ---------------------------------------------------------
    # 7. Save the boundaries.
    # ---------------------------------------------------------

    output_path = Path(
        "data/section_boundaries.txt"
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        for boundary in boundaries:
            f.write(
                f"{boundary['number']} | "
                f"{boundary['title']} | "
                f"{boundary['start']} | "
                f"{boundary['end']}\n"
            )

    print(
        f"\nSaved {len(boundaries)} section boundaries "
        f"to {output_path}"
    )


if __name__ == "__main__":
    main()