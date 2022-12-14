import sqlite3 as sl
import os
from book.book import Book
from user.user import User
from book.borrowed_book import BorrowedBook
from datetime import datetime


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
    def create_user_db(self) -> None:
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

    # Add data in Database
    def add_data_in_db(self, sql, data) -> None:
        with self.con:
            self.con.execute(sql, data)

    # Add new user in the database
    def add_user_in_db(self,
                       first_name: str,
                       last_name: str,
                       date_of_birth: str,
                       mail_address: str,
                       phone_number: str,
                       address: str) -> None:

        sql_user = 'INSERT INTO USER (first_name,last_name, date_of_birth, mail_address, phone_number, address, ' \
                   'number_of_books_borrowed, list_of_books_borrowed_and_returned, list_of_books_currently_borrowed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'

        data_user = [first_name, last_name, date_of_birth, mail_address,
                     phone_number, address, 0, "-", "-"]
        self.add_data_in_db(sql_user, data_user)

    # Add new book in the database
    def add_book_in_db(self,
                       name: str,
                       author: str,
                       total_number_of_books: int,
                       age_restricted: bool) -> None:

        sql_book = 'INSERT INTO BOOK (name, author, total_number_of_books, number_of_books_available, age_restricted) ' \
                   'VALUES(?, ?, ?, ?, ?)'

        data_book = [name, author, total_number_of_books, total_number_of_books, age_restricted]
        self.add_data_in_db(sql_book, data_book)

    # Create BOOK table in the database
    def create_book_db(self) -> None:
        with self.con:
            self.con.execute("""
                        CREATE TABLE BOOK (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        author TEXT,
                        total_number_of_books INTEGER,
                        number_of_books_available INTEGER,
                        age_restricted BOOLEAN);
                        """)

    # Create BORROWED_BOOKS table in the database
    def create_borrowed_books_db(self) -> None:
        with self.con:
            self.con.execute("""
                               CREATE TABLE BORROWED_BOOKS (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                               book_id INTEGER,
                               status TEXT,
                               date_of_borrow TEXT,
                               date_of_return TEXT,
                               user_id_that_borrowed_the_book INTEGER);
                               """)

    # Get available books number from database
    def get_available_books_number(self, book_id: int) -> str:
        with self.con:
            available_books_nr = self.con.execute("""SELECT number_of_books_available FROM BOOK WHERE ID=?""",
                                                  str(book_id)).fetchone()
        return available_books_nr[0]

    # Get the total number of books borrowed by user
    def get_number_of_previous_books_borrowed_by_user(self, user_id: int) -> str:
        with self.con:
            books_borrowed_by_user_nr = self.con.execute("""SELECT number_of_books_borrowed FROM USER WHERE id=?""",
                                                         str(user_id)).fetchone()
        return books_borrowed_by_user_nr[0]

    # Insert borrowed book into borrowed_book table
    def insert_borrowed_book_into_borrowed_book_table(self, book_id: int, user_id: int) -> int:
        borrowed_book_obj = BorrowedBook(book_id=book_id,
                                         status="borrowed",
                                         date_of_borrow=str(datetime.now()),
                                         date_of_return="-",
                                         user_id_that_borrowed_the_book=user_id)

        sql_borrowed_book = 'INSERT INTO BORROWED_BOOKS (book_id, status, date_of_borrow, date_of_return, user_id_that_borrowed_the_book) ' \
                            'VALUES(?, ?, ?, ?, ?)'

        data_borrowed_book = [borrowed_book_obj.book_id, borrowed_book_obj.status, borrowed_book_obj.date_of_borrow,
                              borrowed_book_obj.date_of_return, borrowed_book_obj.user_id_that_borrowed_the_book]
        self.add_data_in_db(sql_borrowed_book, data_borrowed_book)

        with self.con:
            id_of_borrowed_book = \
            (self.con.execute("""SELECT id FROM BORROWED_BOOKS ORDER BY id DESC LIMIT 1;""").fetchone())[0]

        print("Book with ID " + str(borrowed_book_obj.book_id) +
              " was inserted in the BORROWED_BOOKS table")
        return int(id_of_borrowed_book)

    # Get the number of books that the library has for a specific book id
    def number_of_books(self, book_id: int) -> str:
        with self.con:
            book_nr = self.con.execute("""SELECT total_number_of_books FROM BOOK WHERE ID=?""",
                                       str(book_id)).fetchone()
        return book_nr[0]

    # Change the number of books available for an existing book -> if the library receives more books
    def add_books_to_existing_ones(self, book_id: int, new_book_number: int) -> None:
        previous_nr_of_total_books = self.number_of_books(book_id=book_id)
        new_total_nr_of_books = int(previous_nr_of_total_books) + new_book_number

        previous_nr_of_available_books = self.get_available_books_number(book_id=book_id)
        new_nr_of_available_books = int(previous_nr_of_available_books) + new_book_number
        with self.con:
            self.con.execute("""UPDATE BOOK SET total_number_of_books = ? WHERE id = ?""",
                             (str(new_total_nr_of_books), str(book_id)))
            self.con.execute("""UPDATE BOOK SET number_of_books_available = ? WHERE id = ?""",
                             (str(new_nr_of_available_books), str(book_id)))
        print(str(new_book_number) + " new book(s) are added in the database for book with id: " + str(book_id))

    # Borrowing book by book id
    def borrowing_book(self, book_id: int) -> None:
        available_book = self.get_available_books_number(book_id)
        new_nr_of_available_books = int(available_book) - 1
        with self.con:
            self.con.execute("""UPDATE BOOK SET number_of_books_available = ? WHERE id = ?""",
                             (str(new_nr_of_available_books), str(book_id)))
            print("The book with ID: " + str(book_id) + " is borrowed. Available books: " +
                  str(new_nr_of_available_books))

    # List all books from database
    def list_all_books_from_db(self) -> list:
        list_of_book_objects = []
        with self.con:
            list_books = self.con.execute("""SELECT * FROM BOOK""").fetchall()
            for item in list_books:
                age_restricted = True if item[5] == 1 else False
                book_object = Book(name=item[1],
                                   author=item[2],
                                   id=item[0],
                                   total_number_of_books=item[3],
                                   number_of_books_available=item[4],
                                   age_restricted=age_restricted)
                list_of_book_objects.append(book_object)
            return list_of_book_objects

    # List all books that have a specific word
    def list_search_book(self, book_name: str) -> list:
        list_of_book_objects = []
        with self.con:
            list_books = self.con.execute("""SELECT * FROM BOOK""").fetchall()
            for item in list_books:
                if book_name.lower() in item[1].lower():
                    age_restricted = True if item[5] == 1 else False
                    book_object = Book(name=item[1],
                                       author=item[2],
                                       id=item[0],
                                       total_number_of_books=item[3],
                                       number_of_books_available=item[4],
                                       age_restricted=age_restricted)
                    list_of_book_objects.append(book_object)

            return list_of_book_objects

    # Search for a user in the database
    def search_for_user(self, user_name: str) -> list:
        list_of_users = []

        with self.con:
            list_users = self.con.execute("""SELECT * FROM USER""").fetchall()
            for item in list_users:
                print(item[0], item[1])
                if (user_name.lower() in item[1].lower()) or (user_name.lower() in item[2].lower()):
                    user_obj = User(user_id=item[0],
                                    first_name=item[1],
                                    last_name=item[2],
                                    date_of_birth=item[3],
                                    mail_address=item[4],
                                    phone_number=item[5],
                                    address=item[6])
                    list_of_users.append(user_obj)
                    print(item[0])

        return list_of_users

    # Update borrow books number for a user in the database
    def update_borrow_books_number_for_user(self, user_id: int) -> None:
        new_books_borrowed_nr = int(self.get_number_of_previous_books_borrowed_by_user(user_id)) + 1
        with self.con:
            self.con.execute("""UPDATE USER SET number_of_books_borrowed = ? WHERE id = ?""",
                             (str(new_books_borrowed_nr), str(user_id)))

    # Update list_of_books_currently_borrowed for USER in database
    def update_list_of_books_currently_borrowed_by_user(self, user_id: int, borrowed_book_id: int) -> None:
        with self.con:
            books_currently_borrowed_list = list(
                str(self.con.execute("""SELECT list_of_books_currently_borrowed FROM USER WHERE ID=?""",
                                     str(user_id)).fetchone()[0]).split(","))

            print(books_currently_borrowed_list)
            if "-" in books_currently_borrowed_list:
                books_currently_borrowed_list.remove("-")
            books_currently_borrowed_list.append(str(borrowed_book_id))

            new_list_of_borrowed_books = ",".join(books_currently_borrowed_list)

            self.con.execute("""UPDATE USER SET list_of_books_currently_borrowed = ? WHERE id = ?""",
                             (new_list_of_borrowed_books, str(user_id)))

    # Get user by id
    def get_user_by_id(self, user_id: int) -> User:
        with self.con:
            user_details = self.con.execute("""SELECT * FROM USER WHERE id = ?""",
                             str(user_id)).fetchone()

            user_obj = User(user_id=user_details[0],
                            first_name=user_details[1],
                            last_name=user_details[2],
                            date_of_birth=user_details[3],
                            mail_address=user_details[4],
                            phone_number=user_details[5],
                            address=user_details[6],
                            number_of_books_borrowed=int(user_details[7]),
                            list_of_books_borrowed_and_returned=user_details[8],
                            list_of_books_currently_borrowed=user_details[9])

        return user_obj

    # Return book
    def return_book(self, book_id: int, user_id: int) -> None:
        available_books_nr_after_return = int(self.get_available_books_number(book_id=book_id)) + 1

        with self.con:
            self.con.execute("""UPDATE BOOK SET number_of_books_available = ? WHERE id = ?""",
                             (str(available_books_nr_after_return), str(book_id)))
            print("The book with ID: " + str(book_id) + " is returned. Available books: " +
                  str(available_books_nr_after_return))

    def update_return_date_of_borrowed_book(self, borrowed_book_id: int) -> None:
        with self.con:
            self.con.execute("""UPDATE BORROWED_BOOKS SET date_of_return = ? WHERE id = ?""",
                             (str(datetime.now()), str(borrowed_book_id)))


    #  ------------------------
    #  TO DO: not finished yet
    #  -------------------------

    # Identify the book id based on the borrowed id, to use it for return book
    def identify_book_id_for_return(self, borrowed_book_id: int) -> int:
        # db borrowed books adaug data la date of return -> DONE
        # db book adaug cartea inapoi la available
        # db user scad number of books borrowed
        # db user adaug id book borrowed din db borrows books la list of books borrowed and return
        # db user scot id din list of books currently borrowed (in functie de ce id are cartea imprumutata in db borrowed books)

        pass
    #  ------------------------
    #  TO DO: not finished yet
    #  -------------------------
