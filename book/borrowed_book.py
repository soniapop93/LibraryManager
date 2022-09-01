class BorrowedBook:
    def __init__(self,
                 book_id: int,
                 status: str,
                 date_of_borrow: str,
                 date_of_return: str,
                 user_id_that_borrowed_the_book: int):
        self.book_id = book_id
        self.status = status
        self.date_of_borrow = date_of_borrow
        self.date_of_return = date_of_return
        self.user_id_that_borrowed_the_book = user_id_that_borrowed_the_book
