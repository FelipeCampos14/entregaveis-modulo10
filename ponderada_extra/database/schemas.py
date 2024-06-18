from pydantic import BaseModel
from typing import Optional

# User

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Todo

class Todo(BaseModel):
    id: int
    title: str
    status: str

class TodoCreate(BaseModel):
    title: str
    status: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None