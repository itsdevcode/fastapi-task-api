from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
class TaskUpdate(BaseModel):
    title: str = Optional[None]
    description: str = Optional[None]
    is_completed: str = Optional[None]