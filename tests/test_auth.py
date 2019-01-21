import datetime

from .conftest import post_json


def test_sign_up_valid(new_user, cursor, main):
    """test signup with valid details"""
    insert_query = ('INSERT INTO users '
                    '(firstname, lastname, email, phonenumber, '
                    'password, username) '
                    'VALUES (%s, %s, %s, %s, %s, %s);')
    cursor.execute(insert_query,
                   (new_user.firstname, new_user.lastname, new_user.email,
                    new_user.phonenumber, new_user.password, new_user.username))

    # check that values passed in are the ones in the db
    cursor.execute('SELECT * FROM users;')
    data = cursor.fetchone()
    assert isinstance(data["id"], int)
    assert new_user.firstname == data["firstname"] == "fname"
    assert new_user.lastname == data["lastname"] == "lname"
    assert new_user.email == data["email"] == "test@gmail.com"
    assert new_user.phonenumber == data["phonenumber"] == "23432432"
    assert new_user.password == data["password"] != "test_pass!"
    assert new_user.username[0] == data["username"] == "test"
    assert isinstance(data["registered"], datetime.date)

    # clear table after tests
    cursor.execute('TRUNCATE TABLE users;')

    res = post_json(main, "/api/v2/auth/signup", new_user.__dict__)
    assert res.status_code == 201
    assert b"user registered successfully" in res.data
