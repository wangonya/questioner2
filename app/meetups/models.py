from ..db import InitDb
from ..db.select import SelectDataFromDb


class MeetupModel:
    """model to handle meetup data"""

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
        InitDb.cursor.execute(insert_query,
                              (self.title, self.creator, self.location,
                               self.happening_on, self.tags, self.image))

    @staticmethod
    def get_upcoming_meetups():
        """get all upcoming meetups"""
        meetups = SelectDataFromDb.general_select("meetups")
        return meetups

    @staticmethod
    def get_specific_meetup(m_id):
        """get all upcoming meetups"""
        meetups = SelectDataFromDb.conditional_where_select("meetups", "id", m_id)
        return meetups

    @staticmethod
    def delete_meetup(m_id):
        """delete meetup"""
        InitDb.cursor.execute('DELETE FROM meetups '
                              'WHERE id = (%s)', (m_id,))


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
        InitDb.cursor.execute(insert_query,
                              (self.status.lower(), self.uid["id"], self.m_id))

    @staticmethod
    def check_duplicate_rsvp(user, m_id):
        """check if user has already rsvp'd
        if they have, updte the record"""
        data = ["meetup", m_id, "creator", user["id"]]
        rsvp = SelectDataFromDb.conditional_where_and_select("rsvps", *data)
        return rsvp

    @staticmethod
    def update_rsvp(status, user, meetup):
        """update rsvp"""
        query = ('UPDATE rsvps SET status = %s '
                 'WHERE creator = %s '
                 'AND meetup = %s')
        InitDb.cursor.execute(query, (status.lower(), user["id"], meetup))
