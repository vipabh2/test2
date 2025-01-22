import sqlite3
import os

# قاعدة بيانات SQLite
DATABASE_URL = os.getenv('DATABASE_URL')

# إنشاء اتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # لتسهيل الوصول إلى البيانات عبر الأعمدة
    return conn

# إنشاء الجداول إذا لم تكن موجودة
def recreate_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # جدول الأدمن
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER,
        group_id INTEGER,
        PRIMARY KEY (user_id, group_id)
    )
    ''')

    # جدول الموافقات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS approvals (
        user_id INTEGER PRIMARY KEY
    )
    ''')

    # جدول المجموعات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        group_name TEXT
    )
    ''')

    conn.commit()
    conn.close()

recreate_tables()

# إضافة أدمن إلى مجموعة معينة
def add_admin(user_id, group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO admins (user_id, group_id) VALUES (?, ?)', (user_id, group_id))
    conn.commit()
    conn.close()

# إزالة أدمن من مجموعة معينة
def remove_admin(user_id, group_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if group_id:
        # إزالة الأدمن من مجموعة معينة
        cursor.execute('DELETE FROM admins WHERE user_id = ? AND group_id = ?', (user_id, group_id))
    else:
        # إزالة الأدمن من جميع المجموعات
        cursor.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# التحقق من كون المستخدم أدمن في مجموعة معينة
def is_admin(user_id, group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM admins WHERE user_id = ? AND group_id = ?', (user_id, group_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# إضافة مستخدم مُوافق عليه إلى مجموعة معينة
def add_approved_user(user_id, group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # تحقق إذا لم يكن المستخدم مضافًا بالفعل للمجموعة
    cursor.execute('SELECT 1 FROM approvals WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO approvals (user_id) VALUES (?)', (user_id,))
        conn.commit()
    conn.close()

# إزالة مستخدم مُوافق عليه من مجموعة معينة
def remove_approved_user(user_id, group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM approvals WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# الحصول على جميع المستخدمين المصرح لهم
def get_approved_users(group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM approvals')
    users = cursor.fetchall()
    conn.close()
    return users

# إضافة مجموعة إلى قاعدة البيانات
def add_group(group_id, group_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO groups (group_id, group_name) VALUES (?, ?)', (group_id, group_name))
    conn.commit()
    conn.close()
