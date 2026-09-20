from sqlalchemy.orm import Session
from db.models.task import Task as TaskDB
from sqlalchemy import select, func, desc, asc, or_
from schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
import uuid
from enums.task import TaskShortField, SortOrder
def get_task_by_id(task_id: str, db: Session, user_id: str):
    task = db.execute(
        select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    ).scalar_one_or_none()
    return task

def get_all_tasks(
    db: Session, 
    user_id: str, 
    offset: int = 0, 
    limit: int = 10, 
    is_completed: bool | None = None, 
    sort_by: TaskShortField = TaskShortField.created_at, 
    sort_order: SortOrder = SortOrder.desc,
    search: str | None = None
):
    query = select(TaskDB).where(TaskDB.user_id == user_id)
    
    if search:
        query = query.where(
            or_(
                TaskDB.title.ilike(f"%{search}%"),
                TaskDB.description.ilike(f"%{search}%")
            )
        )

    if is_completed is not None:
        query = query.where(TaskDB.is_completed == is_completed)

    sort_column = getattr(TaskDB, sort_by.value)
    order_func = desc if sort_order == SortOrder.desc else asc
    query = query.order_by(order_func(sort_column), order_func(TaskDB.id))
    tasks = db.execute(
        query.offset(offset).limit(limit)
    ).scalars()
    return tasks.all()

def delete_task(task_id: str, db: Session, user_id: str):
    task = get_task_by_id(task_id, db, user_id)
    if task:
        db.delete(task)
        return task
    return None

def create_task(task: TaskCreate, user_id: str, db: Session):
    task_save = TaskDB(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        is_completed=False,
        user_id=user_id
    )
    db.add(task_save)
    return task_save

def update_task(task_id: str, task: TaskUpdate, db: Session, user_id: str):
    db_task = get_task_by_id(task_id, db, user_id)
    if not db_task:
        return None
    updated_task = task.model_dump(exclude_unset=True)

    for key, value in updated_task.items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.now()

    return db_task

def get_total(db:Session, user_id:str, is_completed: bool | None = None, search: str|None = None):
    query = select(func.count(TaskDB.id)).where(TaskDB.user_id == user_id)
    if search is not None:
        query = query.where(
            or_(
                TaskDB.title.ilike(f"%{search}%"),
                TaskDB.description.ilike(f"%{search}%")
            )
        )
    if is_completed is not None:
        query = query.where(TaskDB.is_completed == is_completed)
    total = db.execute(query).scalar()
    return total

