# FastAPI notes

## Setting up FastAPI

1. Creating virtual environment
2. Installing FastAPI

```
$ pip install "fastapi[all]"
```

it also includes uvicorn
</br>
</br>

## main.py file

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

</br>
</br>

## POST, GET, PUT, DELETE methods

### GET

```python
@app.get("/books")
async def read_all_books(skip_book: Optional[str]= None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[3-1]
        return new_books
    return BOOKS
```

### POST

```python
# POST BOOK
@app.post("/create/{book_title}:{book_author}")
async def create_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        last_id = max(book["id"] for book in BOOKS)
        current_book_id = last_id + 1
        book = {"id": current_book_id, "title": book_title, "author": book_author}
        BOOKS.append(book)
        return {"message": f"Created book - {book_title} by {book_author}"}
```

### PUT

```python
@app.put("/update")
async def update_book(book_id: int, new_title: str, new_author: str):
    for book in BOOKS:
        if book["id"] == book_id:
            book["title"] = new_title
            book["author"] = new_author
            return {"message": f"Updated book - {new_title} by {new_author}"}
```

### DELETE

```python
@app.delete("/delete/{book_id}")
async def delete_book(book_id: int):
        for book in BOOKS:
            if book["id"] == book_id:
                BOOKS.remove(book)
                return{"message": f"{book["title"]} has been deleted"}
```
