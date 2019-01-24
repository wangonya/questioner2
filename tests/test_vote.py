import pytest

from .conftest import patch_json
from app.utils import error_handlers, validators


def test_upvote(main, cursor, new_vote, dev_cursor):
    """test upvote endpoint"""
    insert_query = ('INSERT INTO votes '
                    '(creator, question, count) '
                    'VALUES (%s, %s, %s);')
    cursor.execute(insert_query,
                   (new_vote.user, new_vote.question,
                    new_vote.vote))

    cursor.execute('SELECT * FROM votes;')
    data = cursor.fetchone()
    assert isinstance(data["id"], int)
    assert isinstance(data["creator"], int)
    assert isinstance(data["question"], int)
    assert isinstance(data["count"], int)

    dev_cursor.execute('SELECT * '
                       'FROM questions '
                       'WHERE title = (%s)', ("test title",))
    question = dev_cursor.fetchone()

    res = patch_json(main, "/api/v2/questions/{}/upvote".format(question["id"]), new_vote.__dict__)
    assert res.status_code == 201
    assert b"vote added successfully" in res.data

    res = patch_json(main, "/api/v2/questions/{}/upvote".format(question["id"]), new_vote.__dict__)
    assert res.status_code == 201
    assert b"vote added successfully" in res.data


def test_downvote(main, new_vote, dev_cursor):
    """test downvote endpoint"""
    dev_cursor.execute('SELECT * '
                       'FROM questions '
                       'WHERE title = (%s)', ("test title",))
    question = dev_cursor.fetchone()

    res = patch_json(main, "/api/v2/questions/{}/downvote".format(question["id"]), new_vote.__dict__)
    assert res.status_code == 201
    assert b"vote added successfully" in res.data

    res = patch_json(main, "/api/v2/questions/{}/downvote".format(question["id"]), new_vote.__dict__)
    assert res.status_code == 201
    assert b"vote added successfully" in res.data

    dev_cursor.execute('DELETE FROM questions '
                       'WHERE title = (%s)', ("test title",))

    dev_cursor.execute('DELETE FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
