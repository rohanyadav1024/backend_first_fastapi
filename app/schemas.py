from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    id: int
    name: str
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name : str
    email : EmailStr

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id : int

class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"
    

class Vote(BaseModel):
    id: int
    dir: conint(le=1)


class CreatePost(BaseModel):
    id: int
    title: str
    content: str

class PostOut(CreatePost):
    created_at: datetime
    owner_id: int
    published : bool

    owner : UserOut
    votes : int

    class Config:
        orm_mode=True

