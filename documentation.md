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