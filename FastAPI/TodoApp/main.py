from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from auth import get_current_user, get_user_exception
import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



# pobierz todos z bazy danych
def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

class Todo(BaseModel):
  title: str
  description: Optional[str]
  priority: int = Field(gt=0, lt=6, description="Priority 1-5")
  complete: bool

# ta funkcja jest zalezna (Depends) od funkcji get_db()
# parametr db jest typu session i jest rowne dependecy get_db
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
  return db.query(models.Todos).all()

# Ta funkcja wyświetla wszystkie todos dla zalogowanego usera
# Zapytanie musi zawierać bearer token, bez niego funkcja get_current_user wyrzuca error
@app.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
  # funkcja get_current_user z auth sprawdza czy user jest zalogowany i ogarnia token jwt
  if user is None:
    raise get_user_exception()
  # szuka wszystkich todo usera w bazie
  return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

# get todo by ID
@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
  if user is None:
    raise get_user_exception()
  # filtrowanie bazy w poszukiwaniu todo id i sprawdzanie
  # czy todo nalezy to zalogowanego uzytkownika
  todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
  if todo_model is not None:
    return todo_model
  raise http_exception()



@app.post("/")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
  if user is None:
    raise get_current_user()
  # nowa zmienna todo_model jest typu model.Todos
  todo_model = models.Todos()
  todo_model.title = todo.title
  todo_model.description = todo.description
  todo_model.priority = todo.priority
  todo_model.complete = todo.complete
  # owner id jest rowny id zalogowanego uzytkownika
  # jwt token ogarnia ze uzytkonik jest zalogowany i zapisuje id
  todo_model.owner_id = user.get("id")

  db.add(todo_model)

  #db.commit - flush pending changes and commit the current transaction
  db.commit()

  return successful_response(201)


@app.put("/{todo_id}")
async def update_todo(todo_id: int,todo: Todo,user: dict=Depends(get_current_user), db: Session = Depends(get_db)):
  
  todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
  if user is None:
    raise get_user_exception()
  if todo_model is None:
    raise http_exception()
  todo_model.title = todo.title
  todo_model.description = todo.description
  todo_model.priority = todo.priority
  todo_model.complete = todo.complete

  db.add(todo_model)
  db.commit()
  return successful_response(200)

@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
  if user is None:
    raise get_user_exception()
  todo_model = db.query(models.Todos).\
    filter(models.Todos.id == todo_id).\
    filter(models.Todos.owner_id == user.get("id")).\
    first()
  if todo_model is None:
    raise http_exception()
  db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
  db.commit()
  return successful_response(200)




def successful_response(status_code: int):
  return {
    "status": status_code,
    "transaction": "succesful"
  }


def http_exception():
  return HTTPException(status_code=404, detail="Item not found")

