from schemas.task import TaskCreate, TaskUpdate,TaskDetailResponse, TaskListResponse
from fastapi import Depends, HTTPException, APIRouter, Query
from db.database import get_db
import services.task as service
from sqlalchemy.orm import Session
from utilis.user import get_current_user
from schemas.user import UserResponse
from enums.task import TaskShortField, SortOrder
task_router = APIRouter()

@task_router.get("/tasks", response_model=TaskListResponse)
def all(
    db:Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user), 
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    is_completed: bool | None = None,
    sort_by: TaskShortField = Query(default=TaskShortField.created_at),
    sort_order: SortOrder = Query(default=SortOrder.desc),
    search: str | None = None
):
    result = service.all(db, current_user.id, page, limit,is_completed, sort_by, sort_order, search)
    return {
        "message":"Tasks fetched successfully!",
        "page": result["page"],
        "limit": result["limit"],
        "offset": result["offset"],
        "total": result["total"],
        "tasks": result["tasks"]
    }

@task_router.post("/tasks")
def create(task:TaskCreate, db:Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return service.create(task, current_user.id, db)

@task_router.get("/tasks/{task_id}", response_model=TaskDetailResponse)
def get(task_id:str, db:Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    task = service.get(task_id, db, current_user.id)
    print(task.user.name)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return {"message":"Task is fetched successfully!","task":task}

@task_router.patch("/tasks/{task_id}", response_model=TaskDetailResponse)
def update(task_id: str, task:TaskUpdate, db:Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    updated_task = service.update(task_id, task, db, current_user.id)
    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return {"message":"Task is updated successfully!","task":updated_task}


@task_router.delete("/tasks/{task_id}")
def delete(task_id:str, db:Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    deleted_task =  service.delete(task_id, db, current_user.id)
    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return deleted_task
