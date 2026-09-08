from fastapi import FastAPI
from task import TaskCreate, TaskResponse
from datetime import datetime
import uuid
app = FastAPI(
    title="Tasks API",
    description="Tasks API",
    version="0.1.0",
)

tasks = []

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/tasks")
def create_task(task: TaskCreate):
    task_data={
        **task.model_dump(),
        "id": str(uuid.uuid4()),
        "is_completed": False,
        "created_at": datetime.now(),
        "updated_at": None
    }
    tasks.append(task_data)
    return {
        "message": "Task created successfully",
        "task": TaskResponse(**task_data)
        }

@app.get("/tasks")
def get_tasks():
    return {
        "message": "Task list fetched successfully",
        "tasks": [TaskResponse(**task.dict()) for task in tasks]
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task_detail = []
    for task in tasks:
        if task.id == task_id:
            task_detail.append(TaskResponse(**task.dict()))
            break
    
    return {
        "message": "Task fetched successfully" if len(task_detail) > 0 else "Task not found",
        "task": task_detail
    }
