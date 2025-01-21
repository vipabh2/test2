from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import sqlite3
import os

# تحديد رابط قاعدة البيانات من متغير البيئة
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

# اختيار طريقة الاتصال بناءً على نوع قاعدة البيانات
if DATABASE_URL.startswith('postgresql://'):
    # الاتصال بقاعدة بيانات PostgreSQL باستخدام SQLAlchemy
    engine = create_engine(DATABASE_URL, echo=False)
    BASE = declarative_base()
    SessionLocal = sessionmaker(bind=engine)
    SESSION = SessionLocal()

elif DATABASE_URL.startswith('sqlite:///'):
    # الاتصال بقاعدة بيانات SQLite باستخدام sqlite3
    db_path = DATABASE_URL.replace('sqlite:///', '')  # إزالة 'sqlite:///' للحصول على المسار الفعلي
    # التأكد من وجود المجلد لقاعدة بيانات SQLite
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # إعداد الاتصال مع قاعدة بيانات SQLite
    def get_connection():
        conn = sqlite3.connect(db_path)
        return conn

    # إنشاء جدول المسموح لهم بالتعديلات في SQLite
    def create_table():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS approvals (
            user_id INTEGER PRIMARY KEY
        )
        ''')
        conn.commit()
        conn.close()

    # إضافة مستخدم إلى قائمة المسموح لهم باستخدام SQLite
    def add_approved_user(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO approvals (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()

    # إزالة مستخدم من قائمة المسموح لهم باستخدام SQLite
    def remove_approved_user(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM approvals WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    # استرجاع قائمة المستخدمين المسموح لهم باستخدام SQLite
    def get_approved_users():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM approvals')
        approved_users = cursor.fetchall()
        conn.close()
        return approved_users

else:
    raise ValueError("رابط قاعدة البيانات غير صالح أو غير مدعوم. تأكد من أنه PostgreSQL أو SQLite.")
