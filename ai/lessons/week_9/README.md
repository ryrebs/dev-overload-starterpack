# Week 9 — Fine-Tuning, LoRA, and QLoRA

You've used pretrained models. This week you learn to train them further on your own data. Fine-tuning is what separates a general assistant from a specialist.

**Hardware note:** fine-tuning requires a GPU. Use Google Colab (free tier works for 7B models with QLoRA). The theory and data preparation can be done locally; the training run needs GPU.

---

## When to Fine-Tune vs. When to Prompt

| Situation | Solution |
|-----------|---------|
| Model needs factual knowledge from your documents | RAG (not fine-tuning) |
| Model needs to output a specific format | Prompt engineering |
| Model needs a specific *behavior style* consistently | Fine-tuning |
| Model needs domain vocabulary and reasoning patterns | Fine-tuning |
| Model performs poorly even with good prompts | Fine-tuning |

For the legal system: fine-tuning a model on Philippine legal Q&A pairs would improve its ability to cite correctly, use correct legal terminology, and follow the `established/answer/citations` format without extensive prompting.

---

## What Fine-Tuning Actually Does

Pretraining: train on the entire internet (trillions of tokens), learns general language.

Fine-tuning: continue training on a small, specific dataset. The weights shift toward the new distribution.

**The loss:**
```
For each training example (instruction, response):
    loss = cross_entropy(model_output, expected_response)
    update weights via backprop
```

Same math as pretraining. Smaller dataset, smaller learning rate, shorter training.

---

## Full Fine-Tuning vs. LoRA

**Full fine-tuning**: update all 7 billion weights.
- Requires ~28+ GB VRAM (F32) or ~14 GB (BF16)
- Very expensive
- Risk of "catastrophic forgetting" — model forgets what it knew

**LoRA (Low-Rank Adaptation)**: instead of updating the full weight matrix W, add a small update:

```
W_updated = W + ΔW
         = W + (A × B)
```

Where A is (d × r) and B is (r × d), and r << d (rank is much smaller than dimension).

For a 4096×4096 weight matrix:
- Full update: 16M parameters
- LoRA rank=16: 4096×16 + 16×4096 = 131K parameters (1% of full)

**You only update A and B. W stays frozen.**

Benefits:
- ~100× fewer trainable parameters
- Can train on consumer GPU (8–16 GB VRAM)
- Easy to swap: keep the base model, swap the LoRA adapter
- Multiple adapters for different tasks on the same base model

---

## QLoRA: LoRA + Quantization for Even Less VRAM

**QLoRA** loads the base model in 4-bit NF4 quantization (2 GB for a 7B model), then trains LoRA adapters in BF16.

```
Base model (frozen, 4-bit):  ~4 GB
LoRA adapters (trainable):   ~500 MB
Optimizer states:            ~1 GB
Total VRAM:                  ~6-7 GB
```

A 7B model fine-tunable on a free Colab T4 GPU (15 GB VRAM). This is the standard method for consumer hardware.

---

## Training Data Format

For instruction fine-tuning, each example is a (system, instruction, response) triple.

**Alpaca format:**
```json
{
  "instruction": "What are the rights of an accused person under the Philippine Constitution?",
  "input": "",
  "output": "Under Article III Section 14 of the 1987 Philippine Constitution, an accused person has the right to be presumed innocent until the contrary is proved beyond reasonable doubt..."
}
```

**ShareGPT/conversation format:**
```json
{
  "conversations": [
    {"from": "system", "value": "You are a Philippine legal assistant."},
    {"from": "human", "value": "What is the age of majority?"},
    {"from": "gpt", "value": "Under Article 234 of the Family Code..."}
  ]
}
```

For your legal system: create Q&A pairs from the Philippine Constitution and Civil Code. The golden dataset from Week 6 is your starting point.

---

## The QLoRA Training Pipeline

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import torch

# 1. Load base model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
    device_map="auto",
)
model = prepare_model_for_kbit_training(model)

# 2. Add LoRA adapters
lora_config = LoraConfig(
    r=16,                    # rank
    lora_alpha=32,           # scaling factor
    target_modules=["q_proj", "v_proj"],  # which layers to adapt
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# 3. Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./legal-lora",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
        fp16=True,
    ),
)
trainer.train()

# 4. Save adapter (NOT the full model)
model.save_pretrained("./legal-lora-adapter")
```

---

## Using a LoRA Adapter

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

# Attach the adapter
model = PeftModel.from_pretrained(base_model, "./legal-lora-adapter")

# Merge for faster inference (optional)
model = model.merge_and_unload()

# Use exactly like any other model
```

Or convert to GGUF and load in Ollama for CPU inference.

---

## Converting to GGUF (for CPU/Ollama)

After training:
```bash
# 1. Merge adapter into base model
python merge_adapter.py

# 2. Convert to GGUF
python llama.cpp/convert_hf_to_gguf.py ./merged-model --outtype q4_k_m

# 3. Copy to Ollama model directory
ollama create legal-finetuned -f Modelfile
```

Now your fine-tuned model runs via Ollama just like any other model. The entire pipeline: same code, better model.

---

## What to Expect from Fine-Tuning

After fine-tuning on ~500 Philippine legal Q&A pairs:
- Model consistently uses the `established/answer/citations` format
- Legal terminology is more accurate
- Citation verbatim accuracy improves
- `established=False` cases are handled more gracefully

What doesn't improve:
- Retrieval quality (that's the embedding model, not the reasoning model)
- Knowledge of documents not in the training set (that's RAG's job)
- Hallucinations on novel questions (still need retrieval)

Fine-tuning and RAG are complementary. RAG provides documents; fine-tuning provides better reasoning patterns.

---

## This Week's Code

1. `01_lora_math.py` — implement LoRA from scratch in numpy
2. `02_prepare_dataset.py` — build a training dataset from the legal documents
3. `03_qlora_training.py` — full QLoRA training script (run on Colab)
4. `04_merge_and_use.py` — merge adapter and test the fine-tuned model

**For training (Colab):**
- Open `03_qlora_training.py` in Colab
- Select Runtime → T4 GPU
- Run all cells (~30–60 min for 500 examples)

```bash
pip install transformers peft accelerate bitsandbytes datasets trl
python 01_lora_math.py
python 02_prepare_dataset.py
```
