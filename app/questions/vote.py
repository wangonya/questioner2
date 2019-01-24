from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..questions.models import VoteModel
from ..auth.models import AuthModel
from ..utils.validators import QuestionValidators


class Upvote(Resource):
    @staticmethod
    @jwt_required
    def patch(q_id):
        """do a PATCH on upvote question endpoint"""
        data = VoteModel.get_specific_question(q_id)
        user = get_jwt_identity()
        voter = AuthModel.find_by_email(user)

        QuestionValidators.check_question_exists(q_id)

        vote = VoteModel(voter["id"], q_id, 1)
        if not VoteModel.check_vote_exists(voter, q_id):
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
