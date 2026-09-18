# CLRS-LLM Model Card

## Overview

CLRS-LLM is a decoder-only GPT-style language model implemented from scratch using PyTorch.

The project was developed as an educational engineering exercise to understand every major component involved in building modern decoder-only language models. Rather than relying on high-level Transformer libraries, the complete pipeline—from raw PDF preprocessing to autoregressive text generation—was implemented and validated incrementally.

The model is trained exclusively on the technical content of *Introduction to Algorithms* (CLRS).

---

# Model Details

| Property | Value |
|----------|------:|
| Model Name | CLRS-LLM |
| Version | v1.0.0 |
| Architecture | Decoder-only Transformer |
| Framework | PyTorch |
| Parameters | 1,858,816 |
| Transformer Blocks | 4 |
| Attention Heads | 4 |
| Embedding Dimension | 128 |
| Context Length | 128 |
| Vocabulary Size | 8,196 |
| Model Size | 7.15 MB |

---

# Dataset

The training corpus was constructed from the textbook:

> *Introduction to Algorithms (CLRS)*

The preprocessing pipeline included:

- PDF extraction
- Corpus profiling
- Corpus cleaning
- Semantic corpus preparation
- Section boundary detection
- Section extraction
- Custom Byte Pair Encoding (BPE)
- Sliding-window dataset generation

Dataset statistics:

| Metric | Value |
|----------|------:|
| Semantic Sections | 135 |
| Vocabulary Size | 8,196 |
| BPE Merge Rules | 8,077 |

---

# Training

## Hardware

- NVIDIA RTX 4060
- CUDA

## Optimizer

AdamW

## Loss Function

Cross Entropy Loss

## Epochs

10

## Final Training Loss

1.0971

---

# Capabilities

The model is capable of

- autoregressive text generation,
- completing prompts related to algorithms,
- reproducing the writing style of the CLRS textbook,
- generating domain-specific terminology.

Example domains include

- sorting algorithms,
- graph algorithms,
- dynamic programming,
- data structures,
- asymptotic analysis.

---

# Limitations

CLRS-LLM is intentionally a compact educational model.

Current limitations include:

- trained on a single textbook,
- relatively small parameter count,
- greedy decoding only,
- limited semantic coherence over long generations,
- no validation set or perplexity evaluation in Version 1,
- not intended as a general-purpose conversational model.

---

# Intended Use

CLRS-LLM is intended for

- educational purposes,
- understanding Transformer internals,
- studying tokenizer implementation,
- experimenting with language-model architectures,
- learning end-to-end LLM engineering.

It is **not** intended to replace production language models.

---

# Engineering Highlights

Major components implemented from scratch include:

- corpus preprocessing,
- semantic document extraction,
- custom Byte Pair Encoding tokenizer,
- dataset generation,
- GPT-style decoder-only Transformer,
- multi-head causal self-attention,
- GPU training pipeline,
- autoregressive inference.

The project deliberately prioritizes engineering understanding over using high-level frameworks.

---

# Future Work

Planned improvements include:

- Rotary Position Embeddings (RoPE)
- Flash Attention
- Temperature Sampling
- Top-k Sampling
- Top-p Sampling
- Validation Pipeline
- Perplexity Evaluation
- Larger Training Corpus
- Mixed Precision Training
- KV Cache
- Learning Rate Scheduling

---

# Ethical Considerations

CLRS-LLM was developed as an educational engineering project.

The model was trained exclusively on algorithmic and technical material from a single textbook and is not designed for deployment as a general-purpose language model.

Its primary purpose is to demonstrate the engineering pipeline behind modern decoder-only Transformers.

---

# Citation

If you reference this project, please cite the GitHub repository corresponding to the released version.
