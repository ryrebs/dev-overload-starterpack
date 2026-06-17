# Week 1 — Neural Networks: How Machines Learn

Everything in AI is built on one idea: a function with learnable parameters. This week you will understand what those parameters are, how they change, and why that matters for every model you will ever use.

---

## What a Neural Network Actually Is

A neural network is a function: it takes numbers in, does math, returns numbers out.

```
input → [weights + biases] → activation → output
```

The "learning" part: we adjust the weights so the output gets closer to what we want.

A **weight** is just a number. A 7B parameter model has 7 billion of these numbers. They encode everything the model "knows."

---

## The Perceptron: The Simplest Possible Network

One neuron:
1. Take input values `x = [x1, x2, x3]`
2. Multiply each by a weight `w = [w1, w2, w3]`
3. Add a bias `b`
4. Apply an activation function

```
output = activation(w · x + b)
         = activation(w1*x1 + w2*x2 + w3*x3 + b)
```

The **dot product** `w · x` measures alignment: if the inputs match the weights, the output is large.

---

## Activation Functions: Adding Non-Linearity

Without activation functions, stacking layers does nothing (you just get a big linear function). Activation functions add non-linearity — the ability to model curves, not just lines.

| Name | Formula | Used for |
|------|---------|---------|
| ReLU | max(0, x) | Hidden layers (default) |
| Sigmoid | 1/(1+e^-x) | Binary outputs |
| Softmax | e^x_i / Σe^x_j | Multi-class probabilities |
| GELU | x·Φ(x) | Transformers |

---

## Multi-Layer Networks

Stack layers: the output of one becomes the input of the next.

```
input → Layer 1 (weights + activation) → Layer 2 → ... → output
```

Each layer learns a different level of abstraction. For text:
- Early layers: individual character/token patterns
- Middle layers: word meanings and syntax
- Late layers: semantic relationships and facts

---

## How Learning Works: Gradient Descent

Training is an optimization problem: minimize the difference between predicted output and correct output.

**Loss function**: measures how wrong the model is. Common ones:
- Mean Squared Error: `L = (predicted - true)²`
- Cross-Entropy: `L = -log(P(correct_class))`

**Gradient**: the slope of the loss function. Points toward where the loss increases. We move *opposite* to it.

**Update rule:**
```
weight = weight - learning_rate * gradient
```

Small learning rate → slow but stable. Large → fast but can overshoot.

---

## Backpropagation

How do we compute gradients for all layers at once?

Backpropagation applies the **chain rule** from calculus: to find how a weight in layer 1 affects the output, multiply the derivatives along the entire path from that weight to the loss.

```
dL/dw = dL/doutput × doutput/dlayer3 × dlayer3/dlayer2 × dlayer2/dw
```

PyTorch does this automatically with `loss.backward()`. You never have to do it by hand, but understanding it tells you:
- Why deep networks can be hard to train (vanishing/exploding gradients)
- Why residual connections (used in transformers) help
- Why certain architectures work better than others

---

## What Gets Stored in a Model File

After training, you save the weights. That's it. The architecture (how layers connect) is code; the weights are the learned numbers.

A GGUF file (what Ollama uses) stores:
- The weight tensors, quantized to save space
- Metadata: architecture, vocab, context length
- Hyperparameters: layer count, head count, embedding dimension

When you run `ollama run bge-m3`, it loads these weights into RAM and runs the forward pass on your input.

---

## Connection to This Project

`bge-m3` (your embedding model) is a neural network. When you call `embed_texts(["some legal text"])`:
1. Input tokens → embeddings (learnable weight matrix)
2. Multiple transformer layers process the sequence
3. Final hidden state of `[CLS]` token = the embedding vector

The 1024 numbers it returns are the output of the last layer. Similar texts produce similar vectors because the weights were trained to make it so.

---

## Vocabulary

| Term | Definition |
|------|-----------|
| Weight / Parameter | A learnable number in the model |
| Bias | A learnable offset added to each neuron |
| Activation function | Non-linear function applied after each layer |
| Loss function | Measures how wrong the prediction is |
| Gradient | The slope of the loss — direction of steepest increase |
| Learning rate | How big each update step is |
| Backpropagation | Algorithm to compute gradients via chain rule |
| Epoch | One full pass through the training data |
| Batch | A subset of training data processed at once |

---

## This Week's Code

Run these in order:

1. `01_perceptron.py` — a single neuron from scratch in numpy
2. `02_neural_network.py` — a 3-layer network trained on XOR
3. `03_gradient_descent_visual.py` — visualize the loss landscape

```bash
pip install numpy matplotlib
python 01_perceptron.py
python 02_neural_network.py
python 03_gradient_descent_visual.py
```
