# CLRS-LLM

> **Educational Engineering Project**
>
> CLRS-LLM is a decoder-only GPT-style language model built entirely from scratch using PyTorch. The objective of this project is to understand and implement every major engineering component of a modern language model rather than relying on high-level frameworks.

---

# Overview

Modern language models are significantly more than neural networks.

CLRS-LLM was built to understand the complete engineering pipeline behind GPT-style models, beginning with raw PDF extraction and ending with autoregressive text generation.

Instead of using existing Transformer implementations, every major stage of the pipeline was implemented and validated independently.

---

# End-to-End Pipeline

```text
Introduction to Algorithms (CLRS)
                │
                ▼
        PDF Extraction
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
Training Sequence Generation
                │
                ▼
 GPT-style Transformer
                │
                ▼
      GPU Training
                │
                ▼
 Autoregressive Inference
```

---

# Features

## Data Engineering

- PDF extraction
- Corpus profiling
- Corpus cleaning
- Semantic corpus preparation
- Section boundary detection
- Section extraction

## Tokenization

- Custom Byte Pair Encoding (BPE)
- Vocabulary construction
- Token encoding / decoding
- JSON tokenizer serialization

## Dataset

- Sliding context window generation
- Input / target sequence construction
- NumPy training datasets
- PyTorch dataset integration

## Transformer

- Decoder-only architecture
- GPT-style Multi-Head Self-Attention
- Feed Forward Network
- Residual Connections
- Layer Normalization
- Weight Tying

## Training

- GPU training (CUDA)
- AdamW optimizer
- Cross Entropy Loss
- Automatic checkpointing
- Model persistence

## Inference

- Prompt encoding
- Autoregressive generation
- Greedy decoding
- Interactive inference

---

# Model Statistics

| Metric | Value |
|---------|------:|
| Parameters | **1,858,816** |
| Transformer Blocks | **4** |
| Attention Heads | **4** |
| Embedding Dimension | **128** |
| Vocabulary Size | **8,196** |
| Context Length | **128** |
| Model Size | **7.15 MB** |

---

# Training Results

## Hardware

- NVIDIA RTX 4060
- CUDA

## Training Configuration

| Metric | Value |
|---------|------:|
| Optimizer | AdamW |
| Epochs | 10 |
| Batch Size | 16 |
| Learning Rate | 3e-4 |

## Training Loss

| Epoch | Loss |
|------:|-----:|
| 1 | 3.1056 |
| 2 | 1.9902 |
| 3 | 1.6474 |
| 4 | 1.4612 |
| 5 | 1.3412 |
| 6 | 1.2586 |
| 7 | 1.1995 |
| 8 | 1.1558 |
| 9 | 1.1229 |
| 10 | **1.0971** |

Training converged successfully without numerical instability or divergence.

---

# Example Generation

### Prompt

```text
Insertion sort
```

### Output

```text
Insertion sort is a heap...
The heap data structure...
Priority queue...
```

Although semantic coherence is still limited, the model successfully reproduces the vocabulary, formatting, and writing style of the CLRS corpus.

Additional examples are available in the `examples/` directory.

---

# Repository Structure

```text
clrs-llm/

├── data/
├── docs/
├── examples/
├── models/
├── checkpoints/
├── results/
├── scripts/
└── src/
```

---

# Documentation

Detailed engineering documentation is available in the `docs/` directory.

- Project Overview
- Data Pipeline
- Tokenizer
- Dataset Construction
- Transformer Architecture
- Training
- Inference
- Engineering Learnings

The documentation explains not only *how* each component was implemented, but also *why* specific engineering decisions were made.

---

# Design Philosophy

CLRS-LLM prioritizes engineering understanding over abstraction.

Instead of treating modern language models as black boxes, every major stage of the pipeline was implemented independently using PyTorch primitives.

The goal is not to compete with production-scale models such as GPT or Llama.

The goal is to understand the engineering principles behind them.

---

# Roadmap

## Version 1.0

- [x] Data Engineering Pipeline
- [x] Custom BPE Tokenizer
- [x] Dataset Construction
- [x] GPT-style Transformer
- [x] GPU Training
- [x] Autoregressive Inference

## Planned Improvements

- [ ] Rotary Position Embeddings (RoPE)
- [ ] Flash Attention
- [ ] Temperature Sampling
- [ ] Top-k / Top-p Sampling
- [ ] Validation Pipeline
- [ ] Perplexity Evaluation
- [ ] Larger Training Corpus
- [ ] Mixed Precision Training
- [ ] KV Cache

---

# License

MIT License

---

# Acknowledgements

This project was developed as an educational engineering exercise to understand the complete implementation pipeline behind modern decoder-only language models.