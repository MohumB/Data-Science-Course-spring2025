import pandas as pd
import re
from config import RAW_DATA_CSV,PREPROCESSED_CSV
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s,.!?;:\'-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def main():
    df = pd.read_csv(RAW_DATA_CSV)
    df['clean_line'] = df['line'].apply(preprocess_text)

   
    df = df[df['clean_line'] != '']

    print(f"Preprocessed {len(df)} lines.")
    df.to_csv(PREPROCESSED_CSV)

if __name__ == "__main__":
    main()