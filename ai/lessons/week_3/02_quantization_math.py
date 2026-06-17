"""
Week 3 — Quantization: simulate what happens when weights are compressed.

Shows the error introduced by quantization and why Q8 > Q4 in quality.
"""

import numpy as np


def quantize_int8(weights: np.ndarray) -> tuple:
    """
    Quantize float32 weights to int8.
    Maps [min, max] → [-128, 127].
    Returns quantized values and the scale factor needed to reconstruct.
    """
    w_min, w_max = weights.min(), weights.max()
    scale = (w_max - w_min) / 255.0

    # Shift to [0, 255], round to int, shift back to [-128, 127]
    quantized = np.round((weights - w_min) / scale).astype(np.int8)
    return quantized, scale, w_min


def dequantize_int8(quantized: np.ndarray, scale: float, w_min: float) -> np.ndarray:
    """Reconstruct float weights from int8."""
    return quantized.astype(np.float32) * scale + w_min


def quantize_int4(weights: np.ndarray) -> tuple:
    """
    Quantize float32 weights to 4-bit (values 0–15, stored as int8).
    Much more aggressive compression, more error.
    """
    w_min, w_max = weights.min(), weights.max()
    scale = (w_max - w_min) / 15.0  # 4-bit: 0 to 15

    quantized = np.round((weights - w_min) / scale).clip(0, 15).astype(np.uint8)
    return quantized, scale, w_min


def dequantize_int4(quantized: np.ndarray, scale: float, w_min: float) -> np.ndarray:
    return quantized.astype(np.float32) * scale + w_min


def measure_error(original: np.ndarray, reconstructed: np.ndarray) -> dict:
    error = original - reconstructed
    return {
        "max_abs_error": np.abs(error).max(),
        "mean_abs_error": np.abs(error).mean(),
        "rmse": np.sqrt((error**2).mean()),
    }


if __name__ == "__main__":
    print("=== Quantization Error Analysis ===\n")

    # Simulate a weight tensor (e.g., one row of an attention projection matrix)
    np.random.seed(42)
    original = np.random.randn(1000).astype(np.float32)

    print(f"Original weights: min={original.min():.3f}, max={original.max():.3f}")
    print(f"Memory: {original.nbytes} bytes (float32)\n")

    # INT8 quantization
    q8, scale8, min8 = quantize_int8(original)
    reconstructed_8 = dequantize_int8(q8, scale8, min8)
    err8 = measure_error(original, reconstructed_8)
    print(f"INT8 Quantization:")
    print(f"  Memory: {q8.nbytes} bytes (4x smaller)")
    print(f"  Max error:  {err8['max_abs_error']:.6f}")
    print(f"  Mean error: {err8['mean_abs_error']:.6f}")
    print(f"  RMSE:       {err8['rmse']:.6f}")

    # INT4 quantization
    q4, scale4, min4 = quantize_int4(original)
    reconstructed_4 = dequantize_int4(q4, scale4, min4)
    err4 = measure_error(original, reconstructed_4)
    print(f"\nINT4 Quantization:")
    print(f"  Memory: {q4.nbytes // 2} bytes (8x smaller, 2 values packed per byte)")
    print(f"  Max error:  {err4['max_abs_error']:.6f}")
    print(f"  Mean error: {err4['mean_abs_error']:.6f}")
    print(f"  RMSE:       {err4['rmse']:.6f}")

    print(f"\nINT4 error is {err4['rmse']/err8['rmse']:.1f}x larger than INT8.")

    # Memory comparison for a 7B model
    print("\n=== Memory Requirements for 7B Parameter Model ===")
    n_params = 7_000_000_000
    print(f"  FP32:  {n_params * 4 / 1e9:.1f} GB  (not runnable on your machine)")
    print(f"  BF16:  {n_params * 2 / 1e9:.1f} GB  (needs GPU)")
    print(f"  INT8:  {n_params * 1 / 1e9:.1f} GB")
    print(f"  INT4:  {n_params * 0.5 / 1e9:.1f} GB  ← saul-instruct-v1:Q8_0 is ~8.5GB")
    print("\nQ8_0 = INT8 with a slightly different encoding (per-block scale factors)")
    print("Trades a small quality drop for 4x memory reduction vs FP32.")
