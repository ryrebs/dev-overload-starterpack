# Week 3 Resources

## Must-Read
- **llama.cpp README** — understand what GGUF actually is and how quantization works
- **GGUF spec** — technical format specification
- **bitsandbytes paper** — INT8 quantization for LLMs (what makes Q8_0 possible)
- **GPTQ paper** — smarter quantization (what Q4_K_M uses)

## Reference
- **Ollama model library** — available models and their sizes
- **HuggingFace GGUF files** — how to find and download GGUF models
- **llama.cpp quantization guide** — all the quant types explained

## Practice
- Run `ollama show <model>` and understand each line of the Modelfile
- Try pulling a Q4_K_M variant and compare output quality to Q8_0
- Measure tokens/second for both: `time python 03_generation_params.py`

## What Interviewers Ask
- "Why can't you run a BF16 model on CPU efficiently?"
- "What is quantization and what's the trade-off?"
- "What is GGUF and why does Ollama use it?"
- "What's the difference between the model weights and the model architecture?"
