import sqlite3

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        importance INTEGER,
        urgency INTEGER,
        duration INTEGER,
        weight INTEGER,
        scheduled_time TEXT,
        fixed INTEGER DEFAULT 0,
        days_of_week TEXT,
        done INTEGER DEFAULT 0,
        notification_sent INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()