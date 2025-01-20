import sqlite3

# إنشاء اتصال بقاعدة البيانات
conn = sqlite3.connect("groups.db")
cursor = conn.cursor()

# إنشاء جدول لتخزين معرفات المجموعات وكروبات التبليغ
cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    group_id INTEGER PRIMARY KEY,
    notification_group_id INTEGER
)
""")
conn.commit()

# دالة لحفظ معرف كروب التبليغ
def save_notification_group(group_id, notification_group_id):
    cursor.execute("""
    INSERT OR REPLACE INTO groups (group_id, notification_group_id)
    VALUES (?, ?)
    """, (group_id, notification_group_id))
    conn.commit()

# دالة لاسترجاع معرف كروب التبليغ
def get_notification_group(group_id):
    cursor.execute("SELECT notification_group_id FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()
    return result[0] if result else None
