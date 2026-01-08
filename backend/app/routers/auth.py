from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.core.config import settings
from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Compatible Swagger Authorize (OAuth2 password flow):
    - username = email
    - password = password
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if hasattr(user, "is_active") and not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    token = create_access_token(
        subject=str(user.id),
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Inscription publique sécurisée:
    - le client NE PEUT PAS choisir son rôle
    - role est forcé à 'member'
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    db_user = User(
        email=payload.email,
        role="member",  # FIX SECURITE: toujours member à l'inscription publique
        hashed_password=hash_password(payload.password),
    )

    if hasattr(db_user, "full_name") and getattr(payload, "full_name", None) is not None:
        db_user.full_name = payload.full_name

    if hasattr(db_user, "is_active") and getattr(db_user, "is_active", None) is None:
        db_user.is_active = True

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
