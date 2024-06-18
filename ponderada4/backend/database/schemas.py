from pydantic import BaseModel
from typing import Optional


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True



# User

class UserBase(OurBaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

# Todo

class TodoBase(OurBaseModel):
    title: str

class TodoCreate(TodoBase):
    status: str

class TodoUpdate(TodoBase):
    status: Optional[str] = None

class Todo(TodoBase):
    id: int
    title: str
    status: str
