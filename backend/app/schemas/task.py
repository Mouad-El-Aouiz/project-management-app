from pydantic import BaseModel, Field
from typing import Optional, Literal

TaskStatus = Literal["todo", "doing", "done"]

class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    status: TaskStatus = "todo"

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
    # IMPORTANT: on évite de changer project_id via patch (mauvaise pratique)
    # project_id: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True
