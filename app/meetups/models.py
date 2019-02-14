from ..db import InitDb
from ..db.select import SelectDataFromDb


class MeetupModel:
    """model to handle meetup data"""

    def __init__(self, title, details, creator, location,
                 happening_on, tags, image):
        self.title = title
        self.details = details
        self.creator = creator
        self.location = location
        self.happening_on = happening_on
        self.tags = tags,
        self.image = image

    def save_meetup_to_db(self):
        """save entered meetup data to db"""
        insert_query = ('INSERT INTO meetups '
                        '(title, details, creator, location, '
                        'happening_on, tags, image)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s);')
        InitDb.cursor.execute(insert_query,
                              (self.title, self.details, self.creator, self.location,
                               self.happening_on, self.tags, self.image))

    @staticmethod
    def get_upcoming_meetups():
        """get all upcoming meetups"""
        meetups = SelectDataFromDb.general_select("meetups")
        return meetups

    @staticmethod
    def get_specific_meetup(m_id):
        """get all upcoming meetups"""
        select_query = ('SELECT m.*, '
                        'q.title q_title, '
                        'q.id q_id, '
                        'v.count votes, '
                        'COUNT(a.meetup) AS comments '
                        'FROM meetups m '
                        'LEFT JOIN questions q ON m.id = q.meetup '
                        'LEFT JOIN votes v ON q.id = v.question '
                        'LEFT JOIN answers a ON q.id = a.question '
                        'WHERE m.id = (%s) '
                        'GROUP BY q.title, q.votes, v.count, m.id, q.id '
                        'ORDER BY q.votes ASC')
        InitDb.cursor.execute(select_query, (m_id, ))
        meetups = InitDb.cursor.fetchall()
        return meetups

    @staticmethod
    def get_specific_meetup_question(q_id):
        """get specific meetup question"""
        select_query = ('SELECT q.*, '
                        'a.body q_comment '
                        'FROM questions q '
                        'LEFT JOIN answers a ON q.id = a.question '
                        'WHERE q.id = (%s) ')
        InitDb.cursor.execute(select_query, (q_id,))
        question = InitDb.cursor.fetchall()
        return question

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
