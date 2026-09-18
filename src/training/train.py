from pathlib import Path

import torch
from torch.utils.data import DataLoader

from src.model.config import ModelConfig
from src.model.transformer import CLRSLLM
from src.training.checkpoint import save_checkpoint
from src.training.dataset import CLRSDataset
from src.training.trainer import Trainer


def main():

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    config = ModelConfig()

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Using {device}")

    # ---------------------------------------------------------
    # Dataset
    # ---------------------------------------------------------

    dataset = CLRSDataset(
        Path("data/training")
    )

    loader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=True,
    )

    # ---------------------------------------------------------
    # Model
    # ---------------------------------------------------------

    model = CLRSLLM(config).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=3e-4,
    )

    trainer = Trainer(
        model=model,
        dataloader=loader,
        optimizer=optimizer,
        device=device,
    )

    # ---------------------------------------------------------
    # Training
    # ---------------------------------------------------------

    epochs = 10

    best_loss = float("inf")
    best_epoch = 0

    for epoch in range(epochs):

        print(f"\nEpoch {epoch + 1}/{epochs}")

        loss = trainer.train_epoch()

        print(f"Average Loss: {loss:.4f}")

        # -----------------------------------------------------
        # Save Epoch Checkpoint
        # -----------------------------------------------------

        save_checkpoint(
            model=model,
            optimizer=optimizer,
            epoch=epoch + 1,
            loss=loss,
            config=config,
            path=f"checkpoints/epoch_{epoch + 1}.pt",
        )

        # -----------------------------------------------------
        # Save Best Model
        # -----------------------------------------------------

        if loss < best_loss:

            best_loss = loss
            best_epoch = epoch + 1

            model_dir = Path("models")
            model_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "config": vars(config),
                    "best_loss": best_loss,
                    "epoch": best_epoch,
                },
                model_dir / "clrs_llm_best.pt",
            )

    # ---------------------------------------------------------
    # Save Final Model
    # ---------------------------------------------------------

    model_dir = Path("models")
    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "config": vars(config),
            "final_loss": loss,
            "epoch": epochs,
        },
        model_dir / "clrs_llm_v1.pt",
    )

    # ---------------------------------------------------------
    # Training Summary
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("Training Complete")
    print("=" * 60)
    print(f"Best Epoch : {best_epoch}")
    print(f"Best Loss  : {best_loss:.4f}")
    print()
    print("Saved Files")
    print("-----------")
    print("Checkpoints : checkpoints/")
    print("Best Model  : models/clrs_llm_best.pt")
    print("Final Model : models/clrs_llm_v1.pt")
    print("=" * 60)


if __name__ == "__main__":
    main()