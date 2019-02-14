from flask import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..db import InitDb
from ..utils.validators import MeetupValidators
from ..db.select import SelectDataFromDb


class UserProfile(Resource):
    """user profile"""
    @staticmethod
    @jwt_required
    def get():
        """get user profile"""
        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)
        meetups_query = ('SELECT m.title m_title, '
                         'm.happening_on m_date, '
                         'm.id m_id '
                         'FROM meetups m '
                         'LEFT JOIN rsvps r ON m.id = r.meetup '
                         'WHERE r.status = %s '
                         'AND r.creator = %s '
                         'ORDER BY m_date ASC')
        InitDb.cursor.execute(meetups_query, ('yes', creator["id"]))
        meetups = json.dumps(InitDb.cursor.fetchall(), default=str)

        questions_query = ('SELECT q.title q_title, '
                           'q.created_on q_date '
                           'FROM questions q '
                           'LEFT JOIN rsvps r ON q.meetup = r.meetup '
                           'WHERE r.status = %s '
                           'AND r.creator = %s '
                           'ORDER BY q.votes ASC')
        InitDb.cursor.execute(questions_query, ('yes', creator["id"]))
        questions = json.dumps(InitDb.cursor.fetchall(), default=str)

        asked = SelectDataFromDb.select_count("questions", "creator", creator["id"])
        answered = SelectDataFromDb.select_count("answers", "creator", creator["id"])

        res = {
            "status": 200,
            "data": [{
                "meetups": json.loads(meetups),
                "top_questions": json.loads(questions),
                "user_email": user,
                "is_admin": creator["is_admin"],
                "asked": asked["count"],
                "answered": answered["count"]
            }]
        }

        return res, 200


class AdminProfile(Resource):
    """admin profile"""
    @staticmethod
    @jwt_required
    def get():
        """GET all meetups by a certain admin"""
        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)
        MeetupValidators.check_creator_is_admin(creator)

        meetups = SelectDataFromDb.conditional_where_select_all("meetups", "creator", creator["id"])
        meetups = json.dumps(meetups, default=str)

        questions_query = ('SELECT q.title q_title, '
                           'q.created_on q_date '
                           'FROM questions q '
                           'LEFT JOIN meetups m ON q.meetup = m.id '
                           'WHERE m.creator = {} '
                           'ORDER BY q.votes ASC'.format(creator["id"]))
        InitDb.cursor.execute(questions_query)
        questions = json.dumps(InitDb.cursor.fetchall(), default=str)

        response = {
            "status": 200,
            "data": [{
                "meetups": json.loads(meetups),
                "questions": json.loads(questions),
                "admin_email": user,
                "is_admin": creator["is_admin"],
                "meetups_posted": len(json.loads(meetups))
            }]
        }

        return response, 200
