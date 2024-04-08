from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# Tableka SQL


# klasa todo z Base from database
class Todos(Base):
  __tablename__ = "todos"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  complete = Column(Boolean, default=False)



