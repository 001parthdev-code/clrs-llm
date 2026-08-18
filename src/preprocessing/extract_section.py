from pathlib import Path


CORPUS_PATH = Path("data/corpus_semantic_clean.txt")
BOUNDARIES_PATH = Path("data/section_boundaries.txt")
OUTPUT_DIR = Path("data/sections")


def load_boundaries(path):
    boundaries = []

    text = path.read_text(encoding="utf-8")

    for line in text.splitlines():
        parts = [part.strip() for part in line.split("|")]

        if len(parts) != 4:
            continue

        number = parts[0]
        title = parts[1]
        start_line = int(parts[2])
        end_line = int(parts[3])

        boundaries.append({
            "number": number,
            "title": title,
            "start": start_line,
            "end": end_line,
        })

    return boundaries


def extract_sections():
    corpus_lines = CORPUS_PATH.read_text(
        encoding="utf-8"
    ).splitlines()

    boundaries = load_boundaries(BOUNDARIES_PATH)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for section in boundaries:

        start = section["start"] - 1
        end = section["end"]

        section_lines = corpus_lines[start:end]

        content = "\n".join(section_lines).strip()

        filename = (
            f"{section['number'].replace('.', '_')}"
            f"_{section['title']}.txt"
        )

        # Remove characters Windows doesn't like in filenames.
        filename = filename.replace("?", "")
        filename = filename.replace("/", "-")
        filename = filename.replace("\\", "-")
        filename = filename.replace(":", "-")

        output_path = OUTPUT_DIR / filename

        output_path.write_text(
            content,
            encoding="utf-8"
        )

        print(
            f"{section['number']:>6} | "
            f"{section['title']} | "
            f"{len(section_lines)} lines"
        )

    print()
    print(f"Extracted: {len(boundaries)} sections")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    extract_sections()