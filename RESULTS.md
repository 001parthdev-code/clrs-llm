# CLRS-LLM Results

## Dataset

| Metric | Value |
|---------|------:|
| Source | Introduction to Algorithms (CLRS) |
| Corpus Characters | 2,525,115 |
| Corpus Words | 446,163 |
| Semantic Sections | 135 |
| Vocabulary Size | 8,196 |
| BPE Merge Rules | 8,077 |
| Context Length | 128 |

---

## Model

| Metric | Value |
|---------|------:|
| Parameters | 1,858,816 |
| Transformer Blocks | 4 |
| Attention Heads | 4 |
| Embedding Dimension | 128 |
| Model Size | 7.15 MB |

---

## Hardware

| Metric | Value |
|---------|------:|
| GPU | NVIDIA RTX 4060 Laptop |
| Framework | PyTorch |
| Backend | CUDA |

---

## Training Configuration

| Parameter | Value |
|-----------|------:|
| Optimizer | AdamW |
| Batch Size | 16 |
| Learning Rate | 3e-4 |
| Epochs | 10 |

---

## Training Results

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