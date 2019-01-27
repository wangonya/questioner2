import re
import psycopg2
import datetime

from .error_handlers import (DatabaseConnectionError, TableCreationError, InvalidEmailFormatError,
                             UserAlreadyExistsError, InvalidPasswordLengthError, UserLoginError,
                             DuplicateDataError, AdminProtectedError, InvalidRsvpStatusError,
                             MeetupIdDoesNotExist, QuestionIdDoesNotExist)


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
        """check if email already exists to avoid duplicates.
        Authmodel imported here instead of at the top to circumvent circular import loop"""
        from ..db.select import SelectDataFromDb
        if SelectDataFromDb.conditional_where_select("users", "email", email):
            raise UserAlreadyExistsError

    @staticmethod
    def confirm_login_email(email):
        """check if email already exists for login validation"""
        from ..db.select import SelectDataFromDb
        if not SelectDataFromDb.conditional_where_select("users", "email", email):
            raise UserLoginError

    @staticmethod
    def check_password_length(password):
        """check that password is appropriate length"""
        if len(password) < 6:
            raise InvalidPasswordLengthError


class MeetupValidators:
    """meetup methods validators"""
    @staticmethod
    def check_duplicate_meetup(title):
        """check if a meetup with the same title already exists"""
        from ..db.select import SelectDataFromDb
        if SelectDataFromDb.conditional_where_select("meetups", "title", title):
            raise DuplicateDataError

    @staticmethod
    def check_creator_is_admin(creator):
        """check if the user posting the meetup is an admin"""
        if not creator["is_admin"]:
            raise AdminProtectedError

    @staticmethod
    def check_meetup_exists(m_id):
        """check if the requested meetup exists"""
        from ..meetups.models import MeetupModel
        if not MeetupModel.get_specific_meetup(m_id):
            raise MeetupIdDoesNotExist


class QuestionValidators:
    """question methods validators"""
    @staticmethod
    def check_duplicate_question(title, m_id):
        """check if a question with the same title already exists"""
        from ..db.select import SelectDataFromDb
        if SelectDataFromDb.conditional_where_and_select("questions", "title", title, "meetup", m_id):
            raise DuplicateDataError

    @staticmethod
    def check_question_exists(q_id):
        """check if the requested question exists"""
        from ..db.select import SelectDataFromDb
        if not SelectDataFromDb.conditional_where_select("questions", "id", q_id):
            raise QuestionIdDoesNotExist


class RsvpValidators:
    """rsvp validators"""
    @staticmethod
    def check_proper_rsvp(status):
        """rsvp status should only be 'yes', 'no', or 'maybe'"""
        if status not in ("yes", "Yes", "YES", "NO", "No", "no", "MAYBE", "Maybe", "maybe"):
            raise InvalidRsvpStatusError


class AnswerValidators:
    """answers validators"""
    @staticmethod
    def check_duplicate_answer(body, q_id):
        """check if an answer with similar body exists in same question"""
        from ..db.select import SelectDataFromDb
        if SelectDataFromDb.conditional_where_and_select("answers", "body", body, "question", q_id):
            raise DuplicateDataError


class GeneralValidators:
    """validators for data that doesn't belong to any particular route"""
    @staticmethod
    def non_empty_string(s):
        """check for empty strings"""
        if not s.strip():
            raise ValueError("Must not be empty string")
        return s

    @staticmethod
    def date_format(s):
        """check for date format"""
        try:
            datetime.datetime.strptime(s, '%Y-%m-%d')
            return s
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
