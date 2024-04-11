from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tableki SQL


# tabelka klasa users
class Users(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True) # index=True is used to create an index on the column, which can improve the performance of queries that involve searching or filtering based on the column.
  email = Column(String, unique=True, index=True)
  username = Column(String, unique=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)

  # relationship tworzy polaczenie miedzy tabelka users i todos
  # back_populates odnosi sie do owner zawartego w klasie Todos
  todos = relationship("Todos", back_populates="owner")


# klasa todo z Base from database
class Todos(Base):
  __tablename__ = "todos"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  complete = Column(Boolean, default=False)

  # ForeignKey odnosi sie do users.id 
  owner_id = Column(Integer, ForeignKey("users.id"))

  # relationship tworzy polaczenie miedzy tabelka users i todos
  owner = relationship("users", back_populates="todos")




