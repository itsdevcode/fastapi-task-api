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
    return TaskDetailResponse(
        message= "Task created successfully",
        task= TaskResponse(**task_data)
    )

@app.get("/tasks")
def get_tasks():
    return TaskListResponse(
        message= "Task list fetched successfully",
        tasks= [TaskResponse(**task) for task in tasks]
    )


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = find_task_or_404(task_id, tasks)
    return TaskDetailResponse(
        message= "Task fetched successfully",
        task= TaskResponse(**task)
    )
   

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    task_data = find_task_or_404(task_id, tasks)
    task_data.update(**task.model_dump(exclude_unset=True))
    task_data["updated_at"] = datetime.now()
    return TaskDetailResponse(
        message= "Task created successfully",
        task= TaskResponse(**task_data)
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    task = find_task_or_404(task_id, tasks)
    tasks.remove(task)
    return TaskDetailResponse(
        message= "Task deleted successfully",
        task= TaskResponse(**task)
    )