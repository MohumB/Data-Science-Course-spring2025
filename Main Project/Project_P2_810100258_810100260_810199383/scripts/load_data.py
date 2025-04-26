import pandas as pd
from database_connection import connect_db

def load_data():
    db_path="../database/dataset.db"
    conn = connect_db(db_path)
    
    # should change it later
    query = "SELECT token_index, token_text FROM tokens ORDER BY doc_id, token_index"
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

if __name__ == "__main__":
    df = load_data()
    df.to_csv("../../Phase 1/CSV/text.csv", index=False)