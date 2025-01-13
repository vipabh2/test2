import sqlite3

def initialize_database():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_text TEXT NOT NULL,
            target_user TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_message(message_text, target_user):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (message_text, target_user)
        VALUES (?, ?)
    """, (message_text, target_user))
    conn.commit()
    conn.close()

initialize_database()
