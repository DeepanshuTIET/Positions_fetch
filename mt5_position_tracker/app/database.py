import sqlite3
from pathlib import Path

# Get the database file path
DB_PATH = Path(__file__).parent.parent / "positions.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initialize the database with required tables"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                volume REAL NOT NULL,
                price REAL NOT NULL,
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
