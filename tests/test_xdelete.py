from .conftest import delete


def test_delete(main, dev_cursor):
    """test delete meetup endpoint"""
    dev_cursor.execute('SELECT * '
                       'FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
    meetup = dev_cursor.fetchone()

    res = delete(main, "/api/v2/meetups/{}".format(meetup["id"]))
    assert res.status_code == 200
    assert b"Delete successful" in res.data
