#clrs-llm

16th August:

Pipeline: PDF -> Text -> Tokens -> TokenID -> Training Sequence -> LLM

Phase 0: Data extraction

1. I needed to extract text from PDF to a machine readable text.
2. I used Poppler's `pdftotext` utility to extract the text.
3. The first PDF was corrupted and `pdftotext` returned xref/trailer errors.
4. I replaced the PDF with a new copy.
5. I extracted the text into `data/corpus_raw.txt`.
6. The extracted corpus contained 68,590 lines and 447,292 whitespace-separated words.

Phase 0.1: Corpus profiling

1. Before cleaning the corpus, I profiled the extracted text to understand what I was actually working with.
2. The corpus contained:
   - 2,600,328 characters
   - 68,590 lines
   - 23,047 empty lines
   - 447,292 whitespace-separated words
   - Shortest line: 0 characters
   - Longest line: 109 characters
3. I checked the distribution of line lengths.
4. I inspected representative samples from different line-length ranges.
5. This revealed that short lines were not necessarily garbage. They contained headings, metadata, chapter names, and other legitimate book content.
6. I also discovered that the PDF extraction preserved visual formatting through leading spaces.
7. I checked repeated lines, character frequencies, non-ASCII characters, whitespace, suspicious characters, number-like lines, and samples from the beginning, middle, and end of the corpus.
8. The profiling revealed several extraction artifacts:
   - U+00AD SOFT HYPHEN: 2,462 occurrences
   - U+000C FORM FEED: 1,676 occurrences
9. The corpus also contained legitimate Unicode characters such as `×`, `·`, `±`, etc., so Unicode characters cannot simply be treated as garbage.
10. The extracted text also contained different structural regions such as front matter, main book content, exercises, figures, and the index.

Phase 1: Cleaning and normalization

1. I created a separate cleaning pipeline instead of modifying `corpus_raw.txt`.
2. The raw corpus is kept unchanged so that the cleaning process can always be reproduced.
3. The first cleaning pass:
   - removed soft-hyphen extraction artifacts
   - converted form-feed page boundaries into newlines
   - removed leading/trailing whitespace
   - collapsed repeated spaces
   - repaired words broken across PDF line breaks
   - limited excessive consecutive blank lines
4. The result was written to `data/corpus_clean.txt`.
5. I profiled the cleaned corpus again to verify the effect of the cleaning process.

Cleaned corpus:

- Characters: 2,525,115
- Lines: 67,754
- Empty lines: 22,596
- Whitespace-separated words: 446,163
- Shortest line: 0 characters
- Longest line: 252 characters
- Leading spaces: 0
- Trailing spaces: 0
- Multiple-space runs: 0
- Soft hyphens: 0
- Form feeds: 0

6. I decided to remove the front matter from the corpus.
7. The front matter includes:
   - title/publication information
   - copyright information
   - author/publisher metadata
   - table of contents
   - preface
8. I removed these sections because they provide little useful training signal for an LLM whose target domain is algorithms.
9. I kept chapter headings and chapter-level introductions because they provide useful semantic structure for the technical content.
10. I will preserve the main chapters, algorithms, pseudocode, exercises, and references.

Phase 1.1: Semantic corpus

1. After cleaning and removing the unwanted front matter, I created a semantic-clean version of the corpus.
2. The resulting corpus was written to:
   - `data/corpus_semantic_clean.txt`
3. This file became the source corpus for structural section detection and later tokenization.

Phase 1.2: Section boundary detection

1. I needed reliable section boundaries before tokenization so that the corpus could be represented as meaningful training units rather than one undifferentiated text stream.
2. I first extracted the section structure from the Table of Contents.
3. The TOC contained 135 sections.
4. Section identifiers followed the pattern:
   - `1.1`
   - `1.2`
   - `2.1`
   - ...
   - `35.5`
