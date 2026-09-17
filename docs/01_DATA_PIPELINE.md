# Data Pipeline

## Objective

The purpose of the data pipeline is to transform a textbook in PDF format into a machine-readable dataset that can be consumed by a Transformer language model.

The Transformer cannot read PDFs or raw text. Every stage in the pipeline progressively converts human-readable information into structured numerical representations.

---

# Complete Pipeline

```text
CLRS PDF
    ↓
Text Extraction
    ↓
Corpus Profiling
    ↓
Corpus Cleaning
    ↓
Semantic Structuring
    ↓
Section Extraction
    ↓
BPE Tokenization
    ↓
Token IDs
    ↓
Training Sequences
```

Each stage has a single responsibility and produces reproducible outputs.

---

# Stage 1 — PDF Extraction

## Objective

Extract machine-readable text from the CLRS PDF.

## Why?

Neural networks cannot directly process PDF documents. The content must first be converted into plain text.

## Output

```text
data/corpus_raw.txt
```

---

# Stage 2 — Corpus Profiling

## Objective

Understand the structure of the extracted corpus before modifying it.

## Analysis Performed

- Character counts
- Line counts
- Empty lines
- Unicode analysis
- Character frequency
- Suspicious characters
- Whitespace analysis
- Repeated lines
- Sample inspection

## Learning

Never clean data before understanding it.

Profiling revealed that not all Unicode characters were noise. Mathematical symbols were legitimate parts of the textbook and had to be preserved.

---

# Stage 3 — Corpus Cleaning

## Objective

Remove PDF extraction artifacts while preserving semantic information.

## Operations

- Remove soft hyphens
- Remove form-feed characters
- Trim whitespace
- Collapse repeated spaces
- Repair broken words
- Limit excessive blank lines

## Output

```text
data/corpus_clean.txt
```

## Learning

The raw corpus should never be modified directly.

Every transformation should be reproducible.

---

# Stage 4 — Semantic Structuring

## Objective

Remove non-semantic front matter while preserving educational content.

## Removed

- Copyright pages
- Publisher metadata
- Table of contents
- Preface

## Preserved

- Chapters
- Sections
- Algorithms
- Pseudocode
- Exercises

## Learning

Training quality depends more on data quality than data quantity.

---

# Stage 5 — Section Extraction

## Objective

Split the corpus into semantically meaningful documents.

## Why?

A Transformer learns better from structured documents than from one continuous stream of text.

## Output

```text
135 section files
```

## Learning

Document boundaries preserve semantic structure.

---

# Stage 6 — BPE Tokenization

## Objective

Convert text into subword tokens.

## Process

- Character vocabulary
- Word frequencies
- Pair frequencies
- Pair merging
- Vocabulary construction

Vocabulary

```text
8196 tokens
```

Special Tokens

```text
<PAD>
<UNK>
<BOS>
<EOS>
```

## Learning

Modern language models operate on subword units rather than full words.

---

# Stage 7 — Dataset Tokenization

## Objective

Convert every section into token IDs.

Pipeline

```text
Section
    ↓
Tokenizer
    ↓
Token IDs
```

Each document receives

```text
<BOS>

content

<EOS>
```

## Output

```text
data/tokenized/
```

## Learning

The Transformer never sees text.

It only sees integer token IDs.

---

# Stage 8 — Training Sequence Construction

## Objective

Generate supervised training examples.

Example

```text
Input

[BOS A B C]

Target

[A B C D]
```

This is repeated across the entire dataset using a sliding context window.

## Output

```text
inputs.npy

targets.npy
```

## Learning

Autoregressive language models learn by predicting the next token.

---

# Engineering Principles

During implementation the following principles were followed.

- Raw data is immutable.
- Every stage has one responsibility.
- Every stage is reproducible.
- Every stage is independently testable.
- Intermediate artifacts are preserved.

---

# Lessons Learned

Building the data pipeline revealed that a large portion of language-model engineering occurs before any neural network is constructed.

The quality of the dataset directly influences the quality of the trained model.

Most of the engineering effort was spent ensuring that every transformation was deterministic, reproducible, and semantically correct.