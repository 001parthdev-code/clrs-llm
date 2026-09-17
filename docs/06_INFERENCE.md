# Inference

## Objective

The objective of inference is to generate new text using a trained language model.

Unlike training, inference does not update the model parameters.

Instead, the Transformer repeatedly predicts the next token and appends it to the existing sequence until a stopping condition is reached.

---

# Difference Between Training and Inference

Training

```text
Input
    ↓
Prediction
    ↓
Loss
    ↓
Backpropagation
    ↓
Parameter Update
```

Inference

```text
Prompt
    ↓
Prediction
    ↓
Next Token
    ↓
Append
    ↓
Repeat
```

During inference, gradients are disabled and the model parameters remain fixed.

---

# Inference Pipeline

```text
User Prompt
        ↓
Tokenizer
        ↓
Token IDs
        ↓
Transformer
        ↓
Vocabulary Logits
        ↓
Sampling
        ↓
Next Token
        ↓
Append
        ↓
Repeat
        ↓
Generated Text
```

---

# Step 1 — Prompt

Generation begins with an input prompt.

Example

```text
Insertion sort
```

The prompt provides the initial context for the language model.

---

# Step 2 — Tokenization

The prompt is converted into token IDs using the custom BPE tokenizer.

```text
Prompt
    ↓
Tokenizer
    ↓
Token IDs
```

Example

```text
Insertion sort

↓

[2, 145, 83]
```

The BOS token marks the beginning of the sequence.

---

# Step 3 — Transformer Forward Pass

The token IDs are passed through the Transformer.

Pipeline

```text
Token IDs
        ↓
Embeddings
        ↓
Transformer Blocks
        ↓
Vocabulary Logits
```

The output is a tensor of shape

```text
(batch_size,
 sequence_length,
 vocabulary_size)
```

The final position contains the prediction for the next token.

---

# Step 4 — Vocabulary Logits

The Transformer outputs logits rather than probabilities.

Example

```text
[-1.42,
 0.18,
 4.91,
 ...
 2.77]
```

Each value corresponds to one vocabulary token.

Larger values indicate greater confidence.

---

# Step 5 — Sampling

The logits are converted into probabilities.

```text
Logits
    ↓
Softmax
    ↓
Probability Distribution
```

The next token is selected using a sampling strategy.

Possible strategies include

- Greedy decoding
- Temperature sampling
- Top-k sampling
- Top-p sampling

The first implementation of CLRS-LLM uses greedy decoding.

---

# Step 6 — Append

The predicted token is appended to the existing sequence.

Example

```text
Current

[BOS A B C]

↓

Predict

D

↓

New Sequence

[BOS A B C D]
```

---

# Step 7 — Repeat

The updated sequence is passed through the Transformer again.

```text
Sequence
    ↓
Transformer
    ↓
Next Token
    ↓
Append
    ↓
Repeat
```

This loop continues until

- an EOS token is generated,
- or the maximum generation length is reached.

---

# Greedy Decoding

Greedy decoding selects the token with the highest probability.

Example

```text
Probability

Token A : 0.72

Token B : 0.12

Token C : 0.05
```

Greedy decoding chooses

```text
Token A
```

It is simple but may produce repetitive text.

---

# Temperature Sampling

Temperature modifies the probability distribution before sampling.

Lower temperatures

```text
↓

More deterministic
```

Higher temperatures

```text
↓

More creative
```

Temperature does not change the model.

It only changes the sampling strategy.

---

# Top-k Sampling

Rather than considering the entire vocabulary, only the top-k most probable tokens are retained.

Example

```text
Vocabulary

8196 tokens

↓

Top 50

↓

Sample
```

This reduces unlikely predictions.

---

# Top-p Sampling

Top-p sampling dynamically selects the smallest set of tokens whose cumulative probability exceeds a threshold.

Unlike Top-k, the number of candidate tokens changes depending on the probability distribution.

---

# End of Generation

Generation stops when

- an EOS token is produced,
- the maximum sequence length is reached,
- or the maximum number of generated tokens is exceeded.

The resulting token IDs are decoded back into text using the tokenizer.

```text
Token IDs
        ↓
Tokenizer
        ↓
Generated Text
```

---

# Engineering Decisions

- Separate training and inference pipelines.
- Disable gradient computation during inference.
- Use autoregressive generation.
- Begin with greedy decoding before implementing more advanced sampling methods.

---

# Lessons Learned

Training teaches the model statistical relationships between tokens.

Inference uses those learned relationships to generate entirely new text.

The Transformer never generates full sentences at once.

Instead, it repeatedly predicts a single token, appends it to the context, and repeats the process until generation is complete.

Every response produced by a GPT-style language model is generated one token at a time.

---

# Production Notes

Modern language models extend this basic inference loop with additional optimizations.

Examples include

- KV Cache
- Flash Attention
- Speculative Decoding
- Continuous Batching
- Beam Search
- Streaming Token Generation

These optimizations improve efficiency but do not change the fundamental autoregressive generation process.