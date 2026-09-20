import repositories.user as user_repository
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from exceptions.user import UserAlreadyExistsError, UserDoesNotExistError,InvalidCredentialsError
import bcrypt
from config import settings
from datetime import datetime, timedelta, timezone
import jwt
def create(user: UserCreate, db: Session):
    try:
        #check existing user
        existing_user = user_repository.find_user_by_email(user.email, db)
        if existing_user:
            raise UserAlreadyExistsError
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_created = user_repository.create_user(user, hashed_password, db)
        db.commit()
        db.refresh(user_created)
        return user_created
    except Exception:
        db.rollback()
        raise


def login(user: UserLogin, db: Session):
    existing_user = user_repository.find_user_by_email(user.email, db)
    if not existing_user:
        raise InvalidCredentialsError()
    
    hashed_password = existing_user.password
    verified = verify_password(user.password, hashed_password)
    if not verified:
        raise InvalidCredentialsError()
    return existing_user
    

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(user_id):
    data ={
        "sub":str(user_id),
        "exp":datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(
        data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token

def decode_access_token(token:str):
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

def current_user(token, db):
    try:
        payload = decode_access_token(token)
        user_id = payload["sub"]
        user = user_repository.find_user_by_id(user_id, db)
        if not user:
            raise InvalidCredentialsError
        return user
    except Exception:
        raise
    
def test_user(db: Session):
    result = user_repository.test_user(db)
    return result