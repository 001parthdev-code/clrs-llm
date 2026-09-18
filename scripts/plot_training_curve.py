from pathlib import Path

import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Training Loss
# ---------------------------------------------------------

losses = [
    3.1056,
    1.9902,
    1.6474,
    1.4612,
    1.3412,
    1.2586,
    1.1995,
    1.1558,
    1.1229,
    1.0971,
]

epochs = list(range(1, len(losses) + 1))


# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    epochs,
    losses,
    marker="o",
    linewidth=2,
)

plt.title("CLRS-LLM Training Loss")

plt.xlabel("Epoch")

plt.ylabel("Cross Entropy Loss")

plt.xticks(epochs)

plt.grid(True)

plt.tight_layout()


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

output_dir = Path("results")

output_dir.mkdir(
    parents=True,
    exist_ok=True,
)

plt.savefig(
    output_dir / "training_curve.png",
    dpi=300,
)

plt.close()

print("Training curve saved to results/training_curve.png")