import pytest

from app.utils import error_handlers, validators
from app.auth.models import AuthModel


def test_db_connection_error():
    """test that an exception is raised if there's an error connecting to the database"""
    with pytest.raises(error_handlers.DatabaseConnectionError):
        validators.DbValidators.connect_to_db("bad-db-uri-to-check-exception-raise")


def test_table_creation_error(cnxn, cursor):
    """test that an exception is raised if there's an error creating the db tables"""
    sttmt = ""
    with pytest.raises(error_handlers.TableCreationError):
        validators.DbValidators.create_tables(cnxn, cursor, sttmt)


def test_invalid_email_format():
    """test that an exception is raised if an invalid email format is passed in"""
    with pytest.raises(error_handlers.InvalidEmailFormatError):
        validators.AuthValidators.check_email_format("bademail.com")


def test_invalid_password():
    """test that an exception is raised if a short password is passed in"""
    with pytest.raises(error_handlers.InvalidPasswordLengthError):
        validators.AuthValidators.check_password_length("pass")


def test_signup_duplicate_user():
    """test that an exception is raised if an email that already exists is passed in during signup"""
    with pytest.raises(error_handlers.UserAlreadyExistsError):
        validators.AuthValidators.check_email_exists("test@gmail.com")


def test_login_email_check():
    """test that an exception is raised if the email passed in during login is not registered"""
    with pytest.raises(error_handlers.UserLoginError):
        validators.AuthValidators.confirm_login_email("bademail@gmail.com")


def test_login_password_check():
    """test that an exception is raised if an invalid password is passed in"""
    with pytest.raises(error_handlers.UserLoginError):
        assert AuthModel.verify_hash("admin@questioner.com", "badpass")

    with pytest.raises(error_handlers.UserLoginError):
        assert AuthModel.verify_hash("bademail.com", "badpass")


def test_meetups_post_admin(dev_cursor):
    """test that an exception is raised if a non-admin user tries to post a meetup"""
    with pytest.raises(error_handlers.AdminProtectedError):
        dev_cursor.execute('SELECT * '
                           'FROM users '
                           'WHERE email = (%s)', ("test@gmail.com",))
        creator = dev_cursor.fetchone()
        assert validators.MeetupValidators.check_creator_is_admin(creator)

    dev_cursor.execute('DELETE FROM users '
                       'WHERE email = (%s)', ("test@gmail.com",))
