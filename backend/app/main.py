from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine

from app.routers import user, project, task, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Management API")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(task.router)
