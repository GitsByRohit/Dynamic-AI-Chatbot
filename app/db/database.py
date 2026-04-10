import sqlite3
import os
from pathlib import Path

# Database file location
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "chatbot.db"


def get_db_connection():
    """
    Create a thread-safe SQLite database connection.
    Used by all DB query modules.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str, params: tuple = (), fetchone=False, fetchall=False):
    """
    Generic query executor.

    Args:
        query (str): SQL query
        params (tuple): parameters for query
        fetchone (bool): return single row
        fetchall (bool): return all rows

    Returns:
        query result if requested
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()

        if fetchone:
            return cursor.fetchone()

        if fetchall:
            return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def init_database():
    """
    Ensure database directory exists.
    Called during startup.
    """
    os.makedirs(BASE_DIR / "data", exist_ok=True)

    if not os.path.exists(DB_PATH):
        open(DB_PATH, "w").close()