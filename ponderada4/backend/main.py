import logging
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from database.database import SessionLocal, Base, engine
from database.models import UserDB, TodoDB
from database.schemas import User, UserCreate,Todo, TodoCreate, TodoUpdate
from logging_config import LoggerSetup

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)

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
    LOGGER.info("Acessando a rota /")
    return {"message": "Hello world"}

# CRUD Operations
@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    LOGGER.info({"message": "Acessando a rota /users", "method": "GET"})
    users = db.query(UserDB).all()
    db.close()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if user is None:
        LOGGER.warning(f" Usuário com id {user_id} não foi encontrado.")
        raise HTTPException(status_code=404, detail="User not found")
    LOGGER.info(f" Usuário com id {user_id} foi encontrado.")
    return user

@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    LOGGER.info(f" Usuário com id {db_user.id} foi criado.")
    return db_user

@app.post("/token")
def create_token(user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == user.username, UserDB.password == user.password).first()
    db.close()
    if user is None:
        LOGGER.warning(f" Usuário com estas credenciais não foi encontrado.")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    LOGGER.info(f" Usuário com id {user.id} fez login.")
    return {"access_token": str(user.id), "token_type": "bearer"}

# ToDos CRUD

@app.get("/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).all()
    db.close()
    return todos

@app.get("/todos/{todos}", response_model=Todo)
def get_todo(todos: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todos).first()
    db.close()
    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoDB(title=todo.title, status=todo.status)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.close()
    LOGGER.info(f" ToDo com id {db_todo.id} foi criado.")
    return db_todo

@app.put("/todos/{todos}", response_model=Todo)
def update_todo(todos: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todos).first()
    if db_todo is None:
        db.close()
        LOGGER.warning(f"Não há um ToDo com este id {db_todo.id}")
        raise HTTPException(status_code=404, detail="todo not found")
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.status is not None:
        db_todo.status = todo.status
    db.commit()
    db.refresh(db_todo)
    db.close()
    LOGGER.info(f" ToDo com id {db_todo.id} foi atualizado.")
    return db_todo

@app.delete("/todos/{todos}", response_model=Todo)
def delete_todo(todos: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todos).first()
    if db_todo is None:
        db.close()
        LOGGER.warning(f"Não há um ToDo com este id {db_todo.id}")
        raise HTTPException(status_code=404, detail="todo not found")
    db.delete(db_todo)
    db.commit()
    db.close()
    LOGGER.info(f" ToDo com id {db_todo.id} foi removido.")
    return db_todo
