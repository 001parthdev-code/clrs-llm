# Tokenizer

## Objective

The objective of the tokenizer is to convert human-readable text into numerical representations that can be processed by a Transformer language model.

Neural networks cannot directly operate on text. Instead, every piece of text must be represented as a sequence of integer token IDs.

The tokenizer acts as the bridge between natural language and the neural network.

---

# Why Tokenization?

Consider the sentence

```text
Algorithms are fundamental to computer science.
```

A Transformer cannot understand characters or words directly.

Instead, it expects an input similar to

```text
[918, 5, 2907, 5, 4531, 5, 7515, 5, 3544, 5, 6868, 372]
```

Each integer represents one token in the learned vocabulary.

---

# Why Byte Pair Encoding (BPE)?

Several tokenization algorithms exist:

- Character-level tokenization
- Word-level tokenization
- WordPiece
- SentencePiece
- Byte Pair Encoding (BPE)

CLRS-LLM uses Byte Pair Encoding because it provides a good balance between vocabulary size and sequence length while remaining relatively straightforward to implement.

Unlike word-level tokenization, BPE can represent words that were never seen during training by decomposing them into smaller subword units.

---

# Byte Pair Encoding

BPE begins with a vocabulary consisting of individual characters.

Example

```text
algorithm

↓

a l g o r i t h m
```

The algorithm repeatedly

1. counts adjacent symbol pairs,
2. finds the most frequent pair,
3. merges the pair,
4. adds the merged token to the vocabulary.

This process continues until the target vocabulary size is reached.

---

# Training Pipeline

```text
Corpus
    ↓
Character Vocabulary
    ↓
Word Frequency Counting
    ↓
Pair Frequency Counting
    ↓
Most Frequent Pair
    ↓
Merge
    ↓
Repeat
    ↓
Final Vocabulary
```

---

# Vocabulary

Target vocabulary size

```text
8192
```

Final vocabulary

```text
8196
```

The additional four entries correspond to reserved special tokens.

---

# Special Tokens

The tokenizer reserves four special tokens.

```text
<PAD> → 0

<UNK> → 1

<BOS> → 2

<EOS> → 3
```

## BOS

Marks the beginning of a document.

## EOS

Marks the end of a document.

## PAD

Used when sequences of different lengths must be padded to the same size.

## UNK

Represents unknown tokens that are not present in the vocabulary.

---

# Encoding

Encoding transforms text into integer token IDs.

Pipeline

```text
Text
    ↓
Subword Tokens
    ↓
Token IDs
```

Example

```text
Algorithms are fundamental to computer science.
```

↓

```text
[2, 918, 5, 2907, 5, 4531, 5, 7515, 5, 3544, 5, 6868, 372, 3]
```

---

# Decoding

The tokenizer also performs the inverse transformation.

Pipeline

```text
Token IDs
    ↓
Subword Tokens
    ↓
Text
```

Round-trip reconstruction was verified during implementation.

---

# Implementation

The tokenizer was implemented from scratch.

Major components include

- Vocabulary construction
- Merge-rule learning
- Vocabulary indexing
- Token encoding
- Token decoding
- Save/load functionality

No external tokenizer libraries were used during training.

---

# Engineering Decisions

## Preserve whitespace

Whitespace was tokenized rather than discarded in order to preserve the original document structure.

---

## Learned merge rules

Merge rules are learned once during tokenizer training and reused during encoding.

---

## Deterministic vocabulary

The vocabulary is generated deterministically, ensuring reproducible token IDs.

---

## JSON serialization

Tokenizer configuration is stored in

```text
data/tokenizer.json
```

allowing the tokenizer to be reconstructed without retraining.

---

# Validation

The tokenizer was validated by

- vocabulary size verification,
- encode/decode round-trip reconstruction,
- special token verification,
- corpus-wide tokenization.

---

# Lessons Learned

Implementing the tokenizer demonstrated that modern language models do not operate on words directly.

Instead, they learn statistical relationships between subword units.

The tokenizer is one of the most important components in the pipeline because every subsequent stage depends on its output.

Although tokenization appears simple at first glance, it fundamentally determines how the model represents language.

---

# Production Notes

Large production language models often use more advanced tokenization techniques and significantly larger vocabularies.

However, the core principle remains the same:

```text
Natural Language

↓

Discrete Tokens

↓

Integer IDs

↓

Neural Network
```

The tokenizer therefore serves as the interface between human language and machine learning.