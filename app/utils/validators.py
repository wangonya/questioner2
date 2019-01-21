import re
import psycopg2

from .error_handlers import (DatabaseConnectionError, TableCreationError, InvalidEmailFormatError,
                             UserAlreadyExistsError, InvalidPasswordLengthError)


class DbValidators:
    """database operation validators"""
    @staticmethod
    def connect_to_db(db_uri):
        """try making a connection to the db"""
        try:
            cnxn = psycopg2.connect(db_uri)
            cnxn.autocommit = True
            print("Connection successful")
            return cnxn
        except (Exception, psycopg2.Error):
            raise DatabaseConnectionError

    @staticmethod
    def create_tables(cnxn, cursor, *tables):
        """create db tables"""
        try:
            for table in tables:
                cursor.execute(table)
            print("Tables created successfully")
        except (Exception, psycopg2.Error):
            raise TableCreationError


class AuthValidators:
    """auth methods validators"""
    @staticmethod
    def check_email_format(email):
        """check that the entered email format is correct"""
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            raise InvalidEmailFormatError

    @staticmethod
    def check_email_exists(email):
        """check if email already exists to avoid duplicates"""
        from ..auth.models import AuthModel  # imported here to circumvent circular import loop
        if AuthModel.find_by_email(email):
            raise UserAlreadyExistsError

    @staticmethod
    def check_password_length(password):
        """check that password is appropriate length"""
        if len(password) < 6:
            raise InvalidPasswordLengthError
