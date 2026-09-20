from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class UserDetailResponse(BaseModel):
    message: str
    user: UserResponse

class UserLoginResponse(BaseModel):
    user:UserResponse
    access_token:str
    refresh_token:str|None = None

class UserListResponse(BaseModel):
    users:list[UserResponse]
    
    