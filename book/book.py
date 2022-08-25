

class Book:
    def __init__(self,
                 name: str,
                 author: str,
                 id: int,
                 total_number_of_books: int,
                 number_of_books_available: int,
                 age_restricted: bool):
        self.name = name
        self.author = author
        self.id = id
        self.total_number_of_books = total_number_of_books
        self.number_of_books_available = number_of_books_available
        self.age_restricted = age_restricted

    def __str__(self):
        return self.str_output(self.name,
                               self.author,
                               self.id,
                               self.total_number_of_books,
                               self.number_of_books_available,
                               self.age_restricted)

    def str_output(self,
                   name: str,
                   author: str,
                   id: int,
                   total_number_of_books: int,
                   number_of_books_available: int,
                   age_restricted: bool):

        string_output = "Book name: " + name + "\n" + \
                        "Author: " + author + "\n" + \
                        "Book ID: " + str(id) + "\n" + \
                        "Total number of books: " + str(total_number_of_books) + "\n" + \
                        "Books available for borrowing: " + str(number_of_books_available) + "\n" + \
                        "Age restricted book: " + str(age_restricted)

        return string_output