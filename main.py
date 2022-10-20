from db.database_manager import DataBaseManager

# Create db connection object
conn = DataBaseManager()
running = True  # to run in loop, will break only for Exit option


# Display home menu options
def display_home_menu() -> str:
    home_menu = input(
        "Select the following options: \n"
        "1 - Add new user\n"
        "2 - Add new book\n"
        "3 - Borrow_book\n"
        "4 - Return book\n"
        "5 - Update existing books number\n"
        "6 - List all books\n"
        "7 - Exit\n"
        "Option number: ")
    return home_menu


# Add new user
def add_new_user() -> None:
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    date_of_birth = input("Date of birth(dd/MM/yyyy)")
    mail_address = input("Mail address: ")
    phone_number = input("Phone number: ")
    address = input("Address: ")
    conn.add_user_in_db(first_name, last_name, date_of_birth, mail_address, phone_number, address)
    print("User is added in the database")


# Add new book
def add_new_book() -> None:
    name = input("Name of the book: ")
    author = input("Author name: ")
    total_number_of_books = int(input("Books quantity: "))
    age_restricted = bool(input("Age restricted book? (True/False) "))
    conn.add_book_in_db(name, author, total_number_of_books, age_restricted)
    print("Book is added in the database")


# Display book
def output_book(id: int,
                name: str,
                author: str,
                total_number_of_books: int,
                number_of_books_available: int,
                age_restricted: bool) -> str:
    output_str = "ID: " + str(id) + "\n" + \
                 "Name: " + name + "\n" + \
                 "Author: " + author + "\n" + \
                 "Total number of books: " + str(total_number_of_books) + "\n" + \
                 "Number of books available: " + str(number_of_books_available) + "\n" + \
                 "Age restricted: " + str(age_restricted) + "\n"
    return output_str


#  Display user
def output_user(user_id: int,
                first_name: str,
                last_name: str,
                date_of_birth: str,
                mail_address: str,
                phone_number: str,
                address: str) -> str:
    string_output = "User ID: " + str(user_id) + "\n" + \
                    "Name: " + first_name + " " + last_name + "\n" + \
                    "Date of birth: " + date_of_birth + "\n" + \
                    "Mail address: " + mail_address + "\n" + \
                    "Phone number: " + phone_number + "\n" + \
                    "Address: " + address + "\n"
    return string_output


# Select book for borrowing
def selected_book_for_borrowing(user_id: int) -> None:
    borrow_book_input = int(input("Please add the book ID you want to borrow: "))
    conn.borrowing_book(book_id=borrow_book_input)
    borrowed_book_id = conn.insert_borrowed_book_into_borrowed_book_table(book_id=borrow_book_input, user_id=user_id)
    conn.update_borrow_books_number_for_user(user_id=user_id)
    conn.update_list_of_books_currently_borrowed_by_user(user_id=user_id, borrowed_book_id=borrowed_book_id)


# Borrow book by user
def borrow_book() -> None:
    search_user = input("Do you want to search for a user? (Y/N)")

    if search_user.lower() == "y":
        search_user_name_input = input("Please add the name you want to search for: ")

        list_of_searched_users = conn.search_for_user(search_user_name_input)

        for item in list_of_searched_users:
            print("________________________________________")
            print(output_user(item.user_id,
                              item.first_name,
                              item.last_name,
                              item.date_of_birth,
                              item.mail_address,
                              item.phone_number,
                              item.address))

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
    selected_book_for_borrowing(user_id)


# Return book
def return_book() -> None:
    add_user_id = input("Please add user id: ")
    user_obj = conn.get_user_by_id(int(add_user_id))
    print("User identified. Details: \n" + user_obj.str_output(
        user_id=user_obj.user_id,
        first_name=user_obj.first_name,
        last_name=user_obj.last_name,
        date_of_birth=user_obj.date_of_birth,
        mail_address=user_obj.mail_address,
        phone_number=user_obj.phone_number,
        address=user_obj.address,
        number_of_books_borrowed=int(user_obj.number_of_books_borrowed),
        list_of_books_borrowed_and_returned=user_obj.list_of_books_borrowed_and_returned,
        list_of_books_currently_borrowed=user_obj.list_of_books_currently_borrowed))

    id_of_borrowed_book_to_be_returned = input("Please add the id of the borrowed book you want to return: ")

    conn.update_return_date_of_borrowed_book(int(id_of_borrowed_book_to_be_returned))





# Update an existing book number with new values
def add_new_book_to_existing_one() -> None:
    list_books = input("Do you want to list or search for the book you want to update? (Y/N)")

    if list_books.lower() == "y":
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
    update_book_id = input("Please add the book id you want to update: ")
    new_book_nr = int(input("Please add the new book number you received: "))
    conn.add_books_to_existing_ones(book_id=int(update_book_id), new_book_number=new_book_nr)


# Option meniu decisions
def decision_options(option_number: str) -> bool:
    # Add new user
    if option_number == "1":
        add_new_user_input = input("Do you want to add a new user? (Y/N): ")
        if add_new_user_input.lower() == "y":
            add_new_user()

    # Add new book
    elif option_number == "2":
        add_new_book_input = input("Do you want to add a new book? (Y/N): ")
        if add_new_book_input.lower() == "y":
            add_new_book()

    # Borrow book
    elif option_number == "3":
        add_borrow_book_input = input("Do you want to borrow a book? (Y/N)")
        if add_borrow_book_input.lower() == "y":
            borrow_book()

    # Return book
    elif option_number == "4":
        add_return_book_input = input("Do you want to return a book? (Y/N)")
        if add_return_book_input.lower() == "y":
            return_book()

    # Update books number
    elif option_number == "5":
        add_new_nr_book_input = input("Do you want to add new books to an existing one? (Y/N)")
        if add_new_nr_book_input.lower() == "y":
            add_new_book_to_existing_one()

    # List all books in the DB
    elif option_number == "6":
        print("----------------------------------------------------------------------\n")
        db_list_of_books = conn.list_all_books_from_db()

        for book in db_list_of_books:
            print(output_book(book.id, book.name, book.author, book.total_number_of_books,
                              book.number_of_books_available, book.age_restricted))
            print("----------------------------------------------------------------------\n")

    # Exit
    elif option_number == "7":
        print("EXIT")
        global running
        running = False
        return running


while running:
    home_menu = display_home_menu()
    option_return = decision_options(home_menu)
    print("**********************************************************")
