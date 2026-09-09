from fastapi import HTTPException

def find_task_or_404(task_id: str, tasks: list):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task