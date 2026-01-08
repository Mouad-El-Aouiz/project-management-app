from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_role
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))]
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Création user par admin (ex: créer un manager).
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    db_user = User(
        email=payload.email,
        role=getattr(payload, "role", "member") or "member",
        hashed_password=hash_password(payload.password),
    )

    if hasattr(db_user, "full_name") and getattr(payload, "full_name", None) is not None:
        db_user.full_name = payload.full_name

    if hasattr(db_user, "is_active") and getattr(db_user, "is_active", None) is None:
        db_user.is_active = True

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.model_validate(db_user)


@router.get(
    "",
    response_model=list[UserRead],
    dependencies=[Depends(require_role("admin"))]
)
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserRead.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_role("admin"))]
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_role("admin"))]
)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if getattr(payload, "email", None) is not None:
        user.email = payload.email
    if getattr(payload, "role", None) is not None:
        user.role = payload.role
    if hasattr(user, "full_name") and getattr(payload, "full_name", None) is not None:
        user.full_name = payload.full_name
    if hasattr(user, "is_active") and getattr(payload, "is_active", None) is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None
