import os
import json
import pytest
import psycopg2

from psycopg2.extras import RealDictCursor
from flask_jwt_extended import create_access_token

import app
from app.auth.models import AuthModel
from app.meetups.models import MeetupModel, RsvpsModel
from app.db import InitDb
from app.utils.validators import DbValidators
from app.questions.models import PostQuestionsModel, VoteModel, AnswerQuestionsModel


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
    tables = InitDb.tables
    DbValidators.create_tables(cnxn, cursor, *tables)
    default_admin = {
        "firstname": "fname",
        "lastname": "lname",
        "email": "admin@questioner.com",
        "phonenumber": "23432432",
        "password": "q_admin",
        "username": "admin",
        "is_admin": True
    }
    create_admin = ('INSERT INTO users '
                    '(firstname, lastname, email, phonenumber, '
                    'password, username, is_admin) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                    'ON CONFLICT DO NOTHING;')
    cursor.execute(create_admin,
                   (default_admin["firstname"], default_admin["lastname"], default_admin["email"],
                    default_admin["phonenumber"], default_admin["password"],
                    default_admin["username"], default_admin["is_admin"]))
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
    meetup = MeetupModel("sample meetup", creator["id"], "test location", "2029-01-22", "test tag", "test image")
    yield meetup


@pytest.fixture
def new_question(cursor):
    """reuse this in question test to test post new question"""
    cursor.execute('SELECT * '
                   'FROM meetups '
                   'WHERE title = (%s)', ("sample meetup",))
    meetup = cursor.fetchone()
    question = PostQuestionsModel("test title", 1, "test question body", meetup["id"])
    yield question


@pytest.fixture
def new_vote(cursor):
    """reuse this in vote test to test post new vote"""
    cursor.execute('SELECT * '
                   'FROM questions '
                   'WHERE title = (%s)', ("test title",))
    question = cursor.fetchone()
    vote = VoteModel(1, question["id"], 1)
    yield vote


@pytest.fixture
def new_comment(cursor):
    """reuse this in comment test to test post new comment"""
    cursor.execute('SELECT * '
                   'FROM questions '
                   'WHERE title = (%s)', ("test title",))
    question = cursor.fetchone()
    comment = AnswerQuestionsModel("test comment", question["creator"],
                                   question["meetup"], question["id"])
    yield comment


@pytest.fixture
def new_rsvp(cursor):
    """reuse this in rsvp test to test post new rsvp"""
    cursor.execute('SELECT * '
                   'FROM meetups '
                   'WHERE title = (%s)', ("sample meetup",))
    meetup = cursor.fetchone()
    rsvp = RsvpsModel("yes", 1, meetup["id"])
    yield rsvp


def post_json(main, url, json_dict):
    """helper function to post a json dict to the specified url """
    access_token = create_access_token('admin@questioner.com')
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return main.post(url, data=json.dumps(json_dict), content_type='application/json', headers=headers)


def delete(main, url):
    """helper function to delete data in the specified url"""
    access_token = create_access_token('admin@questioner.com')
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return main.delete(url, headers=headers)


def admin_get(main, url):
    """helper function to get admin protected data in the specified url"""
    access_token = create_access_token('admin@questioner.com')
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return main.get(url, headers=headers)


def patch_json(main, url, json_dict):
    """helper function to patch a json dict to the specified url """
    access_token = create_access_token('admin@questioner.com')
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return main.patch(url, data=json.dumps(json_dict), content_type='application/json', headers=headers)
