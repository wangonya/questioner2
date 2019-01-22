import os

from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from ..utils.validators import DbValidators
from ..utils.error_handlers import UserLoginError


class AuthModel:
    """model for auth tables"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cnxn.autocommit = True
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)

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
        AuthModel.cursor.execute(insert_query,
                                 (self.firstname, self.lastname, self.email,
                                  self.phonenumber, self.password, self.username))

    @classmethod
    def find_by_email(cls, email):
        """find user by email"""
        cls.cursor.execute('SELECT email '
                           'FROM users '
                           'WHERE email = (%s)', (email,))
        return cls.cursor.fetchone()

    @classmethod
    def verify_hash(cls, email, unhashed):
        """decode password hash and verify that it matches the passed in password"""
        try:
            cls.cursor.execute('SELECT password '
                               'FROM users '
                               'WHERE email = (%s)', (email,))
            hashed = cls.cursor.fetchone()
            if not check_password_hash(hashed["password"], unhashed):
                raise UserLoginError
            else:
                return check_password_hash(hashed["password"], unhashed)
        except (AttributeError, TypeError):
            raise UserLoginError
