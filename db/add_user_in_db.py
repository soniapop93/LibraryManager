import sqlite3 as sl
import os


class DataBaseManager:
    def __init__(self):
        if os.path.exists("libraryDB.db") is False:
            self.con = sl.connect("libraryDB.db")
            self.create_user_db()
            self.create_book_db()
        else:
            self.con = sl.connect("libraryDB.db")

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
                        list_of_books_borrowed TEXT);
                        """)

    def generate_id(self, previous_id):
        return previous_id + 1

    def get_previous_user_id(self):
        with self.con:
            try:
                previous_user_id = self.con.execute("""SELECT id FROM USER ORDER BY id DESC LIMIT 1;""").fetchone()
                return previous_user_id[0]
            except TypeError:
                return 0

    def add_data_in_db(self, sql, data):
        with self.con:
            self.con.execute(sql, data)


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

    def get_previous_book_id(self):
        with self.con:
            try:
                previous_book_id = self.con.execute("""SELECT id FROM BOOK ORDER BY id DESC LIMIT 1;""").fetchone()
                return previous_book_id[0]
            except TypeError:
                return 0
