import os
import json
import pytest
import psycopg2

from psycopg2.extras import RealDictCursor

import app
from app.auth.models import AuthModel
from app.db import CreateTables
from app.utils.validators import DbValidators


@pytest.fixture
def main():
    """setup testing module with testing config"""
    test = app.create_app("testing")

    with test.app_context():
        yield test.test_client()


@pytest.fixture
def cnxn(main):
    """testdb connection fixture"""
    cnxn = psycopg2.connect(os.getenv("TESTING_DB_URI"))
    cnxn.autocommit = True
    yield cnxn
    cnxn.close()


@pytest.fixture
def cursor(cnxn):
    """testdb cursor fixture"""
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)
    tables = CreateTables.tables
    DbValidators.create_tables(cnxn, cursor, *tables)
    yield cursor
    cnxn.rollback()


@pytest.fixture
def dev_cnxn(main):
    """testdb connection fixture"""
    dev_cnxn = psycopg2.connect(os.getenv("DEV_DB_URI"))
    dev_cnxn.autocommit = True
    yield dev_cnxn
    dev_cnxn.close()


@pytest.fixture
def dev_cursor(dev_cnxn):
    """testdb cursor fixture"""
    dev_cursor = dev_cnxn.cursor(cursor_factory=RealDictCursor)
    yield dev_cursor
    dev_cnxn.rollback()


@pytest.fixture
def new_user():
    """reuse this in auth test to test AuthModel user registration"""
    user = AuthModel('fname', 'lname', 'test@gmail.com', '23432432', 'test_pass!')
    yield user


# helper functions dealing with data
def post_json(main, url, json_dict):
    """send a json dict to the specified url """
    return main.post(url, data=json.dumps(json_dict), content_type='application/json')
