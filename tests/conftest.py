import os
import json
import pytest
import psycopg2

from psycopg2.extras import RealDictCursor
from flask_jwt_extended import create_access_token

import app
from app.auth.models import AuthModel
from app.meetups.models import MeetupModel
from app.db import CreateTables
from app.utils.validators import DbValidators
from app.questions.models import PostQuestionsModel


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


@pytest.fixture
def new_meetup(dev_cursor):
    """reuse this in meetup test to test MeetupModel post new meetup"""
    dev_cursor.execute('SELECT * '
                       'FROM users '
                       'WHERE is_admin = (%s)', (True,))
    creator = dev_cursor.fetchone()
    meetup = MeetupModel("sample meetup", creator["id"], "test location", "2019-01-22", "test tag", "test image")
    yield meetup


@pytest.fixture
def new_question():
    """reuse this in question test to test post new question"""
    meetup = PostQuestionsModel("test title", 1, "test question body", 1)
    yield meetup


def post_json(main, url, json_dict):
    """helper function to send a json dict to the specified url """
    access_token = create_access_token('admin@questioner.com')
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return main.post(url, data=json.dumps(json_dict), content_type='application/json', headers=headers)
