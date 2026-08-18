# CLRS-LLM

A from-scratch language model trained on *Introduction to Algorithms (CLRS)*.

The goal of this project is not simply to train an LLM, but to understand and implement the complete pipeline involved in building one:

```text
PDF
 ↓
Text Extraction
 ↓
Corpus Cleaning
 ↓
Semantic Structuring
 ↓
Section Boundaries
 ↓
Tokenization
 ↓
Token IDs
 ↓
Training Sequences
 ↓
LLM
````

The project is being built incrementally, with each stage implemented and validated before moving to the next.

---

# Project Status

Current stage:

**Tokenization complete.**

Completed:

* PDF extraction
* Corpus profiling
* Corpus cleaning
* Semantic corpus preparation
* Table-of-contents extraction
* Section boundary detection
* Section extraction
* Custom BPE tokenizer training
* Vocabulary construction
* Token encoding / decoding

Next:

* Dataset construction
* Training sequence generation
* Model architecture
* Training
* Evaluation

---

# Phase 0 — Data Extraction

The first objective was to convert the CLRS PDF into machine-readable text.

## PDF → Text

I used Poppler's `pdftotext` utility to extract the text.

The first PDF was corrupted and produced `xref` / `trailer` errors during extraction, so it was replaced with a clean copy.

The extracted corpus was stored as:

```text
data/corpus_raw.txt
```

Initial corpus statistics:

* Characters: `2,600,328`
* Lines: `68,590`
* Empty lines: `23,047`
* Whitespace-separated words: `447,292`
* Shortest line: `0`
* Longest line: `109`

The raw corpus is preserved and is never modified directly.

---

# Phase 0.1 — Corpus Profiling

Before cleaning the corpus, I profiled the extracted text to understand its structure and identify extraction artifacts.

The analysis included:

* line-length distribution
* representative samples from different line-length ranges
* repeated lines
* character frequencies
* non-ASCII characters
* whitespace patterns
* suspicious characters
* number-like lines
* samples from the beginning, middle, and end of the corpus

An important observation was that short lines were not necessarily garbage.

They contained legitimate structural information such as:

* headings
* chapter names
* metadata
* section titles
* other book structure

The PDF extraction also preserved some visual formatting through leading spaces.

## Extraction artifacts

Two major extraction artifacts were identified:

```text
U+00AD SOFT HYPHEN   → 2,462 occurrences
U+000C FORM FEED     → 1,676 occurrences
```

However, the corpus also contained legitimate Unicode characters such as:

```text
×
·
±
```

Therefore, Unicode characters could not simply be removed indiscriminately.

The profiling stage also revealed that the corpus contained several structural regions:

* front matter
* main book content
* exercises
* figures
* index

---

# Phase 1 — Cleaning and Normalization

A separate cleaning pipeline was created instead of modifying the raw corpus.

This allows the entire cleaning process to be reproduced from the original extracted text.

```text
corpus_raw.txt
       ↓
   cleaning
       ↓
corpus_clean.txt
```

Output:

```text
data/corpus_clean.txt
```

## Cleaning operations

The first cleaning pass:

* removed soft-hyphen extraction artifacts
* converted form-feed page boundaries into newlines
* removed leading and trailing whitespace
* collapsed repeated spaces
* repaired words broken across PDF line breaks
* limited excessive consecutive blank lines

## Cleaned corpus statistics

After cleaning:

* Characters: `2,525,115`
* Lines: `67,754`
* Empty lines: `22,596`
* Whitespace-separated words: `446,163`
* Shortest line: `0`
* Longest line: `252`
* Leading spaces: `0`
* Trailing spaces: `0`
* Multiple-space runs: `0`
* Soft hyphens: `0`
* Form feeds: `0`

---

# Phase 1.1 — Semantic Corpus Preparation

After cleaning, the next step was to remove material that was not useful for the target training domain.

The front matter was removed.

This included:

* title/publication information
* copyright information
* author/publisher metadata
* table of contents
* preface

The goal was to focus the training corpus on the actual algorithms content.

However, useful structural information was preserved.

The corpus retains:

* chapter headings
* chapter-level introductions
* algorithms
* pseudocode
* exercises
* references

This creates a cleaner domain-specific corpus while preserving the semantic structure of the book.

---

# Phase 2 — Table of Contents and Section Structure

A major problem with raw PDF text extraction is that the document's visual structure is partially lost.

Instead of relying only on text patterns, the table of contents was used as an authoritative source for identifying section boundaries.

The extracted TOC contains:

```text
135 sections
```

Example:

```text
1.1 | Algorithms
1.2 | Algorithms as a technology
2.1 | Insertion sort
2.2 | Analyzing algorithms
2.3 | Designing algorithms
...
```

The TOC was stored separately:

```text
data/toc_sections.txt
```

---

# Phase 2.1 — Section Boundary Detection

The body corpus was searched for section-like headings.

A simple section-number match produced false positives because normal prose can contain patterns such as:

```text
3.1 ...
4.2 ...
9.1 ...
```

Therefore, section numbers alone were not considered sufficient.

The section detector compares the candidate body heading against the corresponding TOC title using normalized title similarity.

This produced:

```text
TOC sections:       135
Body candidates:    152
Valid body sections: 135
```

The additional candidates were rejected as false positives.

The final result:

```text
135 valid section boundaries
```

was saved to:

```text
data/section_boundaries.txt
```

Each boundary contains:

```text
section number
section title
start line
end line
```

This allows the corpus to be reconstructed as semantically meaningful sections instead of treating the entire book as one continuous text stream.

---

# Phase 2.2 — Section Extraction

Using the detected boundaries, each section was extracted into its own file.

Output:

```text
data/sections/
```

The result:

```text
135 section files
```

Each file corresponds to one section of the book.

Example structure:

```text
data/
├── corpus_raw.txt
├── corpus_clean.txt
├── corpus_semantic_clean.txt
├── toc_sections.txt
├── section_boundaries.txt
└── sections/
    ├── 1_1_Algorithms.txt
    ├── 1_2_Algorithms_as_a_technology.txt
    ├── 2_1_Insertion_sort.txt
    └── ...
