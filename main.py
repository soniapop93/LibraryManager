from db.database_manager import DataBaseManager

conn = DataBaseManager()
running = True

def display_home_menu():
      home_menu = input(
            "Select the following options: \n1 - Add new user\n2 - Add new book \n3 - Borrow_book\n4 - Exit\nOption number: ")
      return home_menu

def add_new_user():
      first_name = input("First Name: ")
      last_name = input("Last Name: ")
      date_of_birth = input("Date of birth(dd/MM/yyyy)")
      mail_address = input("Mail address: ")
      phone_number = input("Phone number: ")
      address = input("Address: ")
      conn.add_user_in_db(first_name, last_name, date_of_birth, mail_address, phone_number, address)
      print("User is added in the database")

def add_new_book():
      name = input("Name of the book: ")
      author = input("Author name: ")
      total_number_of_books = int(input("Books quantity: "))
      age_restricted = bool(input("Age restricted book? (True/False) "))
      conn.add_book_in_db(name, author,total_number_of_books,age_restricted)
      print("Book is added in the database")

def output_book(id: int, name: str, author: str, total_number_of_books: int, number_of_books_available: int, age_restricted: bool):
      output_str = "ID: " + str(id) + "\n" + \
                   "Name: " + name + "\n" + \
                   "Author: " + author + "\n" + \
                   "Total number of books: " + str(total_number_of_books) + "\n" + \
                   "Number of books available: " + str(number_of_books_available) + "\n" + \
                   "Age restricted: " + str(age_restricted) + "\n"
      return output_str

def selected_book_for_borrowing(book_id, conn):
      borrow_book_input = input("Please add the book ID you want to borrow: ")




def borrow_book():
      user_id = int(input("Add user id that wants to borrow the book: "))
      option_list_books = input("Selection option: \n1 - List all books\n2 - Search book\nOption number: ")
      db_list_of_books = []

      if option_list_books == "1":
            print("----------------------------------------------------------------------\n")
            db_list_of_books = conn.list_all_books_from_db()

      elif option_list_books == "2":
            book_name_input_search = input("Book name to search for: ")
            db_list_of_books = conn.list_search_book(book_name_input_search)

      for book in db_list_of_books:
            print(output_book(book.id, book.name, book.author, book.total_number_of_books,
                              book.number_of_books_available, book.age_restricted))
            print("----------------------------------------------------------------------\n")


def decision_options(option_number: str):
      if option_number == "1":
            add_new_user_input = input("Do you want to add a new user? (Y/N): ")
            if add_new_user_input == "Y":
                  add_new_user()

      elif option_number == "2":
            add_new_book_input = input("Do you want to add a new book? (Y/N): ")
            if add_new_book_input == "Y":
                  add_new_book()

      elif option_number == "3":
            add_borrow_book_input = input("Do you want to borrow a book? (Y/N)")
            if add_borrow_book_input == "Y":
                  borrow_book()

      elif option_number == "4":
            print("EXIT")
            global running
            running = False
            return running

while running:
      home_menu = display_home_menu()
      option_return = decision_options(home_menu)
      print("**********************************************************")
