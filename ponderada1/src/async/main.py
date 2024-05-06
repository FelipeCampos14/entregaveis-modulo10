from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from database.models import User
from database.database import SessionLocal
app = FastAPI()

# # CRUD Operations
# @app.get("/users", response_model=List[User])
# def get_users():
#     db = SessionLocal()
#     users = db.query(User).all()
#     db.close()
#     return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @app.post("/users", response_model=User)
# def create_user(user: UserCreate):
#     db = SessionLocal()
#     db_user = User(username=user.username, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     db.close()
#     return db_user

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     password: Optional[str] = None

# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: UserUpdate):
#     db = SessionLocal()
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user is None:
#         db.close()
#         raise HTTPException(status_code=404, detail="User not found")
#     if user.username is not None:
#         db_user.username = user.username
#     if user.password is not None:
#         db_user.password = user.password
#     db.commit()
#     db.refresh(db_user)
#     db.close()
#     return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    db.close()
    return db_user

# Authentication and Authorization
from fastapi.security import HTTPBasicCredentials, HTTPBasic

security = HTTPBasic()

@app.post("/token")
def create_token(credentials: HTTPBasicCredentials = Depends(security)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == credentials.username, User.password == credentials.password).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": str(user.id), "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Cookie(None)):
    db = SessionLocal()
    user = db.query(User).filter(User.id == int(token)).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Static Files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@app.get("/user-login")
async def user_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/user-register")
async def user_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/error")
async def error(request: Request):
    return templates.TemplateResponse("error.html", {"request": request})

@app.get("/content")
async def content(request: Request, token: str = Cookie(None)):
    db = SessionLocal()
    user = db.query(User).filter(User.id == int(token)).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return templates.TemplateResponse("content.html", {"request": request})
