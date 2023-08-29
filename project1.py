from fastapi import FastAPI,Body

app = FastAPI()

books=[
    {
        "title":"book one", "author":"author one", "category":"science"
    },
     {
        "title":"book two", "author":"author two", "category":"math"
    },
     {
        "title":"book three", "author":"author one", "category":"science"
    },
     {
        "title":"book four", "author":"author four", "category":"math"
    }
]


###  1. get method
@app.get("/books")
def get_books_info():
    return books

#path parameter -> are request parameters that have been attached to the URL EX-127.0.0.1:8000/books/book%20one
@app.get("/books/{book_title}")
def read_book(book_title:str):
    for book in books:
        if book.get("title").lower() == book_title.lower():
            return book
        
#order matters - it will execute read_book method because of order.
@app.get("/books/mybook")
def mybook():
    return {"mybook": "my favourite book"}

#query parameter -> are request parameter that have beeen attached after a "?" and its name=value pair Ex-127.0.0.1:8000/books/?category=math
@app.get("/books/")
def read_book_category_query(category:str):
    similar_category_books=[]
    for book in books:
        if book.get("category").lower() == category.lower():
            similar_category_books.append(book)
    return similar_category_books

#path and query parameter ex- 127.0.0.1:8000/books/book%20one/?category=science
@app.get("/books/{book_author}/")
def read_author_category(book_author,category):
    new_books=[]
    for book in books:
        if book.get("author").lower() == book_author.lower() and \
        book.get("category").lower() == category.lower():
            new_books.append(book)
    return new_books
        


###  2. post method - used to create and have body.
@app.post("/books/create_book")
def create_books(new_book=Body()):
    books.append(new_book)


### 3. put method- used to update the data and have body
@app.put("/books/update_book")
def update_books(update_book=Body()):
    for i in range(len(books)):
        if books[i].get("title").lower() == update_book.get("title").lower():
            books[i] = update_book



### 4. Delete Method- used to delete the data and have no body
@app.delete("/books/delete_book/{book_title}")
def delete_books(book_title:str):
    for i in range(len(books)):
        if books[i].get("title").lower() == book_title.lower():
            books.pop(i)
            break

# # question - Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.
# #path parameter
# @app.get("/books/{author_name}")
# async def fetch_book_details_by_author(author_name:str):
#     new_book_list=[]
#     for book in books:
#         if book.get("author").lower() == author_name.lower():
#             new_book_list.append(book)
#     return new_book_list

# #query parameter
# @app.get("/books/")
# async def fetch_book_details_by_author_query(author_name:str):
#     new_book_list=[]
#     for book in books:
#         if book.get("author").lower() == author_name.lower():
#             new_book_list.append(book)
#     return new_book_list

