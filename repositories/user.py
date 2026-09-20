from schemas.user import UserCreate
from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select
import uuid
from db.models.user import User
from db.models.task import Task
def create_user(user: UserCreate, password: str, db: Session):
    user_save = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=password
    )
    db.add(user_save)
    return user_save

def find_user_by_email(email:str, db:Session):
    user = db.execute(
        select(User).where(User.email == email)
    )
    return user.scalar_one_or_none()

def find_user_by_id(id:str, db:Session):
    user = db.execute(
        select(User).where(User.id == id)
    )
    return user.scalar_one_or_none()

def test_user(db: Session):
    users = list(db.execute(select(User).options(selectinload(User.tasks))).scalars().all())
    for user in users:
        tasks = user.tasks 
        print(f"User {user.id} has {len(tasks)} tasks")
   

def find_tasks_by_user(user_id: str, db: Session) -> list[Task]:
    query = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    return db.execute(query).scalars().all()