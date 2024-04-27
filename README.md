# FastAPI notes

## Setting up FastAPI

1. Creating virtual environment
2. Installing FastAPI

```
$ pip install "fastapi[all]"
```

Basic FastAPI setup

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

CORS allows cross-origin requests

```py
origins = ['*']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```

## HTTP Methods

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

## Models

### pydantic

this model is being used throughout the application to validate data

```py
from pydantic import BaseModel, Field

# model z walidacją danych przyjmuje tylko ponizsze typy
class Book(BaseModel):
  id: UUID
  title: str = Field(min_length=1) # Field dodaje walidacje stringa
  author: str = Field(min_length=1, max_length=100)
  description: Optional[str] = Field(max_length=100, min_length=1)
  rating: int = Field(gt=-1, lt=11) # Ocena od 0 do 10

# pydantic json schema, default
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
```

### sqlalchemy

this is a table model using sqlalchemy

```py
# tabelka klasa users
class Users(Base):
  __tablename__ = "users"
  # index=True is used to create an index on the column, which can improve the performance of queries that involve searching or filtering based on the column.
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  username = Column(String, unique=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)

  # relationship tworzy polaczenie miedzy tabelka users i todos
  # back_populates odnosi sie do owner zawartego w klasie Todos
  todos = relationship("Todos", back_populates="owner")
```

## User Authentication

CryptContext is used for password hashing

```py
# secret key is as tring or random 32byte
SECRET_KEY="0bc03c8be4a1243c3f972383ebce9cb41ee033595ccde0a0cb9eed145de66b54"
ALGORITHM = "HS256"
# z biblioteki passlib tworze instance CryptContext
# w ktorym podaje metode hashowania w schemes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

<br/>

OAuth2Bearer is setting up password security, it's telling fastapi to expect client\
 to authenticate by sending their username and password to the /token endpoint

```py
# uzycie dependency ktora bedzie ekstraktowac data z authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

<br/>

The token parameter depends on oauth2_scheme, when api recives a request it\
will first call oauth2_scheme function and use its result as the value of token

```py
@app.get("/v")
# pytamy czy klient ma token, jesli ma to dajemy dostęp do endpointa
# jeśli klient nie ma tokena to idź do tokenUrl
async def validate_token(token: str = Depends(oauth2_scheme)):
  return {"token": token}
```

<br/>

this function looks for a user in database, if user is found it\
 verifies the hashed password and returns true as a response

```py
async def authenticate_user(username, password):
  user = await users_collection.find_one({"username": username})
  if user:
    password_check = pwd_context.verify(password, user["password"])
    return password_check
  return False
```

<br/>

- data dictionary contains claims of the JWT (typically, the user)
- expires_delta specifies how long token should be valid
- function calculates expiration time and encodes token using SECRET_KEY and ALGORITHM, returns encoded JWT Token

```py
def create_access_token(data: dict, expires_delta: timedelta):
  to_encode = data.copy()
  expire = datetime.utcnow() + expires_delta # termin waznosci 30 minut od teraz
  to_encode.update({"exp":expire})
  # to_enocde zawiera sub: username i czas expire
  # to_encode kodujemy za pomoca jwt.encode i wykorzystujemy secret key z algorytmem
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_password_hash(password): # HASHOWANIE HASŁA
  return pwd_context.hash(password)
```

<br/>

login for access token, this is the token endpoint that authenticates\
the user and sends back JWT access token

```py
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  username = form_data.username
  password = form_data.password
  authenticated = await authenticate_user(username, password)
  if authenticated:
    access_token = create_access_token(data={"sub":username expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
  else:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
```
