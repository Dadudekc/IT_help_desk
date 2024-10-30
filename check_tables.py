import sqlite3
from config.config import DB_PATH

def check_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:", tables)

        # Check columns in 'tickets' table if it exists
        cursor.execute("PRAGMA table_info(tickets);")
        columns = cursor.fetchall()
        print("Tickets table schema:", columns)

check_tables()
