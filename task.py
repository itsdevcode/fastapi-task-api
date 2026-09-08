from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
class TaskCreate(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    is_completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    