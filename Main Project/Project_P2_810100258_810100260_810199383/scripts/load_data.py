import pandas as pd
from database_connection import connect_db
import sys

def load_data(db_path):
    conn = connect_db(db_path)
    
    query = "SELECT text FROM text"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

if __name__ == "__main__":
    db_path = sys.argv[1]
    text_csv = sys.argv[2]
    df = load_data(db_path)
    df.to_csv(text_csv, index=False)