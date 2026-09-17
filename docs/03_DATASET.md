# Dataset Construction

## Objective

The objective of the dataset pipeline is to transform tokenized documents into supervised training examples suitable for autoregressive language modeling.

A Transformer cannot train directly on raw token sequences.

Instead, the corpus must be converted into input-target pairs that teach the model to predict the next token.

---

# Why Dataset Construction?

After tokenization, each section of the CLRS corpus is represented as a sequence of token IDs.

Example

```text
[BOS, 15, 83, 421, 912, 74, EOS]
```

Although this sequence contains all the information from the original document, it is not directly suitable for training.

The Transformer learns by predicting the next token given all previous tokens.

Therefore, the sequence must be converted into many supervised training examples.

---

# Pipeline

```text
Section Text
        ↓
BPE Tokenizer
        ↓
Token IDs
        ↓
Sliding Context Window
        ↓
Input Sequence
        ↓
Target Sequence
        ↓
NumPy Arrays
```

---

# Tokenized Documents

Every extracted section is independently tokenized.

Pipeline

```text
Section
    ↓
Tokenizer
    ↓
Token IDs
```

Each document automatically receives

```text
<BOS>

content

<EOS>
```

This preserves document boundaries throughout preprocessing.

---

# Sliding Context Window

The Transformer has a fixed context length.

For CLRS-LLM

```text
Context Length = 128
```

Rather than feeding an entire document to the model, a sliding window is moved across the token sequence.

---

# Example

Suppose the token sequence is

```text
[BOS A B C D E EOS]
```

and the context length is

```text
4
```

The dataset generator produces

Example 1

```text
Input

[BOS A B C]

Target

[A B C D]
```

Example 2

```text
Input

[A B C D]

Target

[B C D E]
```

Example 3

```text
Input

[B C D E]

Target

[C D E EOS]
```

This process continues until every valid context window has been generated.

---

# Why Shift By One Token?

The model is trained using autoregressive next-token prediction.

Conceptually,

```text
Given

[BOS A B C]

predict

D
```

The target sequence is therefore simply the input sequence shifted one position to the left.

---

# Training Arrays

Instead of storing thousands of JSON training examples, the generated dataset is stored as NumPy arrays.

Output

```text
data/training/

inputs.npy

targets.npy

metadata.json
```

This representation is

- compact,
- efficient,
- directly compatible with PyTorch,
- faster to load during training.

---

# Metadata

The dataset also stores metadata describing how it was generated.

Example

```json
{
    "context_length": 128,
    "num_examples": "...",
    "vocab_size": 8196,
    "dtype": "int32"
}
```

Metadata ensures that the training pipeline can reproduce the dataset configuration.

---

# Validation

The dataset pipeline was validated by checking

- BOS/EOS placement,
- sequence lengths,
- vocabulary bounds,
- token counts,
- dataset statistics,
- successful generation of NumPy arrays.

---

# Engineering Decisions

## Preserve document boundaries

Sections were tokenized independently.

Document boundaries were not crossed during sequence generation.

---

## Fixed context length

A constant context length simplifies batching and training.

---

## NumPy storage

NumPy arrays were chosen over JSON because they provide efficient storage and direct compatibility with PyTorch tensors.

---

## Separate preprocessing stages

The dataset generator consumes the output of the tokenizer instead of re-tokenizing text.

This keeps the pipeline modular and reproducible.

---

# Lessons Learned

Building the dataset pipeline demonstrated that preparing training data is one of the most important parts of language-model engineering.

Although the Transformer ultimately learns from tensors, the quality and structure of those tensors are determined entirely by preprocessing.

The dataset is therefore the bridge between natural language and neural network optimization.

---

# Production Notes

Large language models typically use more sophisticated dataset pipelines.

Common improvements include

- memory-mapped datasets,
- streaming datasets,
- distributed sharding,
- packed sequences,
- dynamic batching,
- multi-worker data loading.

Despite these engineering optimizations, the underlying learning objective remains identical:

```text
Input Tokens

↓

Predict Next Token
```