import os

from ..utils.validators import DbValidators


class CreateTables:
    """create required db tables"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cursor = cnxn.cursor()

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
                     'creator INT NOT NULL,'
                     'location VARCHAR(150) NOT NULL,'
                     'happening_on DATE NOT NULL,'
                     'created_on DATE NOT NULL DEFAULT CURRENT_DATE,'
                     'tags VARCHAR(50),'
                     'image VARCHAR(50) );')

    questions_table = ('CREATE TABLE IF NOT EXISTS questions'
                       '(id SERIAL PRIMARY KEY,'
                       'title VARCHAR(50) NOT NULL,'
                       'creator INT NOT NULL,'
                       'body VARCHAR NOT NULL,'
                       'meetup INT NOT NULL,'
                       'created_on DATE NOT NULL DEFAULT CURRENT_DATE,'
                       'votes INT NOT NULL );')

    answers_table = ('CREATE TABLE IF NOT EXISTS answers'
                     '(id SERIAL PRIMARY KEY,'
                     'creator INT NOT NULL,'
                     'body VARCHAR NOT NULL,'
                     'meetup INT NOT NULL,'
                     'question INT NOT NULL );')

    rsvps_table = ('CREATE TABLE IF NOT EXISTS rsvps'
                   '(id SERIAL PRIMARY KEY,'
                   'status VARCHAR(5) NOT NULL,'
                   'meetup INT NOT NULL,'
                   'creator INT NOT NULL );')

    votes_table = ('CREATE TABLE IF NOT EXISTS votes'
                   '(id SERIAL PRIMARY KEY,'
                   'creator INT NOT NULL,'
                   'question INT NOT NULL,'
                   'count INT NOT NULL );')

    tables = [users_table, meetups_table, questions_table, answers_table, votes_table, rsvps_table]
    DbValidators.create_tables(cnxn, cursor, *tables)
