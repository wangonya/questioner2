from werkzeug.security import generate_password_hash, check_password_hash

from ..db import InitDb
from ..utils.error_handlers import UserLoginError


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
        insert_query = ('INSERT INTO users '
                        '(firstname, lastname, email, phonenumber, '
                        'password, username) '
                        'VALUES (%s, %s, %s, %s, %s, %s);')
        InitDb.cursor.execute(insert_query,
                              (self.firstname, self.lastname, self.email,
                               self.phonenumber, self.password, self.username))

    @staticmethod
    def verify_hash(email, unhashed):
        """decode password hash and verify that it matches the passed in password"""
        try:
            InitDb.cursor.execute('SELECT password '
                                  'FROM users '
                                  'WHERE email = (%s)', (email,))
            hashed = InitDb.cursor.fetchone()
            if not check_password_hash(hashed["password"], unhashed):
                raise UserLoginError
            else:
                return check_password_hash(hashed["password"], unhashed)
        except (AttributeError, TypeError):
            raise UserLoginError
