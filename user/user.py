import re

class User:
    def __init__(self,
                 user_id: int,
                 first_name: str,
                 last_name: str,
                 date_of_birth: str,
                 mail_address: str,
                 phone_number: str,
                 address: str,
                 number_of_books_borrowed: int,
                 list_of_books_borrowed: list):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.mail_address = mail_address
        self.phone_number = phone_number
        self.address = address
        self.number_of_books_borrowed = number_of_books_borrowed
        self.list_of_books_borrowed = list_of_books_borrowed

    def __str__(self):
        return self.str_output(self.user_id,
                               self.first_name,
                               self.last_name,
                               self.date_of_birth,
                               self.mail_address,
                               self.phone_number,
                               self.address,
                               self.number_of_books_borrowed,
                               self.list_of_books_borrowed)

    def str_output(self,
                   user_id: int,
                   first_name: str,
                   last_name: str,
                   date_of_birth: str,
                   mail_address: str,
                   phone_number: str,
                   address: str,
                   number_of_books_borrowed: int,
                   list_of_books_borrowed: list):

        mail_address = mail_address if self.verify_mail_address(mail_address) else "-"
        phone_number = phone_number if self.verify_phone_number(phone_number) else "-"

        string_output = "User ID: " + str(user_id) + "\n" + \
                        "Name: " + first_name + " " + last_name + "\n" + \
                        "Date of birth: " + date_of_birth + "\n" + \
                        "Mail address: " + mail_address + "\n" + \
                        "Phone number: " + phone_number + "\n" + \
                        "Address: " + address + "\n" + \
                        "Number of books borrowed: " + str(number_of_books_borrowed) + "\n" + \
                        "List of books borrowed: " + ", ".join(list_of_books_borrowed)
        return string_output

    def verify_mail_address(self, mail_address: str):
        regex_mail_pattern = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08" \
                             r"\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")" \
                             r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|" \
                             r"\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]" \
                             r"?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09" \
                             r"\x0b\x0c\x0e-\x7f])+)\])"
        try:
            regex_matched_mail_group = re.match(regex_mail_pattern, mail_address)
            return regex_matched_mail_group.group(0) == mail_address
        except AttributeError:
            return False


    def verify_phone_number(self, phone_number: str):
        regex_phone_pattern = r"^\d{10}$"

        try:
            regex_matched_phone = re.match(regex_phone_pattern, phone_number)
            return regex_matched_phone.group(0) == phone_number
        except AttributeError:
            return False