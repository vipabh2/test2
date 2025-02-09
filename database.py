from sqlalchemy.orm import Session
from models import SessionLocal, AllowedUser

# إضافة مستخدم إلى قاعدة البيانات
def add_user_to_db(user_id: int):
    db = SessionLocal()
    try:
        user = AllowedUser(user_id=user_id)
        db.add(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# التحقق من وجود مستخدم في قاعدة البيانات
def is_user_allowed(user_id: int) -> bool:
    db = SessionLocal()
    try:
        user = db.query(AllowedUser).filter(AllowedUser.user_id == user_id).first()
        return user is not None
    finally:
        db.close()
