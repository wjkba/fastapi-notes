from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# link do sqlite database todo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"


# tworzenie silnika 
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# instancja sesji database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base zostanie wykorzystany to stworzenia database model
Base = declarative_base()


