from fastapi import FastAPI,HTTPException
from task import TaskCreate, TaskResponse, TaskUpdate
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
        "tasks": [TaskResponse(**task) for task in tasks]
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task_data = next((task for task in tasks if task["id"] == task_id), None)
    if task_data is not None:
        return {
            "message": "Task fetched successfully",
            "task": TaskResponse(**task_data)
        }
    raise HTTPException(
        status_code= 404,
        detail="Task not found",
    )

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    task_data = next((task for task in tasks if task["id"] == task_id), None)
    if task_data is not None:
        task_data.update(**task.model_dump(exclude_unset=True))
        task_data["updated_at"] = datetime.now()
        return {
            "message": "Task updated successfully.",
            "task": TaskResponse(**task_data)
        }

    raise HTTPException(
        status_code= 404,
        detail="Task not found",
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    task_data = next((task for task in tasks if task["id"] == task_id), None)
    if task_data is not None:
        tasks.remove(task_data)
        return {
            "message":"Task delete successfully"
        }

    raise HTTPException(
        status_code = 404,
        detail = "Task not found"
    )