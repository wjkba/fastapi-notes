from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


app = FastAPI()


#BaseModel z walidacja danych przyjmuje tylko ponizsze typy
class Book(BaseModel):
  id: UUID
  title: str = Field(min_length=1) #Field dodaje walidacje stringa
  author: str = Field(min_length=1, max_length=100)
  description: Optional[str] = Field(max_length=100, min_length=1) #optiopnal nie dziala?
  rating: int = Field(gt=-1, lt=11) # Ocena od 0 do 10

  #pydantic json schema, default
  model_config = {
    "json_schema_extra":{
      "example": {
        "id" : "12c56691-2826-4074-a23f-17e0df21c50b",
        "title": "Book title",
        "author": "Book Author",
        "description": "This is where description goes.",
        "rating": 5
      }
    }
  }
BOOKS = []



@app.get("/")
async def read_all_books():
  if len(BOOKS) < 1:
    # jesli nie ma ksiazek w array to je dodaj z funkcji ponizej
    create_books_no_api()
  return BOOKS




@app.post("/")
# book parameter musi byc typu Book, 
# tylko json request body z danymi ustalonymi
# w class Book(BaseModel) zadziala
async def create_book(book: Book): 
  BOOKS.append(book)
  return book






# Ta funkcja nie jest asynchroniczna i jest wywolywana wyzej
def create_books_no_api():
  book_1 =  Book(id="92c56691-2826-4074-a23f-17e0df21c50b", title="Animal Farm", author="George Orwell", description=None, rating=8)
  book_2 =  Book(id="2dfa50f1-d564-497b-8889-7a6700846f73", title="1984", author="George Orwell", description="A dystopian novel", rating=9)
  book_3 =  Book(id="5cca8e5f-f4b2-4b1a-b94d-1a5ce51cdaaa", title="To Kill a Mockingbird", author="Harper Lee", description="A classic American novel", rating=9)
  book_4 =  Book(id="3f6a8575-ab3c-4459-9ba5-635ab5d26e89", title="The Great Gatsby", author="F. Scott Fitzgerald", description="A novel about the American Dream", rating=8)
  book_5 =  Book(id="4258300d-4a20-4ee1-b7eb-12fd090f0beb", title="Pride and Prejudice", author="Jane Austen", description="A classic romance novel", rating=9)
  BOOKS.append(book_1)
  BOOKS.append(book_2)
  BOOKS.append(book_3)
  BOOKS.append(book_4)
  BOOKS.append(book_5)
  
