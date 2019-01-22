import datetime

from .conftest import post_json


def test_sign_up(new_user, cursor, main):
    """test signup endpoint"""
    insert_query = ('INSERT INTO users '
                    '(firstname, lastname, email, phonenumber, '
                    'password, username) '
                    'VALUES (%s, %s, %s, %s, %s, %s);')
    cursor.execute(insert_query,
                   (new_user.firstname, new_user.lastname, new_user.email,
                    new_user.phonenumber, new_user.password, new_user.username))

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

    res = post_json(main, "/api/v2/auth/signup", new_user.__dict__)
    assert res.status_code == 201
    assert b"user registered successfully" in res.data


def test_login(cursor, main):
    """test login endpoint"""
    test_data = {
        "email": "admin@questioner.com",
        "password": "q_admin"
    }
    res = post_json(main, "/api/v2/auth/login", test_data)
    assert res.status_code == 200
    assert b"user logged in successfully" in res.data

    cursor.execute('TRUNCATE TABLE users;')
