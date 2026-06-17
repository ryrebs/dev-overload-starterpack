"""
Week 1 — A 3-layer neural network trained on XOR.

XOR cannot be solved by a single perceptron (it's not linearly separable).
A hidden layer solves this. This demonstrates why depth matters.
"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1 - s)


class NeuralNetwork:
    """
    Architecture: input(2) → hidden(4) → output(1)
    All weights stored as numpy arrays.
    """

    def __init__(self, lr: float = 0.5):
        self.lr = lr
        # Layer 1: input(2) → hidden(4)
        self.W1 = np.random.randn(2, 4) * 0.5
        self.b1 = np.zeros(4)
        # Layer 2: hidden(4) → output(1)
        self.W2 = np.random.randn(4, 1) * 0.5
        self.b2 = np.zeros(1)

    def forward(self, x: np.ndarray) -> tuple:
        """Forward pass. Returns (output, cache) where cache is used in backprop."""
        # Layer 1
        z1 = x @ self.W1 + self.b1  # (n, 4)
        a1 = sigmoid(z1)             # (n, 4)
        # Layer 2
        z2 = a1 @ self.W2 + self.b2  # (n, 1)
        a2 = sigmoid(z2)              # (n, 1)
        return a2, (x, z1, a1, z2, a2)

    def backward(self, cache: tuple, y: np.ndarray) -> dict:
        """Backpropagation: compute gradients for all weights."""
        x, z1, a1, z2, a2 = cache
        n = x.shape[0]

        # Output layer gradient
        dL_da2 = 2 * (a2 - y) / n           # dL/da2
        dL_dz2 = dL_da2 * sigmoid_grad(z2)  # dL/dz2 (chain rule)
        dL_dW2 = a1.T @ dL_dz2              # dL/dW2
        dL_db2 = dL_dz2.sum(axis=0)

        # Hidden layer gradient (chain rule through layer 2)
        dL_da1 = dL_dz2 @ self.W2.T
        dL_dz1 = dL_da1 * sigmoid_grad(z1)
        dL_dW1 = x.T @ dL_dz1
        dL_db1 = dL_dz1.sum(axis=0)

        return {"W1": dL_dW1, "b1": dL_db1, "W2": dL_dW2, "b2": dL_db2}

    def update(self, grads: dict):
        """Gradient descent: nudge each weight opposite to its gradient."""
        self.W1 -= self.lr * grads["W1"]
        self.b1 -= self.lr * grads["b1"]
        self.W2 -= self.lr * grads["W2"]
        self.b2 -= self.lr * grads["b2"]

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 5000):
        for epoch in range(epochs):
            output, cache = self.forward(X)
            loss = np.mean((output - y) ** 2)
            grads = self.backward(cache, y)
            self.update(grads)
            if epoch % 500 == 0:
                print(f"Epoch {epoch:5d} | Loss: {loss:.5f}")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        output, _ = self.forward(X)
        return output


if __name__ == "__main__":
    print("=== Neural Network: Learning XOR ===")
    print("A perceptron CANNOT learn XOR. A hidden layer CAN.\n")

    # XOR: output is 1 only when inputs differ
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    print("Training a single perceptron on XOR...")
    from 01_perceptron import Perceptron
    p = Perceptron(n_inputs=2, learning_rate=0.5)
    p.train(X, y, epochs=2000)
    print("Perceptron predictions (should fail):")
    for xi, yi in zip(X, y):
        pred = p.forward(xi)
        print(f"  input={xi} | expected={yi[0]} | predicted={pred:.3f}")

    print("\n" + "="*50)
    print("Training a 2-layer network on XOR...")
    nn = NeuralNetwork(lr=2.0)
    nn.train(X, y, epochs=5000)

    print("\n2-layer network predictions (should succeed):")
    preds = nn.predict(X)
    for xi, yi, pred in zip(X, y, preds):
        correct = round(float(pred)) == int(yi)
        print(f"  input={xi} | expected={yi[0]} | predicted={pred[0]:.3f} | correct={correct}")

    print("\nThe hidden layer learns intermediate representations.")
    print("This is why depth in neural networks matters.")
