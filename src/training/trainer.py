from tqdm import tqdm

import torch
import torch.nn as nn


class Trainer:
    """
    Handles the training loop for CLRS-LLM.
    """

    def __init__(
        self,
        model,
        dataloader,
        optimizer,
        device,
    ):

        self.model = model
        self.dataloader = dataloader
        self.optimizer = optimizer
        self.device = device

        self.criterion = nn.CrossEntropyLoss()

    def train_epoch(self):

        self.model.train()

        total_loss = 0.0

        progress = tqdm(self.dataloader)

        for inputs, targets in progress:

            inputs = inputs.to(self.device)
            targets = targets.to(self.device)

            # -----------------------------------------
            # Forward
            # -----------------------------------------

            logits = self.model(inputs)

            # -----------------------------------------
            # Reshape
            # -----------------------------------------

            batch_size, sequence_length, vocab_size = logits.shape

            logits = logits.view(
                batch_size * sequence_length,
                vocab_size,
            )

            targets = targets.view(
                batch_size * sequence_length,
            )

            # -----------------------------------------
            # Loss
            # -----------------------------------------

            loss = self.criterion(
                logits,
                targets,
            )

            # -----------------------------------------
            # Backprop
            # -----------------------------------------

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item()

            progress.set_postfix(
                loss=f"{loss.item():.4f}"
            )

        average_loss = (
            total_loss /
            len(self.dataloader)
        )

        return average_loss