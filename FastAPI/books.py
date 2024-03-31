from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()


BOOKS = [
    {"id": 1, "author": "J.K. Rowling", "title": "Harry Potter and the Sorcerer's Stone"},
    {"id": 2, "author": "J.R.R. Tolkien", "title": "The Lord of the Rings"},
    {"id": 3, "author": "George Orwell", "title": "1984"},
    {"id": 4, "author": "Harper Lee", "title": "To Kill a Mockingbird"},
    {"id": 5, "author": "Jane Austen", "title": "Pride and Prejudice"},
    {"id": 6, "author": "F. Scott Fitzgerald", "title": "The Great Gatsby"},
    {"id": 7, "author": "Leo Tolstoy", "title": "War and Peace"},
    {"id": 8, "author": "Mark Twain", "title": "Adventures of Huckleberry Finn"},
    {"id": 9, "author": "Charles Dickens", "title": "A Tale of Two Cities"},
    {"id": 10, "author": "Emily Bronte", "title": "Wuthering Heights"},
    {"id": 11, "author": "Herman Melville", "title": "Moby-Dick"},
    {"id": 12, "author": "Fyodor Dostoevsky", "title": "Crime and Punishment"},
    {"id": 13, "author": "William Shakespeare", "title": "Romeo and Juliet"},
    {"id": 14, "author": "Jane Austen", "title": "Emma"},
    {"id": 15, "author": "Charlotte Bronte", "title": "Jane Eyre"},
    {"id": 16, "author": "George Orwell", "title": "Animal Farm"},
    {"id": 17, "author": "J.D. Salinger", "title": "The Catcher in the Rye"},
    {"id": 18, "author": "Victor Hugo", "title": "Les Misérables"},
    {"id": 19, "author": "Oscar Wilde", "title": "The Picture of Dorian Gray"},
    {"id": 20, "author": "Gabriel Garcia Marquez", "title": "One Hundred Years of Solitude"}
]






@app.get("/")
async def first_api():
    return {"message": "This is / "}

# QUERY PARAMTERS
@app.get("/books")
async def read_all_books(skip_book: Optional[str]= None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[3-1]
        return new_books
    return BOOKS


# GET BOOK OBJECT BY TITLE
@app.get("/books/{title}")
async def book(title):
    for book in BOOKS:
        if book["title"] == title:
            return {book}
    return {"message": "Book not found"}


# GET BOOK TITLE BY ID
@app.get("/books/{book_id}")
async def read_book(book_id):
    title  = BOOKS[f"book_{book_id}"]
    return {"book": f"{title["title"]}"}

# GET BOOK ID BY TITLE
@app.get("/books/id/{title}")
async def id_by_title(title):
    for book in BOOKS:
        if book['title'] == title:
            return {"id": BOOKS.index(book)}
    return {"message": "Book not found"}
    

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

            

# PUT BOOK

@app.put("/update")
async def update_book(book_id: int, new_title: str, new_author: str):
    for book in BOOKS:
        if book["id"] == book_id:
            book["title"] = new_title
            book["author"] = new_author
            return {"message": f"Updated book - {new_title} by {new_author}"}
        
# DELETE BOOK
@app.delete("/delete/{book_id}")
async def delete_book(book_id: int):
        for book in BOOKS:
            if book["id"] == book_id:
                BOOKS.remove(book)
                return{"message": f"{book["title"]} has been deleted"}
