import re
import psycopg2

from .error_handlers import (DatabaseConnectionError, TableCreationError, InvalidEmailFormatError,
                             UserAlreadyExistsError, InvalidPasswordLengthError, UserLoginError,
                             DuplicateDataError, AdminProtectedError, NoDataError, InvalidRsvpStatusError)


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
        from ..auth.models import AuthModel
        if AuthModel.find_by_email(email):
            raise UserAlreadyExistsError

    @staticmethod
    def confirm_login_email(email):
        """check if email already exists for login validation"""
        from ..auth.models import AuthModel
        if not AuthModel.find_by_email(email):
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
        from ..meetups.models import MeetupModel
        if MeetupModel.find_meetup(title):
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
            raise NoDataError


class QuestionValidators:
    """question methods validators"""
    @staticmethod
    def check_duplicate_question(title):
        """check if a question with the same title already exists"""
        from ..questions.models import PostQuestionsModel
        if PostQuestionsModel.find_question(title):
            raise DuplicateDataError

    @staticmethod
    def check_question_exists(q_id):
        """check if the requested question exists"""
        from ..questions.models import VoteModel
        if not VoteModel.get_specific_question(q_id):
            raise NoDataError


class RsvpValidators:
    """rsvp validators"""
    @staticmethod
    def check_proper_rsvp(status):
        """rsvp status should only be 'yes', 'no', or 'maybe'"""
        if status not in ("yes", "no", "maybe"):
            raise InvalidRsvpStatusError


class AnswerValidators:
    """answers validators"""
    @staticmethod
    def check_duplicate_answer(body, q_id):
        """check if an answer with similar body exists in same question"""
        from ..questions.comment import AnswerQuestionsModel
        if AnswerQuestionsModel.find_duplicate_answer(body, q_id):
            raise DuplicateDataError
