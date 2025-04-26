import pandas as pd
from preprocess import preprocess_data
import pickle

def feature_engineering(df):
    df['next_token'] = df['token_text'].shift(-1)  
    df.dropna(inplace=True)  

    df['bigram'] = df['token_text'] + " " + df['next_token']
    
    df.to_pickle('processed_data.pkl') 
    
    return df

if __name__ == "__main__":
    df = pd.read_pickle('../../Phase 1/CSV/cleaned_text.csv')  
    df_fe = feature_engineering(df)
    
