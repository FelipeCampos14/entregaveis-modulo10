from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal, Base, engine
from database.models import UserDB
from database.schemas import User, UserCreate
import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

router = APIRouter(prefix="/assistance")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Home (irei usar como um heartbeat)
@app.get("/")
def get_heartbeat():
    return {"message": "Hello world"}

# CRUD Operations
@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    key = '/users'
    resultado = redis_client.get()
    if resultado:
        return json.loads(resultado)
    
    users = db.query(UserDB).all()
    db.close()
    redis_client.setex(key, 60, json.dumps(users))
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    key = f'/users/{user_id}'
    resultado = redis_client.get()
    if resultado:
        return json.loads(resultado)
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    redis_client.setex(key, 60, json.dumps(user))
    return user

@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.post("/token")
def create_token(user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == user.username, UserDB.password == user.password).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": str(user.id), "token_type": "bearer"}