import sqlite3 as sl
import os
from book.book import Book

class DataBaseManager:
    def __init__(self):
        if os.path.exists("libraryDB.db") is False:
            self.con = sl.connect("libraryDB.db")
            self.create_user_db()
            self.create_book_db()
            self.create_borrowed_books_db()
        else:
            self.con = sl.connect("libraryDB.db")

    # Create USER table in the database
    def create_user_db(self):
        with self.con:
            self.con.execute("""
                        CREATE TABLE USER (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        date_of_birth TEXT,
                        mail_address TEXT,
                        phone_number TEXT,
                        address TEXT,
                        number_of_books_borrowed INTEGER,
                        list_of_books_borrowed_and_returned TEXT,
                        list_of_books_currently_borrowed TEXT);
                        """)
    # Generate new id in database
    def generate_id(self, previous_id):
        return previous_id + 1

    # Get previous User id
    def get_previous_user_id(self):
        with self.con:
            try:
                previous_user_id = self.con.execute("""SELECT id FROM USER ORDER BY id DESC LIMIT 1;""").fetchone()
                return previous_user_id[0]
            except TypeError:
                return 0

    # Add data in Database
    def add_data_in_db(self, sql, data):
        with self.con:
            self.con.execute(sql, data)

    # Add new user in the database
    def add_user_in_db(self,
                      first_name: str,
                      last_name: str,
                      date_of_birth: str,
                      mail_address: str,
                      phone_number: str,
                      address: str):

        sql_user = 'INSERT INTO USER (id, first_name,last_name, date_of_birth, mail_address, phone_number, address, ' \
      'number_of_books_borrowed, list_of_books_borrowed_and_returned, list_of_books_currently_borrowed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        new_user_id = self.generate_id(self.get_previous_user_id())
        data_user = [new_user_id ,first_name, last_name, date_of_birth, mail_address,
                     phone_number, address, 0, "-", "-"]
        self.add_data_in_db(sql_user, data_user)

    # Add new book in the database
    def add_book_in_db(self,
                       name: str,
                       author: str,
                       total_number_of_books: int,
                       age_restricted: bool):

        sql_book = 'INSERT INTO BOOK (id, name,author, total_number_of_books, number_of_books_available, age_restricted) ' \
      'VALUES(?, ?, ?, ?, ?, ?)'

        new_book_id = self.generate_id(self.get_previous_book_id())
        data_book = [new_book_id, name, author, total_number_of_books, total_number_of_books, age_restricted]
        self.add_data_in_db(sql_book, data_book)

    # Create BOOK table in the database
    def create_book_db(self):
        with self.con:
            self.con.execute("""
                        CREATE TABLE BOOK (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        author TEXT,
                        total_number_of_books INTEGER,
                        number_of_books_available INTEGER,
                        age_restricted BOOLEAN);
                        """)
    # Get previous Book id
    def get_previous_book_id(self):
        with self.con:
            try:
                previous_book_id = self.con.execute("""SELECT id FROM BOOK ORDER BY id DESC LIMIT 1;""").fetchone()
                return previous_book_id[0]
            except TypeError:
                return 0

    def add_book_to_existing_one(self, book_id: int):
        pass

    def update_available_books(self, book_id: int, user_id: int):
        pass

    # Create BORROWED_BOOKS table in the database
    def create_borrowed_books_db(self):
        with self.con:
            self.con.execute("""
                               CREATE TABLE BORROWED_BOOKS (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                               book_id INTEGER,
                               status TEXT,
                               date_of_borrow TEXT,
                               date_of_return TEXT);
                               """)

    # Get previous Borrowed_book id
    def get_previous_borrowed_book_id(self):
        with self.con:
            try:
                previous_borrowed_book_id = self.con.execute("""SELECT id FROM BORROWED_BOOKS ORDER BY id DESC LIMIT 1;""").fetchone()
                return previous_borrowed_book_id[0]
            except TypeError:
                return 0


    def borrowing_book(self, book_id: int):
        pass

    # List all books from database
    def list_all_books_from_db(self):
        list_of_book_objects = []
        with self.con:
            list_books = self.con.execute("""SELECT * FROM BOOK""").fetchall()
            for item in list_books:
                age_restricted = "True" if item[5] == 1 else "False"
                book_object = Book(name=item[1],
                                   author=item[2],
                                   id=item[0],
                                   total_number_of_books=item[3],
                                   number_of_books_available=item[4],
                                   age_restricted=bool(age_restricted))
                list_of_book_objects.append(book_object)
            return list_of_book_objects

    # List all books that have a specific word
    def list_search_book(self, book_name: str):
        list_of_book_objects = []
        with self.con:
            list_books = self.con.execute("""SELECT * FROM BOOK""").fetchall()
            for item in list_books:
                if book_name.lower() in item[1].lower():
                    age_restricted = "True" if item[5] == 1 else "False"
                    book_object = Book(name=item[1],
                                       author=item[2],
                                       id=item[0],
                                       total_number_of_books=item[3],
                                       number_of_books_available=item[4],
                                       age_restricted=bool(age_restricted))
                    list_of_book_objects.append(book_object)

            return list_of_book_objects