import pymupdf

pdf_path = "PATH"
output_path = "data/corpus_raw.txt"

doc = pymupdf.open(pdf_path)

with open(output_path, "w", encoding="utf-8") as f:
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        f.write(text)
        f.write("\n\n")

        if page_num % 50 == 0:
            print(f"Processed {page_num}/{len(doc)} pages")

print(f"Done. Extracted {len(doc)} pages.")
print(f"Output: {output_path}")