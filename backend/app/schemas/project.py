from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)

class ProjectCreate(ProjectBase):
    # owner_id vient du token (current_user.id), donc pas ici
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)

class ProjectRead(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
