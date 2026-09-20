
import repositories.task as task_repository
from schemas.task import TaskCreate,TaskUpdate
from sqlalchemy.orm import Session
import services.user as user_services
from enums.task import TaskShortField, SortOrder
def create(task: TaskCreate, user_id: str, db: Session):
    try:
        task_created = task_repository.create_task(task, user_id, db)
        # raise Exception("Test")
        db.commit()
        db.refresh(task_created)
        return task_created
    except Exception:
        db.rollback()
        raise

def get(task_id: str, db: Session, user_id: str):
    task = task_repository.get_task_by_id(task_id, db, user_id)
    return task

def all(
    db: Session,
    user_id: str,
    page:int = 1, 
    limit:int = 10,
    is_completed: bool | None = None,
    sort_by: TaskShortField = TaskShortField.created_at,
    sort_order: SortOrder = SortOrder.desc,
    search: str | None = None
   ):
    total = task_repository.get_total(db, user_id, is_completed, search)
    offset = (page - 1) * limit
    tasks = task_repository.get_all_tasks(db, user_id, offset, limit, is_completed, sort_by, sort_order, search)
    return {
        "page": page,
        "limit": limit,
        "offset": offset,
        "total": total,
        "tasks": tasks
    }

def update(task_id: str, task: TaskUpdate, db: Session, user_id: str):
    try:
        task_updated = task_repository.update_task(task_id, task, db, user_id)
        if task_updated is None:
            return None
        db.commit()
        db.refresh(task_updated)
        return task_updated
    except Exception:
        db.rollback()
        raise
        
def delete(task_id:str, db: Session, user_id: str):
    try:
        task_deleted = task_repository.delete_task(task_id, db, user_id)
       
        if task_deleted is None:
            return None
        db.commit()
        return task_deleted
    except Exception:
        db.rollback()
        raise

def get_total(db: Session, user_id: str):
    return task_repository.get_total(db, user_id)