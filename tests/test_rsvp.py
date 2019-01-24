from .conftest import post_json


def test_post_rsvp(new_rsvp, cursor, main, dev_cursor):
    """test post rsvp endpoint"""
    insert_query = ('INSERT INTO rsvps '
                    '(status, creator, meetup) '
                    'VALUES (%s, %s, %s);')
    cursor.execute(insert_query,
                   (new_rsvp.status, new_rsvp.uid, new_rsvp.m_id))

    cursor.execute('SELECT * FROM rsvps;')
    data = cursor.fetchone()
    assert isinstance(data["id"], int)
    assert new_rsvp.status == data["status"] == "yes"
    assert isinstance(data["creator"], int)
    assert isinstance(data["meetup"], int)

    dev_cursor.execute('SELECT * '
                       'FROM meetups '
                       'WHERE title = (%s)', ("sample meetup",))
    meetup = dev_cursor.fetchone()

    res = post_json(main, "/api/v2/meetups/{}/rsvps".format(meetup["id"]), new_rsvp.__dict__)
    assert res.status_code == 201
    assert b"meetup rsvp successful" in res.data

    cursor.execute('TRUNCATE rsvps RESTART IDENTITY;')
