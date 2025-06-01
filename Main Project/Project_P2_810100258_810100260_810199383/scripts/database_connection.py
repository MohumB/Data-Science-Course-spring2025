import sqlite3
import os

def get_connection(db_path="E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Project_P2_810100258_810100260_810199383/database/dataset.db"):
    if not os.path.exists(db_path):
        raise Exception(f"Database at {db_path} does not exist!")
    conn = sqlite3.connect(db_path)
    return conn


