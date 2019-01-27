from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..questions.models import AnswerQuestionsModel
from ..utils.validators import (AnswerValidators, QuestionValidators,
                                GeneralValidators)
from ..db.select import SelectDataFromDb


class Comment(Resource):
    """post answer endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("body",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)

    @jwt_required
    def post(self, q_id):
        """do a POST on the answers endpoint"""
        data = self.parser.parse_args()
        body = data["body"]

        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)

        QuestionValidators.check_question_exists(q_id)
        question = SelectDataFromDb.conditional_where_select("questions", "id", q_id)

        AnswerValidators.check_duplicate_answer(body, q_id)

        answer = AnswerQuestionsModel(body, creator["id"], question["meetup"], q_id)
        answer.save_answer_to_db()

        response = {
            "status": 201,
            "message": "answer submitted successfully",
            "data": [{
                "body": question["body"],
                "title": question["title"],
                "mcomment": body,
                "question": q_id
            }]}

        return response, 201
