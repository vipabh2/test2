from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تهيئة قاعدة البيانات
DATABASE_URL = "sqlite:///allowed_users.db"  # يمكن تغييرها إلى MySQL أو PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# تعريف جدول المستخدمين المسموح لهم
class AllowedUser(Base):
    __tablename__ = "allowed_users"
    user_id = Column(Integer, primary_key=True)

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)
