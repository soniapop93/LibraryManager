from db.add_user_in_db import DataBaseManager


conn = DataBaseManager()

sql_user = 'INSERT INTO USER (id, first_name,last_name, date_of_birth, mail_address, phone_number, address, ' \
      'number_of_books_borrowed, list_of_books_borrowed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'

new_user_id = conn.generate_id(conn.get_previous_user_id())

data_user = [new_user_id,"John", "Smith", "09/08/1993", "john_smoth@gmail.com", "0746436627", "str Princiapala", 0, ""]

conn.add_data_in_db(sql_user, data_user)

sql_book = 'INSERT INTO BOOK (id, name,author, total_number_of_books, number_of_books_available, age_restricted) ' \
      'VALUES(?, ?, ?, ?, ?, ?)'

new_book_id = conn.generate_id(conn.get_previous_book_id())

data_book = [new_book_id,"China Study", "T Campbell", "5", "5", False]

conn.add_data_in_db(sql_book, data_book)