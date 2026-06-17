"""
Week 1 — Visualize gradient descent on a simple loss landscape.

Shows why learning rate matters and what "converging" means geometrically.
"""

import numpy as np
import matplotlib.pyplot as plt


def loss(w: float) -> float:
    """A simple 1D loss function: (w - 3)^2 + sin(w). Minimum near w=3."""
    return (w - 3.0) ** 2 + 0.5 * np.sin(w * 2)


def gradient(w: float) -> float:
    """Derivative of the loss function."""
    return 2 * (w - 3.0) + 1.0 * np.cos(w * 2)


def gradient_descent(start: float, lr: float, steps: int = 30) -> list:
    """Run gradient descent, record the path."""
    w = start
    path = [w]
    for _ in range(steps):
        grad = gradient(w)
        w = w - lr * grad
        path.append(w)
    return path


if __name__ == "__main__":
    # The loss landscape
    w_range = np.linspace(-2, 7, 500)
    loss_values = [loss(w) for w in w_range]

    # Try three learning rates
    configs = [
        {"lr": 0.05, "label": "lr=0.05 (too slow)", "color": "blue"},
        {"lr": 0.3,  "label": "lr=0.3 (good)",      "color": "green"},
        {"lr": 1.2,  "label": "lr=1.2 (diverges)",  "color": "red"},
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Gradient Descent: Effect of Learning Rate", fontsize=14)

    for ax, cfg in zip(axes, configs):
        path = gradient_descent(start=-1.5, lr=cfg["lr"], steps=30)
        path_losses = [loss(w) for w in path]

        ax.plot(w_range, loss_values, 'k-', lw=2, label='Loss landscape')
        ax.plot(path, path_losses, 'o-', color=cfg["color"], lw=2,
                markersize=5, label=f'Path ({cfg["label"]})')
        ax.axvline(x=3.0, color='gray', linestyle='--', alpha=0.5, label='True minimum')
        ax.set_title(cfg["label"])
        ax.set_xlabel("Weight (w)")
        ax.set_ylabel("Loss")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        print(f"{cfg['label']}: start={path[0]:.2f} → end={path[-1]:.2f} | "
              f"final loss={path_losses[-1]:.4f}")

    plt.tight_layout()
    plt.savefig("gradient_descent.png", dpi=120)
    plt.show()
    print("\nSaved gradient_descent.png")
    print("\nObservation:")
    print("  - Too small lr: moves toward minimum but very slowly")
    print("  - Good lr: converges quickly")
    print("  - Too large lr: overshoots, bounces around, may diverge")
