from fastapi import FastAPI
from task import TaskCreate, TaskResponse
app = FastAPI(
    title="Tasks API",
    description="Tasks API",
    version="0.1.0",
)

tasks = []

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/task")
def create_task(task: TaskCreate):
    tasks.append(task)
    return {
    "message": "Task created",
    "task": TaskResponse(**task.dict())
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
        "message": "Task found",
        "task": task_detail
    }
