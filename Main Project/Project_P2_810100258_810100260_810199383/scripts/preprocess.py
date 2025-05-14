import pandas as pd
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import sys
nltk.download('punkt')

def preprocess_data(df):
    df['text'] = df['text'].str.lower()
    df['token_text'] = df['token_text'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    df['token_text'] = df['token_text'].apply(lambda x: word_tokenize(x))
    return df

if __name__ == "__main__":
    text_csv = sys.argv[1]
    cleaned_text_csv = sys.argv[2]
    df = pd.read_csv(text_csv)  
    df_clean = preprocess_data(df)
    df_clean.to_csv(cleaned_text_csv, index=False)