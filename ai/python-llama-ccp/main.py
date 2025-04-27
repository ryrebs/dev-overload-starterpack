from llama_cpp import Llama


## Using vulkan for GPU processing
## Install cmake libvulkan-dev glslc vulkan-tools (optional)
## Install python deps: CMAKE_ARGS="-DGGML_VULKAN=on" pipenv run python -m pip install llama-cpp-python
## You should see: "load_tensors: layer  29 assigned to device Vulkan0" at command line.
llm = Llama(
    model_path="./models/gemma-3-12b-it-q4_0.gguf",  # or whatever your quantized GGUF file is
    n_ctx=4096,  # Max context your GPU/CPU can handle
    n_gpu_layers=25,  # Use ALL (-1) or set N layers on GPU (if supported by AMD setup) and the system has enough RAM
    seed=42,  # Consistent output
    n_threads=8,  # For CPU-based token processing, balance with your cores
    n_batch=512,  # Tune up/down if memory errors
    top_p=0.9,
    top_k=50,
    temperature=0.7,
    repeat_penalty=1.1,
    chat_format="gemma",
)


output = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You a software engineer that creates reliable, efficient safe code, adheres to SOLID principlies, and creates SPACE grade code or software",
        },
        {
            "role": "user",
            "content": "Write a python code that creates tells if today is biweekly payroll schedule.",
        },
    ]
)

print(output)
