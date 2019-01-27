from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utils.validators import QuestionValidators
from ..questions.models import VoteModel
from ..db.select import SelectDataFromDb


class Upvote(Resource):
    """upvote question endpoint"""
    @staticmethod
    @jwt_required
    def patch(q_id):
        """do a PATCH on upvote question endpoint"""
        QuestionValidators.check_question_exists(q_id)
        user = get_jwt_identity()
        voter = SelectDataFromDb.conditional_where_select("users", "email", user)

        data = SelectDataFromDb.conditional_where_select("questions", "id", q_id)

        vote = VoteModel(voter["id"], q_id, 1)
        if not SelectDataFromDb.conditional_where_and_select("votes", "creator", voter["id"], "question", q_id):
            vote.save_vote_to_db()
        else:
            VoteModel.delete_vote(voter, q_id)
        votes = VoteModel.sum_votes(q_id)

        response = {
            "status": 201,
            "message": "vote added successfully",
            "data": [{
                "title": data["title"],
                "body": data["body"],
                "meetup": data["meetup"],
                "votes": votes["votes"]
            }]
        }

        return response, 201


class Downvote(Resource):
    """downvote question endpoint"""
    @staticmethod
    @jwt_required
    def patch(q_id):
        """do a PATCH on upvote question endpoint"""
        QuestionValidators.check_question_exists(q_id)
        user = get_jwt_identity()
        voter = SelectDataFromDb.conditional_where_select("users", "email", user)

        data = SelectDataFromDb.conditional_where_select("questions", "id", q_id)

        vote = VoteModel(voter["id"], q_id, -1)
        if not SelectDataFromDb.conditional_where_and_select("votes", "creator", voter["id"], "question", q_id):
            vote.save_vote_to_db()
        else:
            VoteModel.delete_vote(voter, q_id)
        votes = VoteModel.sum_votes(q_id)

        response = {
            "status": 201,
            "message": "vote added successfully",
            "data": [{
                "title": data["title"],
                "body": data["body"],
                "meetup": data["meetup"],
                "votes": votes["votes"]
            }]
        }

        return response, 201
