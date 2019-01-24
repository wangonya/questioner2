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

    @classmethod
    def find_meetup_by_q_id(cls, q_id):
        """find meetup with matching question id"""
        cls.cursor.execute('SELECT * '
                           'FROM questions '
                           'WHERE id = (%s)', (q_id,))
        question = cls.cursor.fetchone()
        return question


class AnswerQuestionsModel:
    """model to handle answers data"""
    def __init__(self, body, creator, meetup, question):
        self.body = body
        self.creator = creator
        self.meetup = meetup
        self.question = question

    def save_answer_to_db(self):
        """save entered answer to db"""
        insert_query = ('INSERT INTO answers '
                        '(body, creator, meetup, question) '
                        'VALUES (%s, %s, %s, %s);')
        PostQuestionsModel.cursor.execute(insert_query,
                                          (self.body, self.creator, self.meetup,
                                           self.question))


    @classmethod
    def find_duplicate_answer(cls, body, question):
        """check if a similar answer exists in the question"""
        select_query = ('SELECT * FROM answers '
                        'WHERE question = %s '
                        'AND body = %s')
        PostQuestionsModel.cursor.execute(select_query, (question, body))
        answer = PostQuestionsModel.cursor.fetchone()
        return answer


class VoteModel:
    """model to handle votes data"""

    def __init__(self, user, question, vote):
        self.user = user
        self.question = question
        self.vote = vote

    def save_vote_to_db(self):
        """save entered vote to db"""
        insert_query = ('INSERT INTO votes '
                        '(creator, question, count) '
                        'VALUES (%s, %s, %s);')
        PostQuestionsModel.cursor.execute(insert_query,
                                          (self.user, self.question, self.vote))

    @staticmethod
    def delete_vote(user, question):
        """delete vote"""
        delete_query = ('DELETE FROM votes '
                        'WHERE creator = {} '
                        'AND question = {}'.format(user["id"], question))
        PostQuestionsModel.cursor.execute(delete_query)

    @staticmethod
    def sum_votes(q_id):
        """get sum of all votes the question has"""
        PostQuestionsModel.cursor.execute('SELECT COALESCE(SUM(count),0) as votes '
                                          'FROM votes '
                                          'WHERE question = (%s)', (q_id,))
        votes = PostQuestionsModel.cursor.fetchone()
        return votes

    @staticmethod
    def get_specific_question(q_id):
        """get specific question"""
        PostQuestionsModel.cursor.execute('SELECT * '
                                          'FROM questions '
                                          'WHERE id = (%s)', (q_id,))
        question = PostQuestionsModel.cursor.fetchone()
        return question

    @staticmethod
    def check_vote_exists(user, q_id):
        """check if user has already voted"""
        PostQuestionsModel.cursor.execute('SELECT * '
                                          'FROM votes '
                                          'WHERE question = {} '
                                          'AND creator = {}'.format(q_id, user["id"]))
        vote = PostQuestionsModel.cursor.fetchone()
        return vote
