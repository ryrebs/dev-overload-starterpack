"""
Week 9 — LoRA math from scratch.

LoRA adds a small low-rank update to a frozen weight matrix.
This shows exactly what happens to the weights during LoRA fine-tuning.
"""

import numpy as np


class LoRALayer:
    """
    A single LoRA-augmented linear layer.

    Original: y = W @ x        (W is frozen)
    LoRA:     y = W @ x + (B @ A) @ x
                = (W + B @ A) @ x

    Only A and B are trained. W never changes.
    """

    def __init__(self, in_dim: int, out_dim: int, rank: int, alpha: float = 1.0):
        self.W = np.random.randn(out_dim, in_dim) * 0.02  # frozen base weights
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # LoRA matrices (trainable)
        # A: in_dim → rank   (initialized randomly)
        # B: rank → out_dim  (initialized to zero — no change at start)
        self.A = np.random.randn(rank, in_dim) * 0.02
        self.B = np.zeros((out_dim, rank))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass with LoRA."""
        base_output = self.W @ x
        lora_output = (self.B @ self.A) @ x * self.scaling
        return base_output + lora_output

    def parameter_count(self) -> dict:
        return {
            "base (frozen)": self.W.size,
            "lora_A": self.A.size,
            "lora_B": self.B.size,
            "trainable": self.A.size + self.B.size,
            "trainable_fraction": (self.A.size + self.B.size) / self.W.size,
        }


def compare_parameter_counts():
    """Show how LoRA drastically reduces trainable parameters."""
    print("=== LoRA Parameter Count Comparison ===\n")

    configs = [
        {"name": "Attention Q projection (7B model)", "in_dim": 4096, "out_dim": 4096},
        {"name": "Feed-forward layer (7B model)", "in_dim": 4096, "out_dim": 11008},
    ]

    for cfg in configs:
        print(f"{cfg['name']}:")
        full_params = cfg["in_dim"] * cfg["out_dim"]
        print(f"  Full fine-tuning: {full_params:,} parameters")

        for rank in [4, 8, 16, 32]:
            lora_params = rank * (cfg["in_dim"] + cfg["out_dim"])
            fraction = lora_params / full_params
            print(f"  LoRA rank={rank:2d}:    {lora_params:,} parameters ({fraction:.2%} of full)")
        print()


def demonstrate_lora_update():
    """Show that B@A starts at zero (no change to base model output initially)."""
    print("=== LoRA Starts with Zero Update ===\n")

    layer = LoRALayer(in_dim=8, out_dim=4, rank=2, alpha=1.0)
    x = np.random.randn(8)

    base_output = layer.W @ x
    lora_update = (layer.B @ layer.A) @ x * layer.scaling

    print(f"Base output (W @ x):       {base_output.round(4)}")
    print(f"LoRA update (B @ A @ x):   {lora_update.round(4)}  ← all zeros at init")
    print(f"Combined output:           {layer.forward(x).round(4)}")
    print(f"\nAt initialization, LoRA adds nothing (B=0).")
    print("Training adjusts A and B to add the task-specific update.")


def simulate_lora_training():
    """Simulate one training step of LoRA."""
    print("\n=== Simulating LoRA Training Step ===\n")

    np.random.seed(42)
    layer = LoRALayer(in_dim=4, out_dim=2, rank=1, alpha=1.0)
    lr = 0.01

    # Target: we want the layer to learn y = [1, -1] for a specific input
    x = np.array([1.0, 0.0, 0.0, 0.0])
    y_target = np.array([1.0, -1.0])

    print("Before training:")
    print(f"  Output: {layer.forward(x).round(4)}")
    print(f"  Target: {y_target}")

    W_before = layer.W.copy()

    for step in range(100):
        y_pred = layer.forward(x)
        loss = np.sum((y_pred - y_target) ** 2)

        # Gradient w.r.t. B and A (not W — it's frozen)
        dl_dy = 2 * (y_pred - y_target)

        # dL/dB = dl_dy @ (A @ x).T
        dl_dB = np.outer(dl_dy, (layer.A @ x) * layer.scaling)
        # dL/dA = B.T @ dl_dy @ x.T
        dl_dA = np.outer(layer.B.T @ dl_dy, x) * layer.scaling

        layer.B -= lr * dl_dB
        layer.A -= lr * dl_dA

        if step % 20 == 0:
            print(f"  Step {step:3d} | Loss: {loss:.4f} | Output: {y_pred.round(3)}")

    print("\nAfter training:")
    print(f"  Output: {layer.forward(x).round(4)}")
    print(f"  Target: {y_target}")
    print(f"\nBase weights W changed: {not np.allclose(W_before, layer.W)}")
    print("Base weights are frozen — only A and B changed.")


if __name__ == "__main__":
    compare_parameter_counts()
    demonstrate_lora_update()
    simulate_lora_training()
