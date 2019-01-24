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
    def get_specific_meetup(cls, m_id):
        """get all upcoming meetups"""
        cls.cursor.execute('SELECT * '
                           'FROM meetups '
                           'WHERE id = (%s)', (m_id,))
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


class RsvpsModel:
    """model to handle rsvp data"""

    def __init__(self, status, uid, m_id):
        self.status = status
        self.uid = uid
        self.m_id = m_id

    def save_rsvp_to_db(self):
        """save entered rsvp data to db"""
        insert_query = ('INSERT INTO rsvps '
                        '(status, creator, meetup) '
                        'VALUES (%s, %s, %s);')
        MeetupModel.cursor.execute(insert_query,
                                   (self.status, self.uid["id"], self.m_id))

    @classmethod
    def check_duplicate_rsvp(cls, user, m_id):
        """check if user has already rsvp'd
        if they have, updte the record"""
        MeetupModel.cursor.execute('SELECT * '
                                   'FROM rsvps '
                                   'WHERE meetup = {} '
                                   'AND creator = {}'.format(m_id, user["id"]))
        rsvp = MeetupModel.cursor.fetchone()
        return rsvp

    @staticmethod
    def update_rsvp(status, user, meetup):
        """update rsvp"""
        delete_query = ('UPDATE rsvps SET status = {} '
                        'WHERE creator = {} '
                        'AND meetup = {}'.format(status, user["id"], meetup))
        MeetupModel.cursor.execute(delete_query)
