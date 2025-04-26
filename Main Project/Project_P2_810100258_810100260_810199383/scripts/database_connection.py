import sqlite3
import os

def connect_db(db_path="../database/dataset.db"):
    if not os.path.exists(db_path):
        raise Exception(f"Database at {db_path} does not exist!")
    conn = sqlite3.connect(db_path)
    return conn

def close_connection(conn):
    if conn:
        conn.close()

