# CLRS-LLM

## Objective

CLRS-LLM is a decoder-only Transformer language model built from scratch for educational and engineering purposes.

The objective is not simply to train a language model, but to understand every major component involved in constructing one.

Instead of relying on high-level libraries that hide the implementation details, each stage of the pipeline is implemented and validated independently.

---

# End-to-End Pipeline

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
Custom BPE Tokenizer
    ↓
Dataset Tokenization
    ↓
Training Sequence Construction
    ↓
Transformer
    ↓
Training
    ↓
Inference
```

---

# Current Progress

## Data Pipeline

- ✅ PDF Extraction
- ✅ Corpus Profiling
- ✅ Corpus Cleaning
- ✅ Semantic Structuring
- ✅ Section Extraction
- ✅ Custom BPE Tokenizer
- ✅ Dataset Tokenization
- ✅ Training Sequence Construction

## Transformer

- ✅ Model Configuration
- ✅ Token Embeddings
- ✅ Positional Embeddings
- ✅ Multi-Head Self Attention
- ✅ Feed Forward Network
- ✅ Transformer Block
- ✅ GPT Model

## Remaining

- ⏳ Training Pipeline
- ⏳ Model Optimization
- ⏳ Text Generation

---

# Design Philosophy

Every module should satisfy four properties.

1. Understandable
2. Testable
3. Reproducible
4. Replaceable

The project prioritizes engineering understanding over minimizing lines of code.

PyTorch primitives such as Linear layers, LayerNorm, Embedding layers and automatic differentiation are reused.

The Transformer architecture itself is implemented manually.

---

# Repository Structure

```text
src/

preprocessing/

tokenization/

dataset/

model/

training/

inference/
```

---

# Learning Outcomes

This project covers

- Data engineering
- Tokenization
- Dataset construction
- Transformer architecture
- Multi-head attention
- Neural network training
- Autoregressive inference

The goal is to understand the complete engineering pipeline behind modern decoder-only language models.