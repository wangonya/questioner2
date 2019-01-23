import os

from psycopg2.extras import RealDictCursor

from ..utils.validators import DbValidators


class PostQuestionsModel:
    """model to handle questions data"""
    cnxn = DbValidators.connect_to_db(os.getenv("DEV_DB_URI"))
    cnxn.autocommit = True
    cursor = cnxn.cursor(cursor_factory=RealDictCursor)

    def __init__(self, title, creator, body, meetup):
        self.title = title
        self.creator = creator
        self.body = body
        self.meetup = meetup
        self.votes = 0

    def save_question_to_db(self):
        """save entered question data to db"""
        insert_query = ('INSERT INTO questions '
                        '(title, creator, body, meetup, votes) '
                        'VALUES (%s, %s, %s, %s, %s);')
        PostQuestionsModel.cursor.execute(insert_query,
                                          (self.title, self.creator, self.body,
                                           self.meetup, self.votes))

    @classmethod
    def find_question(cls, title):
        """check if a question with the same title already exists"""
        cls.cursor.execute('SELECT * '
                           'FROM questions '
                           'WHERE title = (%s)', (title,))
        question = cls.cursor.fetchone()
        return question
