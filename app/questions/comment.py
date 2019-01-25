from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..questions.models import PostQuestionsModel, AnswerQuestionsModel, VoteModel
from ..auth.models import AuthModel
from ..utils.validators import AnswerValidators, QuestionValidators, GeneralValidators


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
        creator = AuthModel.find_by_email(user)

        QuestionValidators.check_question_exists(q_id)
        question = VoteModel.get_specific_question(q_id)
        m_id = PostQuestionsModel.find_meetup_by_q_id(q_id)

        AnswerValidators.check_duplicate_answer(body, q_id)

        answer = AnswerQuestionsModel(body, creator["id"], m_id["meetup"], q_id)
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
