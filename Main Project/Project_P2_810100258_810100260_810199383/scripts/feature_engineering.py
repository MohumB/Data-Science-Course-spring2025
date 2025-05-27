import pandas as pd
from nltk.tokenize import sent_tokenize
import sys
def feature_engineering(df):
<<<<<<< Updated upstream
    sentences = []
=======
    df['next_token'] = df['token_text'].shift(-1)  
    df.dropna(inplace = True)  
>>>>>>> Stashed changes

    for idx, row in df.iterrows():
        story = row['text']
        for sentence in sent_tokenize(story):
            sentences.append({'story_id': idx, 'sentence': sentence})

    return pd.DataFrame(sentences)

if __name__ == "__main__":
    cleaned_text_csv = sys.argv[1]
    sentences_csv = sys.argv[2]
    
    df = pd.read_csv(cleaned_text_csv)  
    df_sentences = feature_engineering(df)
    df_sentences.to_csv(sentences_csv, index=False)
