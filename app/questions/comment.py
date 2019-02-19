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
                        type=str,
                        required=True,
                        nullable=False,)

    @jwt_required
    def post(self, q_id):
        """
        Comment on a question
        ---
            tags:
            - questions
            consumes:
            - application/json
            parameters:
            - in: header
              name: Authorization
              description: JWT token
              type: string
              required: true
            - in: path
              name: q_id
              type: int
              required: true
              description: The id of the question to comment on
            - in: body
              name: Add Comment
              description: Comment on a question
              schema:
                id: Comment on a question
                type: object
                required:
                - body
                properties:
                  body:
                    type: string
            responses:
              201:
                description: answer submitted successfully
              404:
                description: No question matching the id passed was found
              409:
                description: The data provided already exists in the resource
        """
        data = self.parser.parse_args()
        body = data["body"]

        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)

        GeneralValidators.non_empty_string(**data)
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
                "comment": body,
                "question": q_id
            }]}

        return response, 201
