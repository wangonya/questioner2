import datetime
import pytest

from .conftest import post_json
from app.utils import error_handlers, validators


def test_post_question(main, cursor, new_question, dev_cursor):
    """test post question endpoint"""
    insert_query = ('INSERT INTO questions '
                    '(title, creator, body, meetup, votes) '
                    'VALUES (%s, %s, %s, %s, %s);')
    cursor.execute(insert_query,
                   (new_question.title, new_question.creator, new_question.body,
                    new_question.meetup, new_question.votes))

    cursor.execute('SELECT * FROM questions;')
    data = cursor.fetchone()
    assert isinstance(data["id"], int)
    assert new_question.title == data["title"] == "test title"
    assert isinstance(data["creator"], int)
    assert new_question.body == data["body"] == "test question body"
    assert isinstance(data["created_on"], datetime.date)
    assert isinstance(data["votes"], int)

    dev_cursor.execute('SELECT * '
                       'FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
    question = dev_cursor.fetchone()

    res = post_json(main, "/api/v2/meetups/{}/questions".format(question["id"]), new_question.__dict__)
    assert res.status_code == 201
    assert b"question submitted successfully" in res.data


def test_duplicate_question(dev_cursor):
    """test that an exception is raised if duplicate data is passed in"""
    with pytest.raises(error_handlers.DuplicateDataError) as err:
        validators.QuestionValidators.check_duplicate_question("test title")

    assert str(err.value) == "409 Conflict: " \
                             "The entered data already exists"

    dev_cursor.execute('DELETE FROM questions '
                       'WHERE title = (%s)', ("test title",))

    dev_cursor.execute('DELETE FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
