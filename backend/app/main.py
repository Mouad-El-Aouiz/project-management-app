from fastapi import FastAPI

from app.database.base import Base
from app.database.session import engine
from app.routers import user, project, task, auth
from app.core.config import settings

app = FastAPI(title="Project Management API")

# Add API versioning prefix
api_v1_prefix = "/api/v1"

@app.on_event("startup")
def on_startup():
    # Sécurité minimale : refuser de démarrer avec une clé par défaut
    if settings.SECRET_KEY == "CHANGE_ME":
        raise RuntimeError("SECRET_KEY must be set in .env (do not use CHANGE_ME).")


app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(user.router, prefix=api_v1_prefix)
app.include_router(project.router, prefix=api_v1_prefix)
app.include_router(task.router, prefix=api_v1_prefix)