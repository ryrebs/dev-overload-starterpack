"""
Week 9 — Merge LoRA adapter into base model and test it.

After training in Colab:
1. Download the ./legal-lora-output/ directory
2. Run this script to merge and test
3. Optionally convert to GGUF for Ollama
"""

import sys
from pathlib import Path


def merge_adapter(base_model_name: str, adapter_path: str, output_path: str):
    """Merge the LoRA adapter into the base model weights."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
    except ImportError:
        print("Install: pip install transformers peft accelerate")
        return

    print(f"Loading base model: {base_model_name}")
    model = AutoModelForCausalLM.from_pretrained(base_model_name)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    print(f"Loading LoRA adapter from: {adapter_path}")
    model = PeftModel.from_pretrained(model, adapter_path)

    print("Merging adapter into base model weights...")
    model = model.merge_and_unload()  # adapter is now baked in

    print(f"Saving merged model to: {output_path}")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("Done!")


def test_model(model_path: str, question: str):
    """Test the merged model on a legal question."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    except ImportError:
        print("Install: pip install transformers")
        return

    print(f"\nLoading merged model from: {model_path}")
    pipe = pipeline(
        "text-generation",
        model=model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    messages = [
        {"role": "system", "content": "You are a Philippine legal assistant. Cite specific articles."},
        {"role": "user", "content": question},
    ]

    print(f"Question: {question}\n")
    output = pipe(messages, max_new_tokens=300, temperature=0.1)
    print(f"Answer: {output[0]['generated_text'][-1]['content']}")


def convert_to_gguf_instructions(merged_model_path: str):
    """Print instructions for converting the merged model to GGUF for Ollama."""
    print(f"""
=== Convert to GGUF for Ollama (CPU inference) ===

1. Clone llama.cpp:
   git clone https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp && pip install -r requirements/requirements-convert_hf_to_gguf.txt

2. Convert to GGUF (Q4_K_M quantization):
   python convert_hf_to_gguf.py {merged_model_path} --outtype q4_k_m --outfile legal-model.gguf

3. Create an Ollama Modelfile:
   cat > Modelfile << 'EOF'
   FROM ./legal-model.gguf
   SYSTEM "You are a Philippine legal assistant specializing in the 1987 Constitution and Civil Code."
   PARAMETER temperature 0.1
   PARAMETER num_ctx 4096
   EOF

4. Register with Ollama:
   ollama create legal-model -f Modelfile

5. Test:
   ollama run legal-model "What are the rights of an accused person?"

6. Update config.py:
   LLM_MODEL = "legal-model"
""")


if __name__ == "__main__":
    ADAPTER_PATH = "./legal-lora-output"
    MERGED_PATH = "./legal-model-merged"
    BASE_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

    if not Path(ADAPTER_PATH).exists():
        print(f"No adapter found at {ADAPTER_PATH}")
        print("Run 03_qlora_training.py in Google Colab first.")
        print("\nTo simulate what this script does:")
        print("  1. Train in Colab, download the adapter")
        print("  2. Place it at ./legal-lora-output/")
        print("  3. Run this script again")
    else:
        merge_adapter(BASE_MODEL, ADAPTER_PATH, MERGED_PATH)
        test_model(MERGED_PATH, "What are the rights of an accused person?")
        convert_to_gguf_instructions(MERGED_PATH)
