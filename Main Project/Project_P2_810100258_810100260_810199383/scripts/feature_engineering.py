import pandas as pd
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def feature_engineering(df):
    
    df['line_length'] = df['clean_line'].apply(len)

    vectorizer = TfidfVectorizer(max_features=100)
    # tfidf_matrix = vectorizer.fit_transform(df['clean_line'])

    # with open("E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/tfidf_vectorizer.pkl", "wb") as f:
    #     pickle.dump(vectorizer, f)
    # with open("E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/tfidf_features.pkl", "wb") as f:
    #     pickle.dump(tfidf_matrix, f)

    return df

if __name__ == "__main__":
    preproc_path = "E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/preprocessed_data.csv"
    df = pd.read_csv(preproc_path)
    df =feature_engineering(df)
    df.to_csv("E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/feature_engineered_data.csv", index=False)
    print("Feature engineering completed and saved.")

