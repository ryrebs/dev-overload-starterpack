"""
Week 1 — A single neuron (perceptron) from scratch.

No PyTorch, no TensorFlow. Just numpy.
Goal: understand what a weight is and how it changes during training.
"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)


class Perceptron:
    def __init__(self, n_inputs: int, learning_rate: float = 0.1):
        # Weights and bias are just numbers — initialized randomly
        self.weights = np.random.randn(n_inputs) * 0.1
        self.bias = 0.0
        self.lr = learning_rate

    def forward(self, x: np.ndarray) -> float:
        """Forward pass: compute output for input x."""
        z = np.dot(self.weights, x) + self.bias  # linear combination
        return sigmoid(z)                          # activation

    def train_step(self, x: np.ndarray, y_true: float) -> float:
        """One training step: forward, compute loss, update weights."""
        # Forward pass
        z = np.dot(self.weights, x) + self.bias
        y_pred = sigmoid(z)

        # Loss: Mean Squared Error
        loss = (y_pred - y_true) ** 2

        # Gradient: how much does loss change with respect to each weight?
        # Chain rule: dL/dw = dL/dy_pred * dy_pred/dz * dz/dw
        dl_dy = 2 * (y_pred - y_true)        # dL/dy_pred
        dy_dz = sigmoid_derivative(z)          # dy_pred/dz
        dz_dw = x                              # dz/dw
        dz_db = 1.0                            # dz/db

        gradient_w = dl_dy * dy_dz * dz_dw
        gradient_b = dl_dy * dy_dz * dz_db

        # Update: move opposite to gradient
        self.weights -= self.lr * gradient_w
        self.bias -= self.lr * gradient_b

        return loss

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000):
        for epoch in range(epochs):
            total_loss = 0
            for xi, yi in zip(X, y):
                total_loss += self.train_step(xi, yi)
            if epoch % 100 == 0:
                avg_loss = total_loss / len(X)
                print(f"Epoch {epoch:4d} | Loss: {avg_loss:.4f} | "
                      f"weights: {self.weights.round(3)} | bias: {self.bias:.3f}")


if __name__ == "__main__":
    print("=== Perceptron: Learning OR gate ===\n")

    # OR gate: output 1 if any input is 1
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ], dtype=float)
    y = np.array([0, 1, 1, 1], dtype=float)

    p = Perceptron(n_inputs=2, learning_rate=0.5)

    print("Before training:")
    for xi, yi in zip(X, y):
        print(f"  input={xi} | expected={yi} | predicted={p.forward(xi):.3f}")

    print("\nTraining...")
    p.train(X, y, epochs=1000)

    print("\nAfter training:")
    for xi, yi in zip(X, y):
        pred = p.forward(xi)
        print(f"  input={xi} | expected={yi} | predicted={pred:.3f} | correct={round(pred) == yi}")

    print(f"\nFinal weights: {p.weights.round(4)}")
    print(f"Final bias: {p.bias:.4f}")
    print("\nThe weights encode the OR logic. Inputs with higher weights are 'more important'.")
