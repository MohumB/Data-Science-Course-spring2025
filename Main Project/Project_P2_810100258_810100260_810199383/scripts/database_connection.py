import sqlite3
import os
from config import DATABASE

def get_connection():
    if not os.path.exists(DATABASE):
        raise Exception(f"Database at {DATABASE} does not exist!")
    conn = sqlite3.connect(DATABASE)
    return conn


