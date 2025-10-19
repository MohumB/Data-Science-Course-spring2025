from datasets import Dataset
import logging
from pathlib import Path

def load_text_data(file_path: str, max_lines: int = None) -> Dataset:
    try:
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            
            if max_lines:
                lines = lines[:max_lines]
                
        
        return Dataset.from_dict({"text": lines})
        
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        raise

if __name__ == "__main__":
    
    dataset = load_text_data(
        file_path="/content/Data-Science-Course-spring2025/Main Project/Phase3/David_Copperfield.txt"
    )
    
    print(f"Loaded dataset with {len(dataset)} samples")

    print(dataset[0])  
    output_dir = "/content/Data-Science-Course-spring2025/Main Project/Phase3"  
    dataset.save_to_disk(output_dir)
    print(f"Dataset saved to {output_dir}")