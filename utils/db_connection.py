import sqlite3
import os

DB_PATH = "cricbuzz.db"
SCHEMA_PATH = os.path.join("sql", "schema.sql")
SEED_PATH = os.path.join("sql", "seed_data.sql")

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Reads schema.sql and creates all tables and indexes."""
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at: {SCHEMA_PATH}")
        
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database schema initialized successfully!")

def seed_db():
    """Populates the database with initial sample cricket records."""
    if not os.path.exists(SEED_PATH):
        raise FileNotFoundError(f"Seed file not found at: {SEED_PATH}")

    with open(SEED_PATH, "r") as f:
        seed_sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(seed_sql)
    conn.commit()
    conn.close()
    print("Seed data loaded successfully!")

if __name__ == "__main__":
    init_db()
    seed_db()