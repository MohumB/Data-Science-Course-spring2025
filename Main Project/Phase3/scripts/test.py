# evaluate.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import logging

def evaluate(model_path: str, dataset_path: str):
    """Evaluate a model's performance using perplexity."""
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load the trained model and tokenizer
    logger.info("Loading model and tokenizer for evaluation...")
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Load dataset for evaluation
    logger.info("Loading dataset for evaluation...")
    dataset = load_dataset('text', data_files=dataset_path, split='train')

    # Calculate perplexity
    model.eval()
    total_loss = 0
    total_tokens = 0
    for batch in dataset:
        inputs = tokenizer(batch['text'], return_tensors='pt', truncation=True, padding=True)
        labels = inputs.input_ids
        inputs = {key: value.to(model.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss

        total_loss += loss.item() * labels.size(0)
        total_tokens += labels.size(0)

    perplexity = torch.exp(torch.tensor(total_loss / total_tokens))
    logger.info(f"Perplexity: {perplexity.item()}")

    return perplexity.item()

if __name__ == "__main__":
    # Example usage when running directly
    evaluate("path_to_trained_model", "path_to_test_dataset.txt")
