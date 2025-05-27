import sqlite3
import pandas as pd
import os
import sys
def import_sentences_to_db(csv_path, db_path):
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            sentence TEXT
        )
    ''')

    # Insert data
    for _, row in df.iterrows():
        c.execute("INSERT INTO sentences (story_id, sentence) VALUES (?, ?)",
                  (row['story_id'], row['sentence']))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    csv_path = sys.argv[1]
    db_path = sys.argv[2]
    import_sentences_to_db(csv_path, db_path)
