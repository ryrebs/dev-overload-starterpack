"""
Week 9 — QLoRA fine-tuning script.

RUN THIS IN GOOGLE COLAB (free T4 GPU):
1. Open Colab: https://colab.research.google.com
2. Runtime → Change runtime type → T4 GPU
3. Upload training_data.jsonl (from 02_prepare_dataset.py)
4. Run this script

This fine-tunes Llama-3.2-3B-Instruct on legal Q&A using QLoRA.
Expected time: 20-45 minutes on a T4 GPU.
"""

# --- SETUP (run in Colab first) ---
# !pip install -q transformers peft accelerate bitsandbytes trl datasets

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from trl import SFTTrainer


# --- Configuration ---
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
OUTPUT_DIR = "./legal-lora-output"
TRAINING_DATA_PATH = "training_data.jsonl"


def load_model_and_tokenizer():
    """Load the base model in 4-bit quantization."""
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",          # NF4 quantization
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,     # Double quantization for extra savings
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    return model, tokenizer


def add_lora_adapters(model):
    """Add LoRA adapters to the model."""
    lora_config = LoraConfig(
        r=16,                          # rank: higher = more capacity, more memory
        lora_alpha=32,                 # scaling: alpha/rank = effective learning rate for LoRA
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # attention layers
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    trainable, total = model.get_nb_trainable_parameters()
    print(f"Trainable: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")
    return model


def format_sharegpt(example: dict) -> str:
    """Convert ShareGPT format to a single training string."""
    convs = example["conversations"]
    system = next((c["value"] for c in convs if c["from"] == "system"), "")
    human = next((c["value"] for c in convs if c["from"] == "human"), "")
    gpt = next((c["value"] for c in convs if c["from"] == "gpt"), "")

    return f"<|system|>\n{system}\n<|user|>\n{human}\n<|assistant|>\n{gpt}"


def train():
    print("Loading model (this takes 2-3 minutes in Colab)...")
    model, tokenizer = load_model_and_tokenizer()
    model = add_lora_adapters(model)

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=TRAINING_DATA_PATH, split="train")
    print(f"Training on {len(dataset)} examples.")

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,     # effective batch = 4*4 = 16
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        save_strategy="epoch",
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_args,
        formatting_func=format_sharegpt,
        max_seq_length=1024,
    )

    print("Starting training...")
    trainer.train()

    print("Saving LoRA adapter...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Done! Adapter saved to {OUTPUT_DIR}")
    print("\nNext: run 04_merge_and_use.py to merge the adapter and test it.")


if __name__ == "__main__":
    if not torch.cuda.is_available():
        print("No GPU detected.")
        print("This script must be run in Google Colab with a T4 GPU runtime.")
        print("Steps:")
        print("  1. Go to https://colab.research.google.com")
        print("  2. Runtime > Change runtime type > T4 GPU")
        print("  3. Upload training_data.jsonl")
        print("  4. Run this script")
    else:
        train()
