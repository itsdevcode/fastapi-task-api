from schemas.task import TaskCreate, TaskUpdate
from fastapi import Depends, HTTPException, APIRouter
from db.database import get_db
import services.task as service
from sqlalchemy.orm import Session


task_router = APIRouter()

@task_router.get("/tasks")
def all(db:Session = Depends(get_db)):
    return service.all(db)

@task_router.post("/tasks")
def create(task:TaskCreate, db:Session = Depends(get_db)):
    return service.create(task, db)

@task_router.get("/tasks/{task_id}")
def get(task_id:str, db:Session = Depends(get_db)):
    task = service.get(task_id, db)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return task

@task_router.patch("/tasks/{task_id}")
def update(task_id: str, task:TaskUpdate, db:Session = Depends(get_db)):
    updated_task = service.update(task_id, task, db)
    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return updated_task


@task_router.delete("/tasks/{task_id}")
def delete(task_id:str, db:Session = Depends(get_db)):
    deleted_task =  service.delete(task_id, db)
    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task is not found"
        )
    return deleted_task
