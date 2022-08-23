from user.user import User
from book.book import Book

list_of_users = []
list_of_books = []

new_user = User(1,"John", "Smith", "01/07/1993", "john_smithgmail.com", "07464512427", "str Principala", 0, "")

list_of_users.append(new_user)

print(list_of_users[0])

new_book = Book("China Study", "T. Colin Campbel", 1, 5, 5, False)

list_of_books.append(new_book)
print(list_of_books[0])