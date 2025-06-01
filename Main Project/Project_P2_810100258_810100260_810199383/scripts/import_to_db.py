import pandas as pd
from database_connection import get_connection


def import_text_to_db(text_file_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line TEXT NOT NULL
        )
    ''')

    with open(text_file_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]  

    cursor.executemany('INSERT INTO book_lines (line) VALUES (?)', [(line,) for line in lines])

    conn.commit()
    conn.close()

    print(f"Imported {len(lines)} lines into the database.")

if __name__ == "__main__":
    text_path = "E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets/David_Copperfield.txt"
    import_text_to_db(text_path)