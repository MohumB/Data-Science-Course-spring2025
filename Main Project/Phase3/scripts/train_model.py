#!/usr/bin/env python3
import argparse
import logging
import os
import torch

from unsloth import FastLanguageModel  
from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import warnings


warnings.filterwarnings("ignore", message=".*Unsloth should be imported before transformers.*")

def check_gpu():
    """Verify CUDA-capable GPU is available"""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU not detected. Unsloth requires:\n"
            "1. In Colab: Runtime -> Change runtime type -> GPU\n"
            "2. Locally: NVIDIA GPU with CUDA 12.x installed"
        )
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")

def initialize_model(model_name: str = "meta-llama/Llama-3.2-3B-Instruct"):
    """Initialize model with Unsloth optimizations"""
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=1024,
        load_in_8bit=True,
        load_in_4bit=False
    )
    
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def tokenize_data(dataset: Dataset, tokenizer):
    """Tokenize dataset with padding"""
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
    return dataset.map(tokenize_function, batched=True, remove_columns=["text"])

def train(model, tokenizer, dataset, output_dir: str):
    """Training loop with fallback"""
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=2,
        learning_rate=3e-4,
        fp16=True,
        save_steps=500,
        save_total_limit=2,
        logging_steps=10,
        eval_strategy="no",
        warmup_steps=100,
        report_to=[],
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=512,
        tokenizer=tokenizer,
        packing=False
    )

    try:
        trainer.train()
    except Exception as e:
        logging.warning(f"Training error: {e}")
        model.gradient_checkpointing_disable()
        trainer.train()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", required=True, help="Path to preprocessed dataset")
    parser.add_argument("--model_name", default="meta-llama/Llama-3.2-3B-Instruct")
    parser.add_argument("--output_dir", default="./llama-lora-finetuned")
    args = parser.parse_args()

    
    check_gpu()
    logging.basicConfig(level=logging.INFO)
    
    
    dataset = Dataset.load_from_disk(args.dataset_path)
    
    
    model, tokenizer = initialize_model(args.model_name)
    train(model, tokenizer, dataset, args.output_dir)
    
    
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    logging.info(f"Training complete. Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()