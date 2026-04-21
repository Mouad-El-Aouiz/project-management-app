import os
import sys

from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

# Fixed role for this script (admin bootstrap)
ROLE = "admin"

def main():
    # On cherche la variable d'environnement, sinon on utilise la valeur par défaut
    admin_email = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "mouad1234567")

    if not admin_email or not admin_email.strip():
        print("ERROR: ADMIN_EMAIL is not set.")
        print("Example (Linux/macOS): export ADMIN_EMAIL='admin@exemple.com'")
        print("Example (PowerShell):  $env:ADMIN_EMAIL='admin@exemple.com'")
        sys.exit(1)

    if not admin_password or not admin_password.strip():
        print("ERROR: ADMIN_PASSWORD is not set.")
        print("Example (Linux/macOS): export ADMIN_PASSWORD='MotDePasseLongEtFort123!'")
        print("Example (PowerShell):  $env:ADMIN_PASSWORD='MotDePasseLongEtFort123!'")
        sys.exit(1)

    if len(admin_password) < 12:
        print("ERROR: ADMIN_PASSWORD is too short (minimum 12 characters).")
        sys.exit(1)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == admin_email).first()
        if existing:
            existing.role = ROLE
            existing.hashed_password = hash_password(admin_password)
            existing.is_active = True
            db.commit()
            print("Admin updated:", admin_email)
            return

        user = User(
            email=admin_email,
            role=ROLE,
            hashed_password=hash_password(admin_password),
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Admin created:", admin_email)
    finally:
        db.close()

if __name__ == "__main__":
    main()
