import logging
from fastapi import FastAPI, Cookie, HTTPException, Depends, File, UploadFile, Request, Response
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.orm import Session
from typing import List
from httpx import AsyncClient
from database.database import SessionLocal, Base, engine
from database.models import UserDB
from database.schemas import User, UserCreate, UserUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(" Heartbeat check")
    return {"message": "Hello world"}

# CRUD Operations
@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    db.close()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if user is None:
        logger.warning(f" Usuário com id {user_id} não foi encontrado.")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    logger.info(f" Usuário com id {db_user.id} foi criado.")
    return db_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        db.close()
        logger.warning(f" Usuário com id {user_id} não foi encontrado para ser atualizado.")
        raise HTTPException(status_code=404, detail="User not found")
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    db.close()
    logger.info(f" Usuário com id {user_id} foi atualizado.")
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        db.close()
        logger.warning(f" Usuário com id {user_id} não foi encontrado para ser excluído.")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    db.close()
    logger.info(f" Usuário com id {user_id} foi excluído.")
    return db_user

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    async with AsyncClient() as client:
        files = {'file': (file.filename, await file.read(), file.content_type)}
        response = await client.post("http://image-processing:8000/api/process-image", files=files)

        if response.status_code == 200:
            return Response(content=response.content, media_type="image/png")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Authentication and Authorization
security = HTTPBasic()

@app.post("/token")
def create_token(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == credentials.username, UserDB.password == credentials.password).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": str(user.id), "token_type": "bearer"}
