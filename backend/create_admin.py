from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

EMAIL = "admin@test.com"
PASSWORD = "Password123!"
ROLE = "admin"

def main():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == EMAIL).first()
        if existing:
            existing.role = ROLE
            existing.hashed_password = hash_password(PASSWORD)
            db.commit()
            print("Admin updated:", EMAIL)
            return

        user = User(
            email=EMAIL,
            role=ROLE,
            hashed_password=hash_password(PASSWORD),
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Admin created:", EMAIL)
    finally:
        db.close()

if __name__ == "__main__":
    main()
