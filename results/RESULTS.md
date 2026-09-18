# CLRS-LLM Results

## Dataset

| Metric | Value |
|--------|------:|
| Source | Introduction to Algorithms (CLRS) |
| Semantic Sections | 135 |
| Vocabulary Size | 8,196 |
| BPE Merge Rules | 8,077 |
| Context Length | 128 |

---

## Model

| Metric | Value |
|--------|------:|
| Architecture | Decoder-only Transformer |
| Transformer Blocks | 4 |
| Attention Heads | 4 |
| Embedding Dimension | 128 |
| Total Parameters | 1,858,816 |
| Trainable Parameters | 1,858,816 |
| Model Size | 7.15 MB |

---

## Hardware

| Metric | Value |
|--------|------:|
| Device | NVIDIA RTX 4060 |
| Backend | CUDA |

---

## Training

| Metric | Value |
|--------|------:|
| Optimizer | AdamW |
| Loss Function | Cross Entropy |
| Epochs | 10 |
| Batch Size | 16 |
| Learning Rate | 3e-4 |

---

## Training Loss

| Epoch | Average Loss |
|------:|-------------:|
| 1 | 3.1056 |
| 2 | 1.9902 |
| 3 | 1.6474 |
| 4 | 1.4612 |
| 5 | 1.3412 |
| 6 | 1.2586 |
| 7 | 1.1995 |
| 8 | 1.1558 |
| 9 | 1.1229 |
| 10 | 1.0971 |

---

## Qualitative Evaluation

### Prompt

```text
Insertion sort
```

### Output

```text
Insertion sort is a heap...
...
```

### Observation

The model successfully learned the vocabulary, formatting, chapter structure, and writing style of CLRS. Although semantic coherence is limited, the generated text remains within the domain of algorithms and data structures.

---

### Prompt

```text
Dynamic programming
```

### Output

```text
Dynamic programming is a greedy algorithm...
flow network...
```

### Observation

The model captures concepts from the training corpus but occasionally mixes related algorithmic topics. This behavior is expected for a compact Transformer trained on a single textbook.

---

## Conclusion

CLRS-LLM successfully completed end-to-end training and autoregressive inference.

The project demonstrates the complete engineering pipeline behind a decoder-only Transformer, including data preprocessing, tokenizer implementation, dataset construction, model architecture, GPU training, checkpointing, and text generation.