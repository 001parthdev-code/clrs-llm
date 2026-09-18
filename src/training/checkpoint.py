from pathlib import Path

import torch


def save_checkpoint(
    model,
    optimizer,
    epoch,
    loss,
    config,
    path,
):
    """
    Save a training checkpoint.
    """

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "config": vars(config),
        "loss": loss,
    }

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.save(
        checkpoint,
        path,
    )


def load_checkpoint(
    model,
    optimizer,
    path,
    device="cpu",
):
    """
    Load a checkpoint.
    """

    checkpoint = torch.load(
        path,
        map_location=device,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    optimizer.load_state_dict(
        checkpoint["optimizer_state_dict"]
    )

    return checkpoint