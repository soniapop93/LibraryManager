from typing import  *

class Book:
    def __init__(self,
                 name: str,
                 author: str,
                 id, int,
                 number_of_books: int,
                 book_available: bool,
                 age_restricted: bool):
        self.name = name
        self.author = author
        self.id = id
        self.number_of_books = number_of_books
        self.book_available = book_available
        self.age_restricted = age_restricted

