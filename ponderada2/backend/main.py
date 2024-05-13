from fastapi import FastAPI, Cookie, HTTPException, Response, Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from database.models import UserDB
from database.database import SessionLocal
app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    password: str

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations
@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db = SessionLocal()
    db_user = UserDB(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db = SessionLocal()
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
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
def create_token(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == credentials.username, UserDB.password == credentials.password).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": str(user.id), "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Cookie(None)):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == int(token)).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

