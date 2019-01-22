import os
import pytest

from app.utils import error_handlers, validators
from app.db import CreateTables


def test_db_error_handlers(capsys):
    """test db error handler. first pass in correct db parameters to test the try blocks
    then pass in incorrect details to check that exception is actually raised"""
    cnxn = validators.DbValidators.connect_to_db(os.getenv("TESTING_DB_URI"))
    cnxn_parameters = cnxn.get_dsn_parameters()
    assert cnxn_parameters.get("dbname") == "questioner_test"
    cursor = cnxn.cursor()
    assert cursor
    captured = capsys.readouterr()
    assert captured.out == "Connection successful\n"

    tables = CreateTables.tables
    validators.DbValidators.create_tables(cnxn, cursor, *tables)
    captured = capsys.readouterr()
    assert captured.out == "Tables created successfully\n"

    with pytest.raises(error_handlers.DatabaseConnectionError) as err:
        validators.DbValidators.connect_to_db("bad-db-uri-to-check-exception-raise")

    assert str(err.value) == "500 Internal Server Error: " \
                             "An error occurred while connecting to the database"

    sttmt = ""
    with pytest.raises(error_handlers.TableCreationError) as err:
        validators.DbValidators.create_tables(cnxn, cursor, sttmt)

    assert str(err.value) == "500 Internal Server Error: " \
                             "An error occurred while creating the tables"


def test_auth_validators(dev_cursor):
    """test auth validators"""
    with pytest.raises(error_handlers.InvalidEmailFormatError) as err:
        validators.AuthValidators.check_email_format("bademail.com")

    assert str(err.value) == "400 Bad Request: " \
                             "Invalid email format"

    with pytest.raises(error_handlers.InvalidPasswordLengthError) as err:
        validators.AuthValidators.check_password_length("pass")

    assert str(err.value) == "400 Bad Request: " \
                             "Password length has to be at least 6 characters"

    with pytest.raises(error_handlers.UserAlreadyExistsError) as err:
        validators.AuthValidators.check_email_exists("test@gmail.com")

    assert str(err.value) == "409 Conflict: " \
                             "A user with that email already exists"

    dev_cursor.execute('DELETE FROM users '
                       'WHERE email = (%s)', ("test@gmail.com",))
