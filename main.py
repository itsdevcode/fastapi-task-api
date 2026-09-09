from fastapi import FastAPI,HTTPException
from model import TaskCreate, TaskResponse, TaskUpdate, TaskDetailResponse, TaskListResponse
from datetime import datetime
import uuid
from helper import find_task_or_404
app = FastAPI(
    title="Tasks API",
    description="Tasks API",
    version="0.1.0",
)

tasks = []

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskDetailResponse)
def create_task(task: TaskCreate):
    task_data={
        **task.model_dump(),
        "id": str(uuid.uuid4()),
        "is_completed": False,
        "created_at": datetime.now(),
        "updated_at": None
    }
    tasks.append(task_data)
    return {"message": "Task created successfully","task": task_data}

@app.get("/tasks", response_model=TaskListResponse)
def get_tasks():
    return {"message": "Task list fetched successfully","tasks": tasks}

@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: str):
    task = find_task_or_404(task_id, tasks)

    return {"message": "Task fetched successfully","task": task}


@app.patch("/tasks/{task_id}", response_model=TaskDetailResponse)
def update_task(task_id: str, task: TaskUpdate):
    task_data = find_task_or_404(task_id, tasks)

    task_data.update(
        **task.model_dump(exclude_unset=True)
    )

    task_data["updated_at"] = datetime.now()

    return {"message": "Task updated successfully","task": task_data}


@app.delete("/tasks/{task_id}", response_model=TaskDetailResponse)
def delete_task(task_id: str):
    task = find_task_or_404(task_id, tasks)

    tasks.remove(task)

    return {"message": "Task deleted successfully","task": task}