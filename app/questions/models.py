from ..db import InitDb


class PostQuestionsModel:
    """model to handle questions data"""
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
        InitDb.cursor.execute(insert_query,
                              (self.title, self.creator, self.body,
                               self.meetup, self.votes))


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
        InitDb.cursor.execute(insert_query,
                              (self.body, self.creator, self.meetup,
                               self.question))


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
        InitDb.cursor.execute(insert_query,
                              (self.user, self.question, self.vote))

    @staticmethod
    def delete_vote(user, question):
        """delete vote"""
        delete_query = ('DELETE FROM votes '
                        'WHERE creator = {} '
                        'AND question = {}'.format(user["id"], question))
        InitDb.cursor.execute(delete_query)

    @staticmethod
    def sum_votes(q_id):
        """get sum of all votes the question has"""
        InitDb.cursor.execute('SELECT COALESCE(SUM(count),0) as votes '
                              'FROM votes '
                              'WHERE question = (%s)', (q_id,))
        votes = InitDb.cursor.fetchone()
        return votes
