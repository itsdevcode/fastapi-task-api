
import repositories.task as task_repository
from schemas.task import TaskCreate,TaskUpdate
from sqlalchemy.orm import Session

def create(task: TaskCreate, db: Session):
    try:
        task_created = task_repository.create_task(task, db)
        db.commit()
        db.refresh(task_created)
        return task_created
    except Exception:
        db.rollback()
        raise

def get(task_id: str, db: Session):
    task = task_repository.get_task_by_id(task_id, db)
    return task

def all(db: Session):
    tasks = task_repository.get_all_tasks(db)
    return tasks

def update(task_id: str, task: TaskUpdate, db: Session):
    try:
        task_updated = task_repository.update_task(task_id, task, db)
        if task_updated is None:
            return None
        db.commit()
        db.refresh(task_updated)
        return task_updated
    except Exception:
        db.rollback()
        raise
        
def delete(task_id:str, db: Session):
    try:
        task_deleted = task_repository.delete_task(task_id, db)
       
        if task_deleted is None:
            return None
        db.commit()
        return task_deleted
    except Exception:
        db.rollback()
        raise
