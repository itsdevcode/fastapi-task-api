from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime | None = None
    
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None