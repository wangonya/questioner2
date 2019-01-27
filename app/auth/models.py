from werkzeug.security import generate_password_hash, check_password_hash

from ..utils.error_handlers import UserLoginError
from ..db.insert import InsertDataToDb
from ..db.select import SelectDataFromDb


class AuthModel:
    """model for auth tables"""

    def __init__(self, firstname, lastname, email, phonenumber, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phonenumber = phonenumber
        self.password = generate_password_hash(password)
        self.username = email.split("@")[0],

    def save_to_db(self):
        """save data to db"""
        InsertDataToDb.save_data_to_db("users",
                                       "firstname", "lastname", "email",
                                       "phonenumber", "password", "username",
                                       self.firstname, self.lastname, self.email,
                                       self.phonenumber, self.password, self.username)

    @staticmethod
    def verify_hash(email, unhashed):
        """decode password hash and verify that it matches the passed in password"""
        try:
            hashed = SelectDataFromDb.conditional_where_select("users", "email", email)
            if not check_password_hash(hashed["password"], unhashed):
                raise UserLoginError
            else:
                return check_password_hash(hashed["password"], unhashed)
        except (AttributeError, TypeError):
            raise UserLoginError
