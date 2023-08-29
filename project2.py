from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book():
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

##for validation
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int

    #for configuration-to create a more descriptive request within swagger docs
    class Config:
        json_schema_extra = {
            'example':{
                "title": "A new book",
                "author": "coding",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }


Books = [
      Book(1,"The India Story","Bimal Jalal", "indian story", 5, 2010),
      Book(2,"Listen to Your Heart: The London Adventure","Ruskin Bond", "about bond", 4, 2011),
      Book(3,"Queen of Fire","Devika Rangachari", "about women", 3, 2012),
      Book(4,"Monsoon","Sahitya Akademi", "about season", 4, 2013),
      Book(5,"Back to the Roots","Tamannaah Bhatia", "about native", 4, 2014),
      Book(6,"400 Days","Chetan Bhagat", "about golden days", 3, 2015),
      Book(7,"Jungle Nama","Amitav Ghosh", "about adventure", 5, 2016)
]

@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return Books

@app.get("/book/{book_id}", status_code= status.HTTP_200_OK)
def read_book_by_id(book_id:int = Path(gt=0)):
    '''
    read a book based on id
    '''
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item Not Found")

@app.get("/books/", status_code= status.HTTP_200_OK)
def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    '''
      read book based on rating
    '''   
    similar_rating_books = []
    for book in Books:
        if book.rating == book_rating:
            similar_rating_books.append(book)
    if similar_rating_books:
        return similar_rating_books
    else:
        raise HTTPException(status_code=404, detail="Item Not Found")
  
@app.get("/books/{published_date}", status_code=status.HTTP_200_OK)
def get_book_by_published_date(published_date:int = Path(gt=0)):
    published_book = []
    for book in Books:
        if book.published_date == published_date:
            published_book.append(book)
    if published_book:
        return published_book
    else:
        raise HTTPException(status_code=404, detail="Item Not Found")
     
### pydantics and data validation 
#pydantics: python library that is used for data modeling, data parsing and has efficient error handling.pydantics commonly used as a resource for data validation and how to handle data coming to our FastAPT Application.
@app.post("/create", status_code= status.HTTP_201_CREATED)
def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id+1
    return book

@app.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found")


@app.delete("/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int = Path(gt=0)):
    book_deleted = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Item Not Found")


