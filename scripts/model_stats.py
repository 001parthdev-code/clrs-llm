from src.model.config import ModelConfig
from src.model.transformer import CLRSLLM


def count_parameters(model):

    total = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    trainable = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )

    return total, trainable


def model_size_mb(model):

    size = 0

    for parameter in model.parameters():
        size += parameter.numel() * parameter.element_size()

    for buffer in model.buffers():
        size += buffer.numel() * buffer.element_size()

    return size / (1024 ** 2)


def main():

    config = ModelConfig()

    model = CLRSLLM(config)

    total, trainable = count_parameters(model)

    print("=" * 60)
    print("CLRS-LLM Model Statistics")
    print("=" * 60)

    print(f"Vocabulary Size      : {config.vocab_size}")
    print(f"Context Length       : {config.context_length}")
    print(f"Embedding Dimension  : {config.embedding_dim}")
    print(f"Transformer Layers   : {config.num_layers}")
    print(f"Attention Heads      : {config.num_heads}")

    print()

    print(f"Total Parameters     : {total:,}")
    print(f"Trainable Parameters : {trainable:,}")

    print(f"Model Size           : {model_size_mb(model):.2f} MB")

    print("=" * 60)


if __name__ == "__main__":
    main()