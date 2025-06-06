from setuptools import setup, find_packages


setup(
    name="llama-finetuner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch==2.6.0+cu124",
        "torchvision==0.21.0+cu124",
        "torchaudio==2.6.0+cu124",
        "unsloth @ git+https://github.com/unslothai/unsloth.git",
        "protobuf>=5.26.1",
        "trl==0.8.6",
        "transformers",
        "datasets",
        "peft",
        "huggingface-hub",
        "accelerate",

        # tested with below versions and failed on xformer and torch conflict
        # "torch==2.7.1",
        # "unsloth @ git+https://github.com/unslothai/unsloth.git",
        # "protobuf<4.0.0",
        # "trl==0.8.6",
        # "transformers",
        # "datasets>=3.4.1",
        # "peft",
        # "huggingface-hub",
        # "accelerate",
        # "fsspec[http]<=2025.3.0,>=2023.1.0",
        # "triton==3.3.1",
        # "xformers==0.0.30"
    ],
    python_requires=">=3.8",
)

def verify_installation():
    import torch
    assert torch.cuda.is_available(), "CUDA not available!"
    
    try:
        from unsloth import FastLanguageModel
        print("✓ Installation verified")
    except ImportError as e:
        raise RuntimeError("Installation failed") from e

if __name__ == "__main__":
    verify_installation()