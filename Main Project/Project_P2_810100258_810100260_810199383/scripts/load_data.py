import pandas as pd
from database_connection import get_connection
from config import RAW_DATA_CSV

def load_data(db_path):
    conn = get_connection(db_path)
    
    query = "SELECT * FROM book_lines"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Loaded {len(df)} rows from the database.")
    df.to_csv(RAW_DATA_CSV, index=False)

if __name__ == "__main__":
    db_path="E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Project_P2_810100258_810100260_810199383/database/dataset.db"
    load_data(db_path)
