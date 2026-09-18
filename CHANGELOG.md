# Changelog

All notable changes to CLRS-LLM are documented here.

---

## v1.0.0

### Added

- End-to-end preprocessing pipeline
- Corpus profiling
- Corpus cleaning
- Semantic corpus preparation
- Section extraction
- Custom Byte Pair Encoding (BPE) tokenizer
- Dataset tokenization
- Sliding-window training sequence generation
- GPT-style decoder-only Transformer
- Multi-head causal self-attention
- Feed Forward Network
- Transformer blocks
- GPU training pipeline
- Automatic checkpointing
- Autoregressive text generation
- Engineering documentation
- Model card
- Training results
- Generated examples

### Training

- NVIDIA RTX 4060
- CUDA
- AdamW optimizer
- Cross Entropy Loss
- 10 training epochs

Final Training Loss

```text
1.0971
```

---

## Planned

### v1.1

- Temperature Sampling
- Top-k Sampling
- Top-p Sampling

### v1.2

- Rotary Position Embeddings (RoPE)
- Flash Attention

### v1.3

- Mixed Precision Training
- Validation Pipeline
- Perplexity Evaluation

### v2.0

- Larger Training Corpus
- Scaling Experiments