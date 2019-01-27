from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..questions.models import PostQuestionsModel
from ..utils.validators import (QuestionValidators, MeetupValidators,
                                GeneralValidators)
from ..db.select import SelectDataFromDb


class PostQuestion(Resource):
    """post question endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("title",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("body",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)

    @jwt_required
    def post(self, m_id):
        """do a POST on the questions endpoint"""
        data = self.parser.parse_args()
        title = data["title"]
        body = data["body"]

        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)

        MeetupValidators.check_meetup_exists(m_id)

        QuestionValidators.check_duplicate_question(title, m_id)

        question = PostQuestionsModel(title, creator["id"], body, m_id)
        question.save_question_to_db()

        response = {
            "status": 201,
            "message": "question submitted successfully",
            "data": [{
                "title": title,
                "body": body,
                "creator": creator["id"],
                "meetup": m_id
            }]}

        return response, 201
