# CLRS-LLM

A decoder-only GPT-style language model built from scratch using PyTorch.

CLRS-LLM is an educational engineering project whose objective is to implement every major component of a modern language model rather than relying on high-level frameworks. The project covers the complete pipeline from raw PDF extraction to autoregressive text generation.

---

# Objective

The goal of this project is to understand how modern decoder-only language models are engineered by implementing each stage independently.

Rather than using pre-built Transformer implementations, CLRS-LLM implements the complete architecture using PyTorch primitives while documenting the engineering decisions made throughout development.

---

# End-to-End Pipeline

```text
CLRS PDF
      │
      ▼
Text Extraction
      │
      ▼
Corpus Profiling
      │
      ▼
Corpus Cleaning
      │
      ▼
Semantic Structuring
      │
      ▼
Section Extraction
      │
      ▼
Custom BPE Tokenizer
      │
      ▼
Dataset Tokenization
      │
      ▼
Training Sequence Construction
      │
      ▼
Transformer
      │
      ▼
Training
      │
      ▼
Autoregressive Text Generation
```

---

# Current Status

## Data Engineering

- ✅ PDF Extraction
- ✅ Corpus Profiling
- ✅ Corpus Cleaning
- ✅ Semantic Structuring
- ✅ Section Extraction
- ✅ Custom BPE Tokenizer
- ✅ Vocabulary Construction
- ✅ Dataset Tokenization
- ✅ Training Sequence Construction

## Transformer

- ✅ Model Configuration
- ✅ Token Embeddings
- ✅ Positional Embeddings
- ✅ GPT-style Multi-Head Self-Attention
- ✅ Feed Forward Network
- ✅ Transformer Block
- ✅ Decoder-only Transformer Architecture

## Remaining

- 🚧 Training Pipeline
- ⏳ Checkpointing
- ⏳ Text Generation
- ⏳ Evaluation

---

# Project Structure

```text
clrs-llm/

├── data/
│   ├── sections/
│   ├── tokenized/
│   └── training/
│
├── docs/
│
├── scripts/
│
└── src/
    ├── preprocessing/
    ├── tokenization/
    ├── dataset/
    ├── model/
    ├── training/
    └── inference/
```

---

# Transformer Architecture

```text
Token IDs
      │
      ▼
Token Embedding
      │
      ▼
Positional Embedding
      │
      ▼
Transformer Block × N
      │
      ├── LayerNorm
      ├── Multi-Head Self-Attention
      ├── Residual Connection
      ├── LayerNorm
      ├── Feed Forward Network
      └── Residual Connection
      │
      ▼
Final LayerNorm
      │
      ▼
Language Modeling Head
      │
      ▼
Vocabulary Logits
```

---

# Technologies

- Python
- PyTorch
- NumPy
- Custom Byte Pair Encoding (BPE)
- Git

---

# Documentation

The repository contains a complete engineering handbook describing every stage of development.

```text
docs/

00_PROJECT_OVERVIEW.md
01_DATA_PIPELINE.md
02_TOKENIZER.md
03_DATASET.md
04_TRANSFORMER.md
05_TRAINING.md
06_INFERENCE.md
07_LEARNINGS.md
```

Each document explains

- the engineering problem,
- implementation approach,
- design decisions,
- validation,
- lessons learned,
- and production considerations.

---

# Design Philosophy

CLRS-LLM is built incrementally.

Every stage is

- modular,
- independently testable,
- reproducible,
- and validated before introducing additional complexity.

The project deliberately favors engineering understanding over abstraction.

PyTorch primitives such as

- `nn.Linear`
- `nn.Embedding`
- `nn.LayerNorm`
- Autograd

are reused.

The Transformer architecture itself—including attention, dataset construction, training pipeline, and inference—is implemented manually.

---

# Roadmap

## Completed

- [x] Data Engineering Pipeline
- [x] Custom BPE Tokenizer
- [x] Dataset Construction
- [x] GPT-style Transformer Architecture

## In Progress

- [ ] Training Pipeline

## Planned

- [ ] Autoregressive Text Generation
- [ ] Model Evaluation
- [ ] Training Optimization
- [ ] Production Improvements

---

# Why This Project?

Many projects demonstrate how to *use* modern language models.

CLRS-LLM focuses on understanding how they are built.

The objective is not to reproduce the scale of production systems such as GPT or Llama, but to engineer every major component—from raw document preprocessing to Transformer architecture—in order to understand the complete lifecycle of a language model.

---

# License

This project is intended for educational and research purposes.