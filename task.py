from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid
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
    
    