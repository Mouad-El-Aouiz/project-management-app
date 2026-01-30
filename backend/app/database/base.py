from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings


DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

Base = declarative_base()
