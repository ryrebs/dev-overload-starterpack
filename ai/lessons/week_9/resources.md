# Week 9 Resources

## Must-Read
- **LoRA paper (Hu et al., 2021)** — the original LoRA method
- **QLoRA paper (Dettmers et al., 2023)** — quantized fine-tuning on consumer hardware
- **Axolotl** — production fine-tuning framework (wraps HuggingFace/PEFT)

## Reference
- **HuggingFace PEFT docs** — LoRA, QLoRA, Prefix Tuning, Adapters
- **TRL (Transformers Reinforcement Learning)** — SFTTrainer, DPOTrainer
- **bitsandbytes docs** — quantization during training (4-bit, 8-bit)
- **Unsloth** — 2x faster QLoRA training with less VRAM

## Colab Setup
```python
# Minimal Colab setup for QLoRA
!pip install -q transformers peft accelerate bitsandbytes trl datasets unsloth
```

## Practice
- Run 01_lora_math.py locally — understand LoRA from first principles
- Generate 100 Q&A pairs with 02_prepare_dataset.py
- Fine-tune in Colab using 03_qlora_training.py
- Compare the fine-tuned model vs. the base model on your golden dataset

## What Interviewers Ask
- "What is the difference between fine-tuning and RAG? When to use each?"
- "What is LoRA and why does it reduce memory requirements?"
- "What is catastrophic forgetting and how does LoRA avoid it?"
- "What is QLoRA and what hardware does it need?"
- "How do you evaluate whether fine-tuning improved the model?"
