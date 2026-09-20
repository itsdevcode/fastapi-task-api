from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str|None = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
    
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None

class TaskDetailResponse(BaseModel):
    message:str
    task:TaskResponse

class TaskListResponse(BaseModel):
    message: str
    page: int
    limit: int
    total: int
    offset: int
    tasks: list[TaskResponse]