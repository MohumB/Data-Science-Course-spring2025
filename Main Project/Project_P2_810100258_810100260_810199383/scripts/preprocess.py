import pandas as pd
import re

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s,.!?;:\'-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def main():
    raw_path = "E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/raw_data.csv"
    df = pd.read_csv(raw_path)
    df['clean_line'] = df['line'].apply(preprocess_text)

   
    df = df[df['clean_line'] != '']

    print(f"Preprocessed {len(df)} lines.")
    df.to_csv("E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/preprocessed_data.csv")

if __name__ == "__main__":
    main()