# Training

## Objective

The objective of training is to optimize the parameters of the Transformer so that it learns to predict the next token in a sequence.

Initially, every parameter in the model is randomly initialized.

During training, the model repeatedly predicts the next token, measures its error, and updates its parameters to reduce that error.

---

# Training Pipeline

```text
Training Sequences
        ↓
DataLoader
        ↓
Transformer
        ↓
Vocabulary Logits
        ↓
Cross Entropy Loss
        ↓
Backpropagation
        ↓
Optimizer
        ↓
Updated Parameters
```

This process is repeated for many epochs until the model converges.

---

# Training Data

The model is trained using autoregressive next-token prediction.

Example

Input

```text
[BOS A B C]
```

Target

```text
[A B C D]
```

The model receives the input sequence and attempts to predict the target sequence.

---

# Forward Pass

The forward pass computes predictions.

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

Each position contains one prediction for the next token.

---

# Vocabulary Logits

The Transformer does not directly output probabilities.

Instead it produces logits.

Example

```text
Token

↓

[2.14,
-1.07,
0.42,
...
3.81]
```

One value exists for every vocabulary token.

Higher values indicate greater confidence.

---

# Cross Entropy Loss

## Objective

Measure how different the predicted probability distribution is from the correct next token.

Pipeline

```text
Logits

↓

Softmax

↓

Probability Distribution

↓

Cross Entropy

↓

Loss
```

Lower loss indicates better predictions.

---

# Backpropagation

The loss alone does not improve the model.

Backpropagation computes gradients for every trainable parameter.

Conceptually

```text
Loss

↓

Gradients

↓

Every Layer

↓

Embedding Matrix

↓

Attention

↓

Feed Forward
```

Every parameter receives information about how it should change.

---

# Optimizer

CLRS-LLM uses AdamW.

AdamW combines

- adaptive learning rates
- momentum
- weight decay

It is the standard optimizer used for GPT-style models.

Each optimization step updates the parameters.

```text
Current Parameters

↓

Gradient

↓

AdamW

↓

Updated Parameters
```

---

# Epoch

An epoch represents one complete pass through the training dataset.

Example

```text
Epoch 1

↓

Every training example processed once
```

Training typically requires many epochs.

---

# Batch

Training examples are processed in batches rather than individually.

Example

```text
Batch Size

32 sequences
```

Benefits

- efficient GPU utilization
- stable gradient estimates
- faster training

---

# Gradient Descent

The optimizer attempts to minimize the loss.

Ideally

```text
Epoch 1

Loss 8.9

↓

Epoch 2

Loss 7.8

↓

Epoch 3

Loss 6.4

↓

...
```

A decreasing loss indicates that learning is occurring.

---

# Checkpointing

Training may take a long time.

Model checkpoints allow training to resume without starting from scratch.

Each checkpoint stores

- model weights
- optimizer state
- epoch number
- configuration

---

# Evaluation

Training loss measures how well the model fits the training data.

Evaluation measures how well the model generalizes.

Typical evaluation includes

- validation loss
- perplexity
- qualitative text generation

---

# Inference

After training, gradients are disabled.

Pipeline

```text
Prompt

↓

Tokenizer

↓

Transformer

↓

Vocabulary Logits

↓

Next Token

↓

Append

↓

Repeat
```

This autoregressive loop continues until

- an EOS token is produced,
- or the maximum generation length is reached.

---

# Engineering Decisions

- Used teacher forcing during training.
- Used Cross Entropy Loss.
- Used AdamW optimization.
- Planned checkpoint support.
- Separated training and inference pipelines.

---

# Lessons Learned

Training transforms a randomly initialized Transformer into a language model.

The architecture alone contains no knowledge.

Knowledge emerges through optimization.

Each optimization step slightly adjusts millions of parameters to better predict the next token.

Over thousands of updates, the model gradually learns statistical patterns present in the training corpus.