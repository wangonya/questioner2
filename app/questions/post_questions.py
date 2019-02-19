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
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("body",
                        type=str,
                        required=True,
                        nullable=False,)

    @jwt_required
    def post(self, m_id):
        """
        Post Question
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
              name: m_id
              type: int
              required: true
              description: The id of the meetup to add question
            - in: body
              name: Create question
              description: Create new question
              schema:
                id: Post Question
                type: object
                required:
                - title
                - body
                properties:
                  title:
                    type: string
                  body:
                    type: string
            responses:
              201:
                description: question submitted successfully
              400:
                description: Invalid data format
              404:
                description: No meetup matching the id passed was found
        """
        data = self.parser.parse_args()
        title = data["title"]
        body = data["body"]

        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)

        GeneralValidators.non_empty_string(**data)
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
