import sqlite3

def save_notification_group(group_id, notification_group_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notification_groups
                      (group_id INTEGER PRIMARY KEY, notification_group_id INTEGER)''')
    cursor.execute('INSERT OR REPLACE INTO notification_groups (group_id, notification_group_id) VALUES (?, ?)', 
                   (group_id, notification_group_id))
    conn.commit()
    conn.close()

def get_notification_group(group_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT notification_group_id FROM notification_groups WHERE group_id = ?', (group_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def delete_notification_group(group_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notification_groups WHERE group_id = ?', (group_id,))
    conn.commit()
    conn.close()
