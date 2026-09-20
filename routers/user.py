from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from sqlalchemy.orm import Session
import services.user as services_user
from schemas.user import UserCreate, UserDetailResponse, UserLogin, UserLoginResponse
from exceptions.user import UserAlreadyExistsError,InvalidCredentialsError,UserDoesNotExistError
from utilis.user import get_current_user

user_router = APIRouter()

@user_router.post("/users", response_model=UserDetailResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    
    try:
        created_user = services_user.create(user, db)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        print(type(e), e)
        raise HTTPException(status_code=400, detail=f"{e}")
  
    return {
        "message":"user created succesfully",
        "user":created_user
    }

@user_router.post("/login", response_model=UserLoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        logged_in_user = services_user.login(user, db)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        print(type(e), e)
        raise HTTPException(status_code=400, detail=f"{e}")
    return {
        "user": logged_in_user,
        "access_token": services_user.create_access_token(logged_in_user.id)
    }
    

@user_router.get("/current_user", response_model=UserDetailResponse)
def read_current_user(current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    result = services_user.test_user(db)
    print(result)
    return {
        "user": current_user,
        "message": "current user fetched successfully"
    }