5. I then searched the body of `corpus_semantic_clean.txt` for lines matching these section-number patterns.
6. A simple section-number match produced 152 body candidates.
7. The problem was that mathematical explanations and figure text could also begin with strings such as `3.1`, `4.2`, etc.
8. Therefore, section numbers alone were not sufficient to identify true section boundaries.
9. I used the TOC title as an additional signal.
10. For each body candidate, I compared its detected title against the corresponding TOC title using string similarity.
11. Candidates with sufficiently strong title similarity were accepted as actual section headings.
12. This reduced:
   - Body candidates: 152
   - Valid body sections: 135
13. The 17 rejected candidates were false positives caused by section-like text appearing inside the actual body content.
14. The final result produced exactly 135 valid section boundaries, matching the 135 TOC sections.
15. The boundaries were saved to:
   - `data/section_boundaries.txt`
16. Each boundary records:
   - section number
   - section title
   - starting line
   - ending line

Phase 1.3: Section extraction

1. Using the validated section boundaries, I split the semantic corpus into individual sections.
2. Each section was saved as its own `.txt` file.
3. The sections were written to:
   - `data/sections/`
4. The directory contains exactly 135 section files.
5. This gives the project a clean structural representation of the book:

   PDF
   ↓
   raw corpus
   ↓
   cleaned corpus
   ↓
   semantic corpus
   ↓
   135 sections

6. This structure will allow tokenization, dataset construction, debugging, and later evaluation to operate at the section level.

Phase 2: Tokenization

1. I decided to build a tokenizer rather than directly feeding raw text into the model.
2. I chose Byte Pair Encoding (BPE) because it provides subword-level tokenization and can represent words through reusable learned subword units.
3. I initially considered using an existing tokenizer, but decided to implement the BPE training and tokenization pipeline myself as part of the project.
4. The tokenizer was trained on the 135 extracted sections.
5. The initial vocabulary was constructed from individual characters.
6. Initial vocabulary size:
   - 115
7. The BPE trainer repeatedly:
   - counted adjacent symbol pairs
   - selected the most frequent pair
   - merged that pair
   - added the resulting token to the vocabulary
8. The target vocabulary size was:
   - 8,192 learned tokens
9. Training completed with:
   - Vocabulary: 8,192
   - Learned merges: 8,077
10. The learned BPE vocabulary and merges were saved so that the tokenizer can be reconstructed without retraining.
11. The tokenizer implementation reserves four additional special tokens:
   - `<PAD>` = 0
   - `<UNK>` = 1
   - `<BOS>` = 2
   - `<EOS>` = 3
12. Therefore, the final tokenizer ID space contains:
   - 8,192 learned BPE tokens
   - 4 special tokens
   - 8,196 total token IDs
13. The tokenizer was serialized to:
   - `data/tokenizer.json`

Phase 2.1: Tokenizer validation

1. Before encoding the entire corpus, I tested the tokenizer independently.
2. I tested the following round trip:

   text
   ↓
   encode
   ↓
   token IDs
   ↓
   decode
   ↓
   text

3. Test input:

   `Algorithms are fundamental to computer science.`

4. The tokenizer produced:
   - Vocabulary size: 8,196
   - Merges: 8,077
   - Token count including BOS/EOS: 14
5. The decoded output was:

   `Algorithms are fundamental to computer science.`

6. The successful round-trip confirmed that the tokenizer can:
   - load its vocabulary
   - apply its learned merges
   - convert text into integer token IDs
   - reconstruct the original text
   - correctly handle special BOS/EOS tokens
7. Tokenizer construction and validation are therefore complete.

Current project state:

PDF
 ↓
Text extraction                         ✓
 ↓
Corpus profiling                        ✓
 ↓
Cleaning                                ✓
 ↓
Semantic corpus                         ✓
 ↓
TOC extraction                          ✓
 ↓
Section boundary detection              ✓
 ↓
135 section extraction                  ✓
 ↓
BPE training                            ✓
 ↓
Tokenizer serialization                 ✓
 ↓
Tokenizer encode/decode validation      ✓
 ↓
Corpus tokenization                     ← NEXT
 ↓
Training sequence construction
 ↓
Transformer
 ↓
LLM