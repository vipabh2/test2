import sqlite3

# الاتصال بقاعدة البيانات
def connect_db():
    return sqlite3.connect('database.db')

def save_notification_group(group_id, notification_group_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notification_groups (
                        group_id INTEGER PRIMARY KEY, 
                        notification_group_id INTEGER)''')
    cursor.execute('INSERT OR REPLACE INTO notification_groups (group_id, notification_group_id) VALUES (?, ?)', (group_id, notification_group_id))
    conn.commit()
    conn.close()

def get_notification_group(group_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT notification_group_id FROM notification_groups WHERE group_id = ?', (group_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def delete_notification_group(group_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notification_groups WHERE group_id = ?', (group_id,))
    conn.commit()
    conn.close()

def approve_user(group_id, user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS allowed_users (
                        group_id INTEGER, 
                        user_id INTEGER,
                        PRIMARY KEY (group_id, user_id))''')
    cursor.execute('INSERT OR REPLACE INTO allowed_users (group_id, user_id) VALUES (?, ?)', (group_id, user_id))
    conn.commit()
    conn.close()

def remove_approval(group_id, user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM allowed_users WHERE group_id = ? AND user_id = ?', (group_id, user_id))
    conn.commit()
    conn.close()

def is_user_approved(group_id, user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM allowed_users WHERE group_id = ? AND user_id = ?', (group_id, user_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
