from sqlalchemy import Column, Integer, String
from .database import Base

class TodoDB(Base):
  __tablename__ = 'todos'

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(50), nullable=False)
  status = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, title:{self.title}, status:{self.status}]>'
    
  def serialize(self):
    return {
      "id": self.id,
      "title": self.title,
      "status": self.status
    }

class UserDB(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(50), nullable=False)
  password = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, username:{self.username}, password:{self.password}]>'
    
  def serialize(self):
    return {
      "id": self.id,
      "username": self.username,
      "password": self.password
    }
