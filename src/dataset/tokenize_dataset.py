from  pathlib import Path
from src.tokenization.tokenizer import BPETokenizer

def main():
    print("====CLRS-LLM DATASET TOKENIZER=====")

    project_root = Path(__file__).resolve().parents[2]

    sections_dir = project_root/"data"/ "sections"
    output_dir = project_root/"data"/ "tokenized"

    output_dir.mkdir(exist_ok=True)
    print(sections_dir)
    print(output_dir)

    section_files = sorted(sections_dir.glob("*.txt"))

    print(f"Found {len(section_files)} sections.")

    tokenizer_path = project_root / "data" / "tokenizer.json"

    tokenizer = BPETokenizer.load(tokenizer_path)

    print("Tokenizer loaded.")

    
    print(f"Reading: {first_section.name}")

    text = first_section.read_text(encoding="utf-8")

    print(text[:200])

    token_ids = tokenizer.encode(
    text,
    add_bos=True,
    add_eos=True
)

    print(f"Generated {len(token_ids)} token IDs.")

    print(token_ids[:20])

    print(f"First token: {token_ids[0]}")
    print(f"Last token: {token_ids[-1]}")

    assert token_ids[0] == tokenizer.special_tokens["<BOS>"]
    assert token_ids[-1] == tokenizer.special_tokens["<EOS>"]

    print("BOS/EOS validation passed.")

if __name__ == "__main__":
    main()