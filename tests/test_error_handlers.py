import os
import pytest

from app.utils import error_handlers, validators
from app.db import CreateTables


def test_db_error_handlers(capsys):
    """test db error handlers"""

    # first pass in correct db parameters to test the try block

    # db connection
    cnxn = validators.DbValidators.connect_to_db(os.getenv("TESTING_DB_URI"))
    cnxn_parameters = cnxn.get_dsn_parameters()
    assert cnxn_parameters.get("dbname") == "questioner_test"
    cursor = cnxn.cursor()
    assert cursor
    captured = capsys.readouterr()
    assert captured.out == "Connection successful\n"

    # table creation
    tables = CreateTables.tables
    validators.DbValidators.create_tables(cnxn, cursor, *tables)
    captured = capsys.readouterr()
    assert captured.out == "Tables created successfully\n"

    # now pass in incorrect db parameters to make sure an exception is raised

    # db connection
    with pytest.raises(error_handlers.DatabaseConnectionError) as err:
        validators.DbValidators.connect_to_db("bad-db-uri-to-check-exception-raise")

    assert str(err.value) == "500 Internal Server Error: " \
                             "An error occurred while connecting to the database"

    # table creation
    sttmt = ""  # passing in empty string to make it fail
    with pytest.raises(error_handlers.TableCreationError) as err:
        validators.DbValidators.create_tables(cnxn, cursor, sttmt)

    assert str(err.value) == "500 Internal Server Error: " \
                             "An error occurred while creating the tables"
