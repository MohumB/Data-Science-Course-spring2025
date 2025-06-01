import pandas as pd
from database_connection import get_connection
from config import RAW_DATA_CSV

def load_data():
    conn = get_connection()
    
    query = "SELECT * FROM book_lines"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Loaded {len(df)} rows from the database.")
    df.to_csv(RAW_DATA_CSV, index=False)

if __name__ == "__main__":
    load_data()
