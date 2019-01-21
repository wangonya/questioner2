import os

from werkzeug.security import generate_password_hash

from ..utils.validators import DbValidators


class AuthModel:
    """model for auth tables"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cnxn.autocommit = True
    cursor = cnxn.cursor()

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