```

This gives the later training pipeline access to explicit document boundaries.

---

# Phase 3 — Tokenization

With the corpus structurally prepared, tokenization was started as a separate module.

The tokenizer is implemented from scratch rather than relying on an existing tokenizer library.

The chosen approach is:

**Byte Pair Encoding (BPE)**

The tokenizer is implemented in:

```text
src/tokenization/
```

The tokenizer pipeline consists of:

```text
Section text
     ↓
Initial character vocabulary
     ↓
Word frequency counting
     ↓
Adjacent pair statistics
     ↓
Most frequent pair selection
     ↓
Pair merging
     ↓
Vocabulary expansion
     ↓
BPE vocabulary
```

---

# Phase 3.1 — BPE Training

The initial vocabulary was constructed from characters appearing in the corpus.

The BPE trainer then repeatedly:

1. counts adjacent symbol pairs
2. finds the most frequent pair
3. merges the pair
4. adds the merged token to the vocabulary
5. records the merge rule

The target vocabulary size was:

```text
8192
```

The tokenizer learned:

```text
Vocabulary size: 8196
Merges: 8077
```

The vocabulary is slightly larger than the requested 8192 because special tokens are reserved separately.

---

# Phase 3.2 — Token IDs

The learned vocabulary was converted into integer token IDs.

Special tokens were reserved:

```text
<PAD> → 0
<UNK> → 1
<BOS> → 2
<EOS> → 3
```

The tokenizer can now perform:

```text
Text
 ↓
BPE tokens
 ↓
Integer token IDs
```

Example:

```text
Original:

Algorithms are fundamental to computer science.
```

produced:

```text
Token IDs:

[2, 918, 5, 2907, 5, 4531, 5, 7515, 5, 3544, 5, 6868, 372, 3]
```

Token count:

```text
14
```

The tokenizer was also tested by decoding the generated token IDs:

```text
Algorithms are fundamental to computer science.
```

The decoded output matched the original text.

This confirms that the current tokenizer can perform the basic:

```text
encode → decode
```

round trip.

---

# Current Architecture

The project is currently organized roughly as:

```text
clrs-llm/
│
├── data/
│   ├── corpus_raw.txt
│   ├── corpus_clean.txt
│   ├── corpus_semantic_clean.txt
│   ├── toc_sections.txt
│   ├── section_boundaries.txt
│   └── sections/
│
├── src/
│   ├── preprocessing/
│   │   ├── ...
│   │   ├── section_boundaries.py
│   │   └── extract_section.py
│   │
│   └── tokenization/
│       ├── corpus.py
│       ├── bpe.py
│       └── tokenizer.py
│
└── README.md
```

The exact structure may evolve as the model-training pipeline is implemented.

---

# Design Philosophy

This project is being built from the bottom up.

Instead of jumping directly to model training, each stage of the LLM pipeline is implemented and validated independently.

The current philosophy is:

```text
Understand the data
        ↓
Understand the representation
        ↓
Build the tokenizer
        ↓
Build the dataset
        ↓
Build the model
        ↓
Train
        ↓
Evaluate
```

The purpose is not to produce the largest possible model.

The purpose is to understand what actually happens underneath an LLM by implementing the complete pipeline.

---

# Roadmap

## Completed

* [x] PDF extraction
* [x] Raw corpus preservation
* [x] Corpus profiling
* [x] Corpus cleaning
* [x] Semantic corpus preparation
* [x] TOC extraction
* [x] Section boundary detection
* [x] Section extraction
* [x] Custom BPE trainer
* [x] Vocabulary construction
* [x] Token ID mapping
* [x] Encoding
* [x] Decoding

## Next

* [ ] Dataset construction
* [ ] Training sequence generation
* [ ] Context window handling
* [ ] Train/validation split
* [ ] Transformer architecture
* [ ] Attention implementation
* [ ] Positional embeddings
* [ ] Training loop
* [ ] Loss calculation
* [ ] Checkpointing
* [ ] Evaluation
* [ ] Text generation

---

# Goal

Build a working language model from the ground up while understanding every major transformation:

```text
Raw PDF
  ↓
Extracted text
  ↓
Clean corpus
  ↓
Semantic sections
  ↓
BPE tokens
  ↓
Token IDs
  ↓
Training sequences
  ↓
Transformer
  ↓
Learned parameters
  ↓
Generated text
```

This repository documents that process step by step.

```