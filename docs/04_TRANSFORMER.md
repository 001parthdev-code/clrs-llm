# Transformer Architecture

## Objective

The objective of the Transformer is to learn the probability distribution of the next token given all previous tokens.

Unlike recurrent neural networks, the Transformer processes all tokens in a sequence simultaneously using self-attention.

The implementation in CLRS-LLM follows the decoder-only Transformer architecture introduced by GPT models.

---

# High-Level Architecture

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
Transformer Block
      │
      ▼
Transformer Block
      │
      ▼
Transformer Block
      │
      ▼
Transformer Block
      │
      ▼
Final Layer Normalization
      │
      ▼
Language Modeling Head
      │
      ▼
Vocabulary Logits
```

---

# Token Embedding

## Objective

Convert integer token IDs into dense vector representations.

## Why?

Token IDs are merely integer indices.

The model cannot learn useful relationships directly from integers.

Instead, every token is mapped to a trainable vector.

Example

```text
54

↓

[-0.17, 0.42, ..., 0.08]
```

## Implementation

PyTorch's `nn.Embedding` layer was used.

Vocabulary Size

```text
8196
```

Embedding Dimension

```text
128
```

The embedding matrix therefore has dimensions

```text
8196 × 128
```

## Learning

Embeddings are learned during training.

Initially they are random.

Over time, semantically similar tokens become nearby vectors.

---

# Positional Embedding

## Objective

Provide information about token order.

## Problem

Self-attention has no inherent notion of sequence order.

The sentences

```text
Dog bites man.

Man bites dog.
```

contain the same words but have different meanings.

Without positional information the Transformer cannot distinguish them.

## Solution

A trainable vector is assigned to every position.

The final representation becomes

```text
Token Embedding

+

Position Embedding

=

Transformer Input
```

## Learning

The Transformer understands order because position vectors are added to token vectors before attention is computed.

---

# Multi-Head Self-Attention

## Objective

Allow every token to gather information from previous tokens.

## Motivation

Traditional recurrent neural networks process tokens sequentially.

Transformers instead compare every token with every other token in parallel.

## Pipeline

```text
Input
    ↓
QKV Projection
    ↓
Split into Heads
    ↓
Scaled Dot Product
    ↓
Causal Mask
    ↓
Softmax
    ↓
Weighted Sum
    ↓
Merge Heads
    ↓
Output Projection
```

---

## Query

Represents what the current token is searching for.

## Key

Represents what every token offers.

## Value

Represents the information that should be aggregated.

---

## Scaled Dot Product

Attention scores are computed using

```text
Q × Kᵀ
```

These scores are divided by

```text
√head_dimension
```

to stabilize gradients.

---

## Causal Mask

Language models must not see future tokens.

The causal mask ensures that token *i* can only attend to tokens

```text
0 ... i
```

and never to future positions.

---

## Softmax

Converts raw attention scores into probabilities.

Every row sums to one.

---

## Output Projection

The outputs from all heads are concatenated and projected back into the embedding dimension.

---

# Feed Forward Network

## Objective

Process every token independently after attention.

Pipeline

```text
Linear
    ↓
GELU
    ↓
Linear
```

Unlike attention, the feed-forward network operates independently on each token.

## Learning

Attention determines **where to look**.

Feed Forward determines **what to compute**.

---

# Transformer Block

Each block consists of

```text
LayerNorm
    ↓
Attention
    ↓
Residual

LayerNorm
    ↓
Feed Forward
    ↓
Residual
```

Residual connections improve optimization.

Layer normalization stabilizes training.

---

# Decoder-Only Architecture

CLRS-LLM follows the decoder-only Transformer architecture used by GPT.

Unlike encoder-decoder models, only previous tokens are visible during prediction.

This is achieved using causal self-attention.

---

# Weight Tying

The embedding matrix is reused as the output projection matrix.

Benefits

- fewer parameters
- improved generalization
- standard practice in GPT-style models

---

# Tensor Shapes

Input

```text
(batch_size, sequence_length)
```

After Embedding

```text
(batch_size, sequence_length, embedding_dimension)
```

After Attention

```text
(batch_size, sequence_length, embedding_dimension)
```

After Feed Forward

```text
(batch_size, sequence_length, embedding_dimension)
```

Output

```text
(batch_size, sequence_length, vocabulary_size)
```

---

# Engineering Decisions

- Used PyTorch primitives instead of implementing tensors from scratch.
- Implemented the Transformer architecture manually.
- Used a single QKV projection instead of three independent projections.
- Stored the causal mask using `register_buffer`.
- Derived `head_dimension` automatically.
- Used GPT-style weight tying.

---

# Lessons Learned

Implementing the Transformer demonstrated that modern language models are built from a small number of carefully composed modules.

The apparent complexity of GPT-style models arises primarily from scale rather than architectural complexity.

Once embeddings, attention, feed-forward networks, residual connections and layer normalization are understood, the remaining work consists mainly of stacking these components repeatedly.