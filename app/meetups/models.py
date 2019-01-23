import os

from psycopg2.extras import RealDictCursor

from ..utils.validators import DbValidators


class MeetupModel:
    """model to handle meetup data"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cnxn.autocommit = True
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)

    def __init__(self, title, creator, location,
                 happening_on, tags, image):
        self.title = title
        self.creator = creator
        self.location = location
        self.happening_on = happening_on
        self.tags = tags,
        self.image = image

    def save_meetup_to_db(self):
        """save entered meetup data to db"""
        insert_query = ('INSERT INTO meetups '
                        '(title, creator, location, '
                        'happening_on, tags, image) '
                        'VALUES (%s, %s, %s, %s, %s, %s);')
        MeetupModel.cursor.execute(insert_query,
                                   (self.title, self.creator, self.location,
                                    self.happening_on, self.tags, self.image))

    @classmethod
    def get_upcoming_meetups(cls):
        """get all upcoming meetups"""
        cls.cursor.execute('SELECT * '
                           'FROM meetups')
        meetups = cls.cursor.fetchall()
        return meetups

    @classmethod
    def find_meetup(cls, title):
        """check if a meetup with the same title already exists"""
        cls.cursor.execute('SELECT * '
                           'FROM meetups '
                           'WHERE title = (%s)', (title,))
        meetup = cls.cursor.fetchone()
        return meetup
