import datetime
import pytest

from .conftest import post_json
from app.utils import error_handlers, validators


def test_post_meetup(new_meetup, cursor, main):
    """test post meetup endpoint"""
    insert_query = ('INSERT INTO meetups '
                    '(title, creator, location, happening_on, '
                    'tags, image) '
                    'VALUES (%s, %s, %s, %s, %s, %s);')
    cursor.execute(insert_query,
                   (new_meetup.title, new_meetup.creator, new_meetup.location,
                    new_meetup.happening_on, new_meetup.tags, new_meetup.image))

    cursor.execute('SELECT * FROM meetups;')
    data = cursor.fetchone()
    assert isinstance(data["id"], int)
    assert new_meetup.title == data["title"] == "sample meetup"
    assert isinstance(data["creator"], int)
    assert new_meetup.location == data["location"] == "test location"
    assert isinstance(data["happening_on"], datetime.date)
    assert new_meetup.tags[0] == data["tags"] == "test tag"
    assert new_meetup.image == data["image"] == "test image"

    res = post_json(main, "/api/v2/meetups", new_meetup.__dict__)
    assert res.status_code == 201
    assert b"meetup created successfully" in res.data


def test_duplicate_meetup():
    """check duplicate meetup"""
    with pytest.raises(error_handlers.DuplicateDataError):
        assert validators.MeetupValidators.check_duplicate_meetup("sample meetup")


def test_get_upcoming_meetups(main):
    """test view upcoming meetups"""
    res = main.get('/api/v2/meetups/upcoming')
    assert res.status_code == 200


def test_specific_meetup(main, dev_cursor):
    """test view specific meetup"""
    dev_cursor.execute('SELECT * '
                       'FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
    meetup = dev_cursor.fetchone()
    res = main.get('/api/v2/meetups/{}'.format(meetup["id"]))
    assert res.status_code == 200


def test_specific_meetup_not_found(main):
    """test that a 404 is returned if the meetup does not exist"""
    res = main.get('/api/v2/meetups/7688')
    assert res.status_code == 404
