from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import  status
app = FastAPI()


class Book:
    id = int
    title: str
    author: str
    description: str
    ratings: int
    published_date: int

    def __init__(self, id, title, author, description, ratings, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.ratings = ratings
        self.published_date = published_date


BOOK = [Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
        Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
        Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
        Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
        Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
        Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
        ]


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    ratings: int = Field(gt=0, lt=6)
    published_date :int = Field(gt=1990, lt=2050)

    class Config:
        schema_extra = {
            'example': {
                'id': 0,
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'ratings': 5,
                'published_date': 2012
            }
        }


@app.get('/books/')
def read_all_books():
    return BOOK


@app.get("/book/{book_id}/", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    print(book_id)
    for i in range(len(BOOK)):
        if BOOK[i].id == book_id:
            return BOOK[i]
        else:
            return "Id is not present"
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/book/", status_code=status.HTTP_200_OK)
async def read_book_by_ratings(ratings: int = Query(gt=0, lt=6)):
    responce_book_by_reviews = []
    for book in BOOK:
        if book.ratings == ratings:
            responce_book_by_reviews.append(book)
    return responce_book_by_reviews


@app.get("/books/{pub_date}", status_code=status.HTTP_200_OK)
async def read_by_published_date(pub_date: int):
    return_responce = []
    for book in BOOK:
        if book.published_date == pub_date:
            return_responce.append(book)
    return return_responce


@app.post('/books/add_book/', status_code=status.HTTP_201_CREATED)
def add_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOK.append(find_book_id(new_book))


def find_book_id(book: Book):
    '''
    This function is checking the index value and assing it to last
    :param book:
    :return: book
    '''
    if len(BOOK) > 0:
        book.id = BOOK[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOK)):
        if BOOK[i].id == book.id:
            BOOK[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    book_deleted = False
    for i in range(len(BOOK)):
        if BOOK[i].id == book_id:
            BOOK.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')
