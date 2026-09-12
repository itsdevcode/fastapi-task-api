from sqlalchemy.orm import Session
from db.models.task import Task as TaskDB
from sqlalchemy import select
from schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
import uuid
def get_task_by_id(task_id: str, db: Session):
    task = db.execute(
        select(TaskDB).where(TaskDB.id == task_id)
    ).scalar_one_or_none()
    return task

def get_all_tasks(db: Session):
    tasks = db.execute(
        select(TaskDB)
    ).scalars().all()
    return tasks

def delete_task(task_id: str, db: Session):
    task = get_task_by_id(task_id, db)
    if task:
        db.delete(task)
        return task
    return None

def create_task(task: TaskCreate, db: Session):
    task_save = TaskDB(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        is_completed=False
    )
    db.add(task_save)
    return task_save

def update_task(task_id: str, task: TaskUpdate, db: Session):
    db_task = get_task_by_id(task_id, db)
    if not db_task:
        return None
    updated_task = task.model_dump(exclude_unset=True)

    for key, value in updated_task.items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.now()

    return db_task