from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


# klasa o typie exception
class NegativeNumberException(Exception):
  def __init__(self, books_to_return):
    self.books_to_return = books_to_return


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

class BookNoRating(BaseModel):
  id: UUID
  title: str = Field(min_length=1)
  author: str = Field(min_length=1)
  description: Optional[str] = Field(None, title="description of the Book", max_length=100, min_length=1)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(reqeust: Request, exception: NegativeNumberException):
  return JSONResponse(
    status_code=418,
    content={"message": f"Negative number of books {exception.books_to_return} error"}
  )


@app.post("/books/login")
async def books_login(username: str = Form(...), password: str = Form(...)): # Form automatycznie dekoduje username i password
  return {"username": username, "password": password}


# Header wysyla dodatkowe informacje podczas zadania
@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
  return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
  if books_to_return and books_to_return < 0:
    raise NegativeNumberException(books_to_return=books_to_return)
  if len(BOOKS) < 1:
    # ZAPELNIA ARRAY, BEZ TEGO ARRAY JEST PUSTY
    # jesli nie ma ksiazek w array to je dodaj z funkcji ponizej
    create_books_no_api()

  if books_to_return and len(BOOKS) >= books_to_return > 0:
    # books_to_return to opcjonalne query, ktore po podaniu
    # liczby zwraca taka ilosc ksiazek
    i = 1
    x_books = []
    while i <= books_to_return:
      x_books.append(BOOKS[i-1])
      i += 1
    return x_books
  return BOOKS


# GET BOOK BY UUID
@app.get("/book/{book_id}")
async def get_by_id(book_id: UUID):
  for book in BOOKS:
    if book.id == book_id:
      return book
  raise raise_item_cannot_be_found_exception()

# GET BOOK NO RATING
# kiedy funkcja returnuje book to response_model zostanie przekonwertowany na BookNoRating model
@app.get("/book/norating/{book_id}", response_model=BookNoRating)
async def get_by_id_no_rating(book_id: UUID):
  for book in BOOKS:
    if book.id == book_id:
      return book
  raise raise_item_cannot_be_found_exception()





# PUT UPDATE BY UUID
@app.put("/book/{book_id}")
async def update_book(book_id: UUID, book : Book):
  for item in BOOKS:
    if item.id == book_id:
      BOOKS[BOOKS.index(item)] = book
      return{"msg":"Book has been updated"}
  raise raise_item_cannot_be_found_exception()
    

# DELETE BY UUID
@app.delete("/book/{book_id}")
async def delete_book(book_id: UUID):
  for item in BOOKS:
    if item.id == book_id:
      BOOKS.remove(item)
      return{"message": f"{item.title} has been deleted"}
  # kod nizej zostanie wykonany wtedy kiedy if fails
  raise HTTPException(status_code=404, detail="Book not found", headers={"X-Header-Error": "Nothing to be seen at the UUID"})


# POST ADD BOOK
@app.post("/" , status_code=status.HTTP_201_CREATED) # status code dodaje nowy status dla post
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
  



def raise_item_cannot_be_found_exception():
  return HTTPException(status_code=404, detail="Book not found", headers={"X-Header-Error": "Nothing to be seen at the UUID"})
