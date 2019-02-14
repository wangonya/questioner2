import os

from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor

from ..utils.validators import DbValidators


class InitDb:
    """create required db tables"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cnxn.autocommit = True
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)

    users_table = ('CREATE TABLE IF NOT EXISTS users'
                   '(id SERIAL PRIMARY KEY,'
                   'firstname VARCHAR(15) NOT NULL,'
                   'lastname VARCHAR(15) NOT NULL,'
                   'email VARCHAR(30) NOT NULL UNIQUE,'
                   'phonenumber VARCHAR(10),'
                   'username VARCHAR(10) NOT NULL,'
                   'registered DATE NOT NULL DEFAULT CURRENT_DATE,'
                   'is_admin BOOLEAN,'
                   'password VARCHAR NOT NULL );')

    meetups_table = ('CREATE TABLE IF NOT EXISTS meetups'
                     '(id SERIAL PRIMARY KEY,'
                     'title VARCHAR(50) NOT NULL,'
                     'details VARCHAR NOT NULL,'
                     'creator INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,'
                     'location VARCHAR(150) NOT NULL,'
                     'happening_on DATE NOT NULL,'
                     'created_on DATE NOT NULL DEFAULT CURRENT_DATE,'
                     'tags VARCHAR(50),'
                     'image VARCHAR(50) );')

    questions_table = ('CREATE TABLE IF NOT EXISTS questions'
                       '(id SERIAL PRIMARY KEY,'
                       'title VARCHAR(50) NOT NULL,'
                       'creator INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,'
                       'body VARCHAR NOT NULL,'
                       'meetup INT NOT NULL REFERENCES meetups(id) ON DELETE CASCADE,'
                       'created_on DATE NOT NULL DEFAULT CURRENT_DATE,'
                       'votes INT NOT NULL );')

    answers_table = ('CREATE TABLE IF NOT EXISTS answers'
                     '(id SERIAL PRIMARY KEY,'
                     'creator INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,'
                     'body VARCHAR NOT NULL,'
                     'meetup INT NOT NULL REFERENCES meetups(id) ON DELETE CASCADE,'
                     'question INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE);')

    rsvps_table = ('CREATE TABLE IF NOT EXISTS rsvps'
                   '(id SERIAL NOT NULL,'
                   'status VARCHAR(5) NOT NULL,'
                   'meetup INT NOT NULL REFERENCES meetups(id) ON DELETE CASCADE,'
                   'creator INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, '
                   'PRIMARY KEY (creator, meetup));')

    votes_table = ('CREATE TABLE IF NOT EXISTS votes'
                   '(id SERIAL PRIMARY KEY,'
                   'creator INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,'
                   'question INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,'
                   'count INT NOT NULL );')

    tables = [users_table, meetups_table, questions_table, answers_table, votes_table, rsvps_table]
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
                    default_admin["phonenumber"], generate_password_hash(default_admin["password"]),
                    default_admin["username"], default_admin["is_admin"]))